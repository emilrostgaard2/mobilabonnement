"""Telemobil Prisindeks — beregning og visning.

HVORFOR ET INDEKS: medianen af "alle abonnementer i dag" mod "alle dengang"
sammenligner to forskellige kurve. Ryger et selskab ud af feedet, hopper tallet
15 % uden at én eneste pris er ændret. Det kan ingen journalist citere.

Indekset følger derfor de SAMME abonnementer fra måling til måling (matched
model) og kædes sammen dag for dag med geometrisk gennemsnit af prisforholdene
— samme princip som elementærindeks i forbrugerprisindekset. Nye og udgåede
abonnementer påvirker ikke tallet; kun reelle prisændringer gør.
"""
import json
import math
import os
from datetime import date

MD = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august",
      "september", "oktober", "november", "december"]
MDK = ["jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "aug.", "sep.", "okt.", "nov.", "dec."]

SORT, GRAA, LINJE = "#1A1A1A", "#666666", "#DCDCDC"
OP, NED, NEUTRAL = "#B3261E", "#1B7F4B", "#BDBDBD"


def d_kort(iso):
    d = date.fromisoformat(iso)
    return f"{d.day}. {MDK[d.month - 1]}"


def d_lang(iso):
    d = date.fromisoformat(iso)
    return f"{d.day}. {MD[d.month - 1]} {d.year}"


def tal(x, dec=1):
    return f"{x:.{dec}f}".replace(".", ",")


def kr(v):
    return f"{v:,.0f}".replace(",", ".")


def median(v):
    v = sorted(v)
    n = len(v)
    return None if not n else (v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2)


def geo(forhold):
    return math.exp(sum(math.log(f) for f in forhold) / len(forhold)) if forhold else 1.0


# ------------------------------------------------------------------ BEREGNING
def beregn(maalinger, abon, umap):
    """Returnerer None, hvis der ikke er to målinger med enkeltpriser."""
    m = [x for x in maalinger if x.get("priser")]
    if len(m) < 2:
        return None
    navne = {a["id"]: a for a in abon}

    def selskab(pid):
        if pid in navne:
            return navne[pid]["udbyder"]
        return next((s for s in sorted(umap, key=len, reverse=True) if pid.startswith(s + "-")), None)

    serie = [{"dato": m[0]["dato"], "indeks": 100.0, "median": median(m[0]["priser"].values()),
              "antal": len(m[0]["priser"]), "aendret": 0}]
    log = []
    for a, b in zip(m, m[1:]):
        faelles = [i for i in a["priser"] if i in b["priser"] and a["priser"][i] > 0 and b["priser"][i] > 0]
        led = geo([b["priser"][i] / a["priser"][i] for i in faelles])
        aendrede = [i for i in faelles if a["priser"][i] != b["priser"][i]]
        for i in aendrede:
            s = selskab(i)
            log.append({"dato": b["dato"], "id": i, "selskab": s,
                        "navn": navne[i]["navn"] if i in navne else "Abonnement, der siden er udgået",
                        "foer": a["priser"][i], "efter": b["priser"][i]})
        serie.append({"dato": b["dato"], "indeks": serie[-1]["indeks"] * led,
                      "median": median(b["priser"].values()), "antal": len(b["priser"]),
                      "aendret": len(aendrede),
                      "selskaber": sorted({selskab(i) for i in aendrede if selskab(i)})})

    f, s = m[0]["priser"], m[-1]["priser"]
    faelles = [i for i in f if i in s]
    dyrere = [i for i in faelles if s[i] > f[i]]
    billigere = [i for i in faelles if s[i] < f[i]]

    pr_selskab = {}
    for slug in umap:
        egne_nu = [a for a in abon if a["udbyder"] == slug and a["pris"] > 0]
        if not egne_nu:
            continue
        ids = [i for i in faelles if selskab(i) == slug]
        pr_selskab[slug] = {
            "antal": len(egne_nu), "billigst": min(a["pris"] for a in egne_nu),
            "median": median([a["pris"] for a in egne_nu]),
            "aendring": (geo([s[i] / f[i] for i in ids]) - 1) * 100 if ids else None,
            "op": len([i for i in ids if s[i] > f[i]]), "ned": len([i for i in ids if s[i] < f[i]]),
        }
    return {
        "serie": serie, "log": sorted(log, key=lambda x: x["dato"], reverse=True),
        "start": m[0]["dato"], "slut": m[-1]["dato"], "maaledage": len(m),
        "dage": (date.fromisoformat(m[-1]["dato"]) - date.fromisoformat(m[0]["dato"])).days,
        "indeks": serie[-1]["indeks"], "pct": serie[-1]["indeks"] - 100,
        "median": median(s.values()), "antal": len(s),
        "dyrere": len(dyrere), "billigere": len(billigere),
        "uaendret": len(faelles) - len(dyrere) - len(billigere),
        "nye": len([i for i in s if i not in f]), "udgaaet": len([i for i in f if i not in s]),
        "pr_selskab": pr_selskab,
    }


def retning(pct):
    return "op" if pct >= 0.05 else "ned" if pct <= -0.05 else "flad"


def rubrik(R):
    _d = date.fromisoformat(R["start"])
    p, fra = abs(R["pct"]), f"{_d.day}. {MD[_d.month - 1]}"
    r = retning(R["pct"])
    if r == "op":
        return f"Mobilpriserne er steget {tal(p)}&nbsp;% siden {fra}"
    if r == "ned":
        return f"Mobilpriserne er faldet {tal(p)}&nbsp;% siden {fra}"
    return f"Mobilpriserne har stået stille siden {fra}"


def underrubrik(R):
    def n(x, en, fl):
        return f"{'Ét' if x == 1 else x} {en if x == 1 else fl}"
    if not R["dyrere"] and not R["billigere"]:
        return (f"Ingen af de {R['uaendret']} abonnementer, vi har fulgt hele perioden, har "
                f"ændret normalpris.")
    def ab(x):
        return f"{x} abonnement" if x == 1 else f"{x} abonnementer"
    if R["dyrere"] and R["billigere"]:
        dele = [f"{ab(R['dyrere'])} er blevet dyrere og {R['billigere']} billigere"]
    elif R["dyrere"]:
        dele = [f"{ab(R['dyrere'])} er blevet dyrere, ingen billigere"]
    else:
        dele = [f"{ab(R['billigere'])} er blevet billigere, ingen dyrere"]
    hvem = sorted(s for s, d in R["pr_selskab"].items() if d["op"] or d["ned"])
    return (f"{' og '.join(dele)}. De øvrige {R['uaendret']} koster det samme som den "
            f"{d_lang(R['start'])}. Ændringerne kommer fra {len(hvem)} "
            f"{'selskab' if len(hvem) == 1 else 'selskaber'}.")


def citat(R):
    r = retning(R["pct"])
    verb = {"op": f"er steget {tal(abs(R['pct']))} procent", "ned": f"er faldet {tal(abs(R['pct']))} procent",
            "flad": "har stået stille"}[r]
    sel = len(R["pr_selskab"])
    return (f"Priserne på danske mobilabonnementer {verb} siden {d_lang(R['start'])}, viser "
            f"Telemobil Prisindeks, der følger {R['antal']} abonnementer fra {sel} selskaber to "
            f"gange dagligt.")


# ------------------------------------------------------------------ GRAFIK
def graf_svg(R, bredde=1100, hoejde=380, selvstaendig=False):
    S = R["serie"]
    d0 = date.fromisoformat(S[0]["dato"])
    span = max((date.fromisoformat(S[-1]["dato"]) - d0).days, 1)
    v = [p["indeks"] for p in S]
    lo, hi = min(v + [100]), max(v + [100])
    luft = max((hi - lo) * .22, .25)
    lo, hi = lo - luft, hi + luft * 1.6
    pv, ph, pt, pb = 40, 92, 22, 38

    def X(iso):
        return pv + (bredde - pv - ph) * (date.fromisoformat(iso) - d0).days / span

    def Y(x):
        return pt + (hoejde - pt - pb) * (1 - (x - lo) / (hi - lo))

    trin = next(t for t in (.1, .2, .25, .5, 1, 2, 5, 10) if (hi - lo) / t <= 7)
    g, t = "", math.floor(lo / trin) * trin
    while t <= hi:
        if t >= lo:
            basis = abs(t - 100) < 1e-6
            g += (f'<line x1="{pv}" y1="{Y(t):.1f}" x2="{bredde - ph}" y2="{Y(t):.1f}" '
                  f'stroke="{SORT if basis else LINJE}" stroke-width="1"/>'
                  f'<text x="{pv - 8}" y="{Y(t) + 4:.1f}" text-anchor="end" font-size="12" fill="{GRAA}" '
                  f'font-weight="{700 if basis else 400}">{tal(t, 1 if trin < 1 else 0)}</text>')
        t = round(t + trin, 4)
    skridt = 7 if span <= 70 else 30
    for k in range(0, span + 1, skridt):
        iso = date.fromordinal(d0.toordinal() + k).isoformat()
        g += (f'<line x1="{X(iso):.1f}" y1="{hoejde - pb}" x2="{X(iso):.1f}" y2="{hoejde - pb + 5}" stroke="{GRAA}"/>'
              f'<text x="{X(iso):.1f}" y="{hoejde - pb + 21}" text-anchor="{"start" if k == 0 else "middle"}" '
              f'font-size="12" fill="{GRAA}">{d_kort(iso)}</text>')

    sti = f"M{X(S[0]['dato']):.1f} {Y(S[0]['indeks']):.1f}"
    for a, b in zip(S, S[1:]):
        sti += f" L{X(b['dato']):.1f} {Y(a['indeks']):.1f}"
        if abs(b["indeks"] - a["indeks"]) > 1e-9:
            sti += f" L{X(b['dato']):.1f} {Y(b['indeks']):.1f}"
    farve = {"op": OP, "ned": NED, "flad": SORT}[retning(R["pct"])]
    g += (f'<path d="{sti} L{X(S[-1]["dato"]):.1f} {Y(100):.1f} L{X(S[0]["dato"]):.1f} {Y(100):.1f} Z" '
          f'fill="{farve}" fill-opacity=".08"/>'
          f'<path d="{sti}" fill="none" stroke="{SORT}" stroke-width="2.25"/>')
    if len(S) <= 90:
        for p in S:
            g += (f'<circle cx="{X(p["dato"]):.1f}" cy="{Y(p["indeks"]):.1f}" r="2.2" fill="#fff" '
                  f'stroke="{SORT}" stroke-width="1.25"/>')
    for n, p in enumerate(_markeringer(R), 1):
        x, y = X(p["dato"]), Y(p["indeks"])
        g += (f'<line x1="{x:.1f}" y1="{y - 6:.1f}" x2="{x:.1f}" y2="{y - 22:.1f}" stroke="{SORT}"/>'
              f'<circle cx="{x:.1f}" cy="{y - 31:.1f}" r="9" fill="#fff" stroke="{SORT}" stroke-width="1.25"/>'
              f'<text x="{x:.1f}" y="{y - 27:.1f}" text-anchor="middle" font-size="11.5" font-weight="700" '
              f'fill="{SORT}">{n}</text>')
    sx, sy = X(S[-1]["dato"]), Y(S[-1]["indeks"])
    g += (f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.5" fill="{farve}" stroke="#fff" stroke-width="2"/>'
          f'<text x="{sx + 12:.1f}" y="{sy + 1:.1f}" font-size="21" font-weight="700" fill="{farve}">'
          f'{tal(R["indeks"])}</text><text x="{sx + 12:.1f}" y="{sy + 17:.1f}" font-size="12" '
          f'fill="{GRAA}">{d_kort(R["slut"])}</text>')
    ekstra = ""
    if selvstaendig:
        ekstra = (f'<rect width="{bredde}" height="{hoejde + 34}" fill="#fff"/>'
                  f'<text x="{pv}" y="{hoejde + 22}" font-size="12.5" fill="{GRAA}">Kilde: Telemobil '
                  f'Prisindeks · telemobil.dk/prisudvikling · {d_lang(R["start"])} = 100</text>')
    h = hoejde + (34 if selvstaendig else 0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bredde} {h}" width="{bredde}" '
            f'height="{h}" role="img" font-family="Georgia,serif" aria-label="Telemobil Prisindeks fra '
            f'{d_lang(R["start"])} til {d_lang(R["slut"])}: {tal(R["indeks"])}">{ekstra}{g}</svg>')


def _markeringer(R):
    """De op til tre største trin — dem, en læser vil have forklaret."""
    trin = []
    for a, b in zip(R["serie"], R["serie"][1:]):
        if b["aendret"]:
            trin.append((abs(b["indeks"] - a["indeks"]), b))
    return sorted([b for _, b in sorted(trin, key=lambda x: -x[0])[:3]], key=lambda p: p["dato"])


def _noter(R, umap, e):
    ud = ""
    for n, p in enumerate(_markeringer(R), 1):
        hvem = [umap[s]["navn"] for s in p.get("selskaber", []) if s in umap]
        aendr = [x for x in R["log"] if x["dato"] == p["dato"]]
        op = len([x for x in aendr if x["efter"] > x["foer"]])
        ned = len(aendr) - op
        hvad = " og ".join(filter(None, [f"{op} dyrere" if op else "", f"{ned} billigere" if ned else ""]))
        ud += (f'<li><span>{n}</span><b>{d_kort(p["dato"])}</b> {e(", ".join(hvem) or "Flere selskaber")}: '
               f'{hvad}</li>')
    return f'<ol class="pi-noter">{ud}</ol>' if ud else ""


# ------------------------------------------------------------------ SEKTIONER
def _logo(u, h=20):
    w = round(u.get("logo_w", 240) * h / u.get("logo_h", 96))
    return (f'<img src="/assets/img/logoer/{u["logo"]}" alt="{u["navn"]}" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async">')


def _pil(d, enhed="kr."):
    if d == 0:
        return '<span class="pi-flad">uændret</span>'
    return (f'<span class="pi-{"op" if d > 0 else "ned"}">{"+" if d > 0 else "−"}'
            f'{kr(abs(d)) if enhed == "kr." else tal(abs(d))} {enhed}</span>')


def sek_log(R, umap, e, maks=12):
    if not R["log"]:
        return ('<h2 id="aendringer">Seneste prisændringer</h2><p>Ingen abonnementer har ændret '
                f'normalpris siden {d_lang(R["start"])}. Når det sker, lander ændringen her med dato.</p>')
    r = ""
    for x in R["log"][:maks]:
        u = umap.get(x["selskab"])
        r += (f'<tr><td class="pi-dato">{d_kort(x["dato"])}</td>'
              f'<td class="pi-sel">{_logo(u) if u else ""}</td>'
              f'<td><a href="/udbydere/{x["selskab"]}/">{e(u["navn"]) if u else "Ukendt"}</a>'
              f'<span class="pi-u">{e(x["navn"])}</span></td>'
              f'<td class="t"><s>{kr(x["foer"])} kr.</s></td><td class="t"><b>{kr(x["efter"])} kr.</b></td>'
              f'<td class="t">{_pil(x["efter"] - x["foer"])}</td></tr>')
    flere = (f'<p class="pi-note">Viser de seneste {maks} af {len(R["log"])} ændringer. Alle ligger i '
             f'<a href="/prisudvikling/telemobil-prisindeks.csv">datafilen</a>.</p>'
             if len(R["log"]) > maks else "")
    return f"""<h2 id="aendringer">Seneste prisændringer</h2>
<p>Hver gang et abonnement skifter normalpris, lander det her med dato. Introtilbud tæller ikke.</p>
<div class="tabelrul"><table class="pi-tabel"><thead><tr><th>Dato</th><th colspan="2">Selskab og abonnement</th>
<th class="t">Før</th><th class="t">Nu</th><th class="t">Ændring</th></tr></thead><tbody>{r}</tbody></table></div>{flere}"""


def sek_selskaber(R, umap, e, snapshot=None):
    data = R["pr_selskab"] if R else snapshot
    maks = max([abs(d.get("aendring") or 0) for d in data.values()] + [1])
    r = ""
    for slug, d in sorted(data.items(), key=lambda x: (-(x[1].get("aendring") or 0), umap[x[0]]["navn"])):
        u = umap[slug]
        a = d.get("aendring")
        if a is None:
            bar, txt = "", '<span class="pi-flad">for ny til at måle</span>'
        elif abs(a) < .05:
            bar, txt = "", '<span class="pi-flad">uændret</span>'
        else:
            b = abs(a) / maks * 46
            bar = (f'<i class="pi-bar {"op" if a > 0 else "ned"}" style="width:{b:.1f}%;'
                   f'{"left" if a > 0 else "right"}:50%"></i>')
            txt = _pil(a, "%")
        kol = (f'<td class="pi-div"><div>{bar}</div></td><td class="t pi-aend">{txt}</td>' if R else "")
        r += (f'<tr><td class="pi-sel">{_logo(u, 22)}</td>'
              f'<td><a href="/udbydere/{slug}/"><b>{e(u["navn"])}</b></a>'
              f'<span class="pi-u">Net: {e(u.get("netvaerk", ""))}</span></td>'
              f'<td class="t">{d["antal"]}</td><td class="t">{kr(d["billigst"])} kr.</td>'
              f'<td class="t">{kr(d["median"])} kr.</td>{kol}</tr>')
    hoved = ('<th class="pi-divh">Billigere ← siden start → dyrere</th><th class="t">Ændring</th>' if R else "")
    intro = (f"Gennemsnitlig ændring på de abonnementer, selskabet har haft hele perioden siden "
             f"{d_lang(R['start'])}." if R else "Antal abonnementer og prisniveau hos hvert selskab i dag.")
    return f"""<h2 id="selskaber">Selskaberne enkeltvis</h2>
<p>{intro} Klik på et selskab for at se alle dets abonnementer og vores vurdering.</p>
<div class="tabelrul"><table class="pi-tabel pi-selskaber"><thead><tr><th colspan="2">Selskab</th>
<th class="t">Abonnementer</th><th class="t">Billigste</th><th class="t">Typisk pris</th>{hoved}</tr></thead>
<tbody>{r}</tbody></table></div>"""


def sek_spaend(abon, gb_tekst):
    grupper = [("1–10 GB", 1, 10), ("11–20 GB", 11, 20), ("21–40 GB", 21, 40), ("41–80 GB", 41, 80),
               ("81–200 GB", 81, 200), ("Fri data", 9999, 10 ** 9)]
    rk = []
    for navn, lo, hi in grupper:
        p = [a["pris"] for a in abon if lo <= a["data_gb"] <= hi and a["pris"] > 0
             and not a.get("forbrugsafregnet")]
        if len(p) >= 2:
            rk.append((navn, min(p), median(p), max(p), len(p)))
    if not rk:
        return ""
    top = max(r[3] for r in rk) * 1.12
    r = ""
    for navn, a, m, c, n in rk:
        r += (f'<div class="pi-sr"><b>{navn}<span>{n} abonnementer</span></b><div class="pi-sl">'
              f'<i class="pi-sb" style="left:{a / top * 100:.1f}%;width:{(c - a) / top * 100:.1f}%"></i>'
              f'<i class="pi-sm" style="left:{m / top * 100:.1f}%"></i>'
              f'<em class="l" style="left:{a / top * 100:.1f}%">{kr(a)} kr.</em>'
              f'<em class="r" style="left:{c / top * 100:.1f}%">{kr(c)} kr.</em></div>'
              f'<span class="pi-sd">{kr((c - a) * 12)} kr.</span></div>')
    return f"""<h2 id="prisspaend">Samme datamængde, vidt forskellig pris</h2>
<p>Billigste og dyreste abonnement i hver datastørrelse lige nu. Den sorte streg er den typiske
pris. Tallet til højre er, hvad forskellen løber op i på et år.</p>
<div class="pi-spaend"><div class="pi-sh"><span>Datamængde</span><span>Pris pr. måned</span>
<span>Forskel pr. år</span></div>{r}</div>"""


def sek_kroner(R):
    if retning(R["pct"]) == "flad":
        return ""
    aar = R["median"] * 12 * R["pct"] / 100
    ord_ = "mere" if aar > 0 else "mindre"
    kl = "pi-op" if aar > 0 else "pi-ned"
    celler = "".join(
        f'<div><p class="pi-lab">{hvem}</p><p class="pi-kr {kl}">{"+" if aar > 0 else "−"}{kr(abs(aar) * n)} kr.</p>'
        f'<p class="pi-und">{ord_} om året</p></div>'
        for hvem, n in (("Én person", 1), ("Et par", 2), ("Familie med fire abonnementer", 4)))
    return f"""<div class="pi-kroner"><div><h2>Hvad betyder det i kroner?</h2>
<p>Regnet på et typisk abonnement til {kr(R["median"])} kr. om måneden og ændringen i indekset.</p></div>{celler}</div>"""


def felter(R):
    return "".join(f'<i class="{k}"></i>' for k in
                   ["op"] * R["dyrere"] + ["ned"] * R["billigere"] + ["fl"] * R["uaendret"])


# ------------------------------------------------------------------ FILER
def skriv_filer(R, rod, domaene):
    """CSV, selvstændig SVG og en embed-side. Ligger ved siden af selve siden."""
    mappe = os.path.join(rod, "prisudvikling")
    os.makedirs(mappe, exist_ok=True)
    linjer = ["dato;indeks;medianpris_kr;antal_abonnementer;abonnementer_med_prisaendring"]
    for p in R["serie"]:
        linjer.append(f'{p["dato"]};{tal(p["indeks"], 2)};{tal(p["median"], 0)};{p["antal"]};{p["aendret"]}')
    linjer += ["", "dato;selskab;abonnement;pris_foer_kr;pris_efter_kr"]
    for x in reversed(R["log"]):
        linjer.append(f'{x["dato"]};{x["selskab"] or ""};{x["navn"]};{x["foer"]};{x["efter"]}')
    linjer += ["", f"# Kilde: Telemobil Prisindeks, {domaene}/prisudvikling/ — CC BY 4.0. "
                   f"Indeks: {R['start']} = 100, samme abonnementer fulgt over tid."]
    with open(os.path.join(mappe, "telemobil-prisindeks.csv"), "w", encoding="utf-8-sig") as f:
        f.write("\n".join(linjer))
    with open(os.path.join(mappe, "telemobil-prisindeks.svg"), "w", encoding="utf-8") as f:
        f.write(graf_svg(R, selvstaendig=True))
    embed = f"""<!doctype html><html lang="da"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow">
<title>Telemobil Prisindeks — graf til indlejring</title>
<meta name="description" content="Graf over Telemobil Prisindeks til indlejring på andre sider. Se hele prisudviklingen på mobilabonnementer på telemobil.dk/prisudvikling."><link rel="canonical" href="{domaene}/prisudvikling/">
<style>body{{margin:0;padding:14px 16px;font-family:Georgia,serif;color:#1A1A1A;background:#fff}}
h1{{font-size:18px;margin:0 0 2px}}p{{margin:0 0 8px;font:13px/1.4 system-ui,sans-serif;color:#666}}
svg{{width:100%;height:auto;display:block}}a{{color:#1A1A1A}}</style></head><body>
<h1>{rubrik(R).replace("&nbsp;", " ")}</h1><p>Telemobil Prisindeks · {d_lang(R["start"])} = 100 · opdateret {d_lang(R["slut"])}</p>
{graf_svg(R)}
<p>Kilde: <a href="{domaene}/prisudvikling/" target="_blank" rel="noopener">Telemobil Prisindeks</a></p>
</body></html>"""
    with open(os.path.join(mappe, "embed.html"), "w", encoding="utf-8") as f:
        f.write(embed)


def dataset_ld(R, domaene, besk):
    return {"@type": "Dataset", "@id": domaene + "/prisudvikling/#dataset",
            "name": "Telemobil Prisindeks — prisudvikling på danske mobilabonnementer",
            "description": besk, "url": domaene + "/prisudvikling/", "inLanguage": "da-DK",
            "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True,
            "creator": {"@id": domaene + "/#organisation"},
            "temporalCoverage": f'{R["start"]}/{R["slut"]}', "spatialCoverage": "Danmark",
            "variableMeasured": ["Prisindeks (matched model)", "Medianpris pr. måned i kr."],
            "measurementTechnique": "Priser hentet to gange dagligt; kædet geometrisk indeks over "
                                    "identiske abonnementer.",
            "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv",
                              "contentUrl": domaene + "/prisudvikling/telemobil-prisindeks.csv"}]}


KOPI_JS = """<script>document.addEventListener('click',function(ev){var b=ev.target.closest('[data-kopier]');
if(!b)return;var t=b.getAttribute('data-kopier');if(t.charAt(0)==='#'){t=document.querySelector(t).textContent.trim()}
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){var o=b.textContent;
b.textContent='Kopieret';setTimeout(function(){b.textContent=o},1600)}).catch(function(){prompt('Kopiér:',t)})});</script>"""
