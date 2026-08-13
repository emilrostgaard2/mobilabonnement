import re
# -*- coding: utf-8 -*-
"""Skabelonlag for telemobil.dk — HTML-shell, navigation og genbrugelige komponenter."""

import json
import html

DOMAENE = "https://telemobil.dk"
SITENAVN = "Telemobil"

FORFATTER = {
    "navn": "Emil Rostgaard",
    "rolle": "Stifter og redaktør, Telemobil",
    "linkedin": "https://www.linkedin.com/in/emil-rostgaard-702809195/",
    "billede": "/assets/img/emil-rostgaard.webp",
    "bio": ("Emil Rostgaard har arbejdet med digitale sammenligningstjenester og "
            "forbrugerøkonomi siden 2018 og står bag flere danske prisportaler. Han "
            "gennemgår selv udbydernes produktvilkår og står bag den metode, "
            "Telemobils tabeller bygger på."),
}

SAMMENLIGN = [
    ("/billigste-mobilabonnement/", "Billigste mobilabonnement", "Hele markedet sorteret efter pris"),
    ("/bedste-mobilabonnement/", "Bedste mobilabonnement", "Bedst samlet værdi, ikke bare lavest pris"),
    ("/mobilabonnement-med-fri-data/", "Fri data", "Ubegrænset data i Danmark"),
    ("/mobilabonnement-med-fri-tale/", "Fri tale", "Ubegrænsede opkald og sms"),
    ("/mobilabonnement-uden-data/", "Uden data", "Kun tale og sms"),
    ("/mobilabonnement-med-streaming/", "Med streaming", "Netflix og co. i abonnementet"),
    ("/mobilabonnement-med-esim/", "Med eSIM", "Digitalt simkort, klar samme dag"),
    ("/mobilabonnement-til-boern/", "Til børn", "Trygt, billigt og uden overraskelser"),
    ("/mobilabonnement-til-unge/", "Til unge og studerende", "Meget data, ingen binding"),
    ("/mobilabonnement-uden-binding/", "Uden binding", "Opsig når du vil"),
    ("/mobilabonnement-med-streaming/tjenester/", "Streaming: vælg tjeneste",
     "Netflix, HBO Max, Disney+, Viaplay …"),
    ("/netvaerk/", "Mobilnetværk", "TDC NET, Telenor og 3"),
    ("/landekoder/", "Landekoder", "Alle telefonkoder med søgning"),
    ("/hvem-ringer-til-mig/", "Hvem ringer til mig?", "Slå ukendt nummer op"),
]

MENU = [
    ("/billigste-mobilabonnement/", "Billigste abonnement"),
    ("/bedste-mobilabonnement/", "Bedste abonnement"),
    ("/guides/", "Guides"),
    ("/om-os/", "Om os"),
]


NAV_UDBYDERE = []


def e(t):
    """Escaper tekst til HTML."""
    return html.escape(str(t), quote=True)


def kr(v):
    """Formaterer et kronebeløb dansk."""
    return f"{v:,.0f}".replace(",", ".")


def gb_tekst(gb):
    if gb >= 900:
        return "Fri data"
    return f"{gb} GB" if gb > 0 else "Ingen data"


def gns12(a):
    """Reel gennemsnitspris pr. md. over 12 mdr. inkl. intropris og oprettelse."""
    if a.get("forbrugsafregnet"):
        return None
    m = min(a.get("intro_mdr") or 0, 12)
    ip = a.get("intro_pris")
    total = (ip * m if (ip is not None and m) else 0) + a["pris"] * (12 - m)
    return (total + a.get("oprettelse", 0)) / 12


def netlabel(u):
    """Kort netværksetiket til tabeller. MVNO = udbyder uden eget net."""
    n = u.get("netvaerk", "")
    if n in ("", "MVNO", "Se udbyder"):
        return "MVNO"
    if n == "3":
        return "Nettet fra 3"
    return f"{e(n)}-nettet" if n == "TDC NET" else f"{e(n)}s net"


# ---------------------------------------------------------------- HTML-shell

def indholdsfortegnelse(html, minimum=4):
    """Bygger ToC af H2'er og giver dem id, så de kan linkes til."""
    fundne = re.findall(r"<h2>(.*?)</h2>", html, re.S)
    rene = []
    for f in fundne:
        t = re.sub(r"<[^>]+>", "", f).strip()
        if t and t not in rene:
            rene.append(t)
    if len(rene) < minimum:
        return html, ""

    def slug(t):
        s = t.lower()
        for a, b in (("æ", "ae"), ("ø", "oe"), ("å", "aa"), ("é", "e")):
            s = s.replace(a, b)
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s[:60]

    brugte = {}
    for t in rene:
        s = slug(t)
        brugte[t] = s
        html = html.replace(f"<h2>{t}</h2>", f'<h2 id="{s}">{t}</h2>', 1)

    punkter = "".join(f'<li><a href="#{brugte[t]}">{e(t)}</a></li>' for t in rene)
    toc = f'''<nav class="toc" aria-label="Indhold">
  <div class="toc-titel">Indhold på siden</div>
  <ol>{punkter}</ol>
</nav>'''
    return html, toc


def laesetid(html):
    tekst = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", html, flags=re.S))
    return max(1, round(len(tekst.split()) / 200))


def shell(*, sti, titel, beskrivelse, indhold, jsonld=None, krumme=None,
          hero=None, efter_hero="", opdateret="", ekstra_hoved=""):
    indhold, toc = indholdsfortegnelse(indhold)
    if toc:
        indhold = indhold.replace('<section class="sektion baand-smal artikel">',
                                  f'<section class="sektion baand-smal">{toc}</section>'
                                  '<section class="sektion baand-smal artikel">', 1)
    minutter = laesetid(indhold)
    """Bygger en komplet HTML-side."""
    kanonisk = DOMAENE + sti
    blokke = ""
    for blok in (jsonld or []):
        blokke += ('<script type="application/ld+json">'
                   + json.dumps(blok, ensure_ascii=False, separators=(",", ":"))
                   + "</script>\n")

    def aktiv(href):
        return ' aria-current="page"' if sti == href else ""

    sammenlign_punkter = "".join(
        f'<a href="{h}"{aktiv(h)}><span class="mp-navn">{e(t)}</span>'
        f'<span class="mp-under">{e(b)}</span></a>'
        for h, t, b in SAMMENLIGN
    )
    udbyder_punkter = "".join(
        f'<a href="/udbydere/{u["slug"]}/"{aktiv("/udbydere/" + u["slug"] + "/")}>'
        f'<img src="/assets/img/logoer/{u["logo"]}" alt="" loading="lazy" height="18">'
        f'<span>{e(u["navn"])}</span></a>'
        for u in NAV_UDBYDERE
    )

    navpunkter = f'''
<div class="nav-gruppe">
  <button type="button" class="nav-knap" aria-expanded="false" aria-controls="menu-sammenlign">
    Sammenlign <span class="pil-ned" aria-hidden="true"></span>
  </button>
  <div class="nav-menu nav-menu-liste" id="menu-sammenlign">{sammenlign_punkter}</div>
</div>
<div class="nav-gruppe">
  <button type="button" class="nav-knap" aria-expanded="false" aria-controls="menu-udbydere">
    Udbydere <span class="pil-ned" aria-hidden="true"></span>
  </button>
  <div class="nav-menu nav-menu-logoer" id="menu-udbydere">
    {udbyder_punkter}
    <a href="/udbydere/" class="nav-alle">Se alle udbydere og anmeldelser →</a>
  </div>
</div>'''
    for href, tekst in MENU:
        if href in ("/billigste-mobilabonnement/", "/bedste-mobilabonnement/"):
            continue
        a = ' aria-current="page"' if sti == href or (href != "/" and sti.startswith(href)) else ""
        navpunkter += f'<a href="{href}"{a}>{e(tekst)}</a>'
    navpunkter += '<a href="/billigste-mobilabonnement/" class="nav-cta">Se priser</a>'

    krummehtml = ""
    if krumme:
        led = ""
        for i, (href, tekst) in enumerate(krumme):
            if href and i < len(krumme) - 1:
                led += f'<li><a href="{href}">{e(tekst)}</a></li>'
            else:
                led += f'<li>{e(tekst)}</li>'
        krummehtml = f'<nav class="krumme baand" aria-label="Brødkrumme"><ol>{led}</ol></nav>'

    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beskrivelse)}">
<link rel="canonical" href="{kanonisk}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="author" content="{e(FORFATTER['navn'])}">
<meta name="twitter:label1" content="Estimeret læsetid">
<meta name="twitter:data1" content="{minutter} minutter">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="geo.region" content="DK">
<meta name="geo.placename" content="Danmark">
<meta property="og:type" content="website">
<meta property="og:locale" content="da_DK">
<meta property="og:site_name" content="{SITENAVN}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beskrivelse)}">
<meta property="og:url" content="{kanonisk}">
<meta property="og:image" content="{DOMAENE}/assets/img/telemobil-social.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titel)}">
<meta name="twitter:description" content="{e(beskrivelse)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0B1026">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400..700&display=swap">
<script>document.documentElement.className+=" js";</script>
<link rel="stylesheet" href="/assets/css/telemobil.css">
{ekstra_hoved}
{blokke}</head>
<body>
<a class="spring" href="#indhold">Spring til indhold</a>

<div class="topstribe">
  <div class="baand">
    <span><i class="prik"></i> Priser opdateret {e(opdateret)}</span>
    <span>Uafhængig sammenligning</span>
    <span>Ingen binding på 9 ud af 10 abonnementer</span>
  </div>
</div>

<header class="hoved">
  <div class="baand">
    <a href="/" class="logo" aria-label="Telemobil forside">
      <span class="logo-maerke" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <span class="logo-tekst">Tele<em>mobil</em></span>
    </a>
    <button class="burger" aria-label="Åbn menu" aria-expanded="false" aria-controls="hovedmenu">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="hovedmenu" aria-label="Hovedmenu">{navpunkter}</nav>
  </div>
</header>

{hero or ''}
{efter_hero}
{krummehtml}

<main id="indhold">
{indhold}
</main>

{fod(opdateret)}
<script src="/assets/js/telemobil.js" defer></script>
</body>
</html>
"""


def fod(opdateret):
    return f"""<footer class="fod">
  <div class="baand">
    <div class="fod-gitter">
      <div>
        <a href="/" class="logo">
          <span class="logo-maerke" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
          <span class="logo-tekst">Tele<em>mobil</em></span>
        </a>
        <p>Uafhængig dansk sammenligning af mobilabonnementer. Vi gennemgår udbydernes
        vilkår, regner priserne igennem og skriver, hvad vi finder — også når det ikke
        passer udbyderne.</p>
        <p style="font-size:.84rem">Senest opdateret {e(opdateret)}</p>
      </div>
      <div>
        <div class="fodtitel">Sammenlign</div>
        <ul>
          <li><a href="/billigste-mobilabonnement/">Billigste mobilabonnement</a></li>
          <li><a href="/bedste-mobilabonnement/">Bedste mobilabonnement</a></li>
          <li><a href="/mobilabonnement-med-fri-data/">Fri data</a></li>
          <li><a href="/mobilabonnement-med-fri-tale/">Fri tale</a></li>
          <li><a href="/mobilabonnement-uden-data/">Uden data</a></li>
          <li><a href="/mobilabonnement-med-streaming/">Med streaming</a></li>
          <li><a href="/mobilabonnement-med-esim/">Med eSIM</a></li>
          <li><a href="/mobilabonnement-til-boern/">Til børn</a></li>
          <li><a href="/mobilabonnement-til-unge/">Til unge og studerende</a></li>
          <li><a href="/mobilabonnement-uden-binding/">Uden binding</a></li>
          <li><a href="/mobilabonnement-med-streaming/tjenester/">Streaming pr. tjeneste</a></li>
          <li><a href="/netvaerk/">Mobilnetværk</a></li>
          <li><a href="/udbydere/">Alle udbydere</a></li>
        </ul>
      </div>
      <div>
        <div class="fodtitel">Guides</div>
        <ul>
          <li><a href="/guides/skift-mobilselskab/">Skift mobilselskab</a></li>
          <li><a href="/guides/hvor-meget-data/">Hvor meget data?</a></li>
          <li><a href="/guides/daekning-og-netvaerk/">Dækning og netværk</a></li>
          <li><a href="/guides/esim/">eSIM forklaret</a></li>
          <li><a href="/guides/">Alle guides</a></li>
          <li><a href="/landekoder/">Landekoder</a></li>
          <li><a href="/hvem-ringer-til-mig/">Hvem ringer til mig?</a></li>
        </ul>
      </div>
      <div>
        <div class="fodtitel">Om Telemobil</div>
        <ul>
          <li><a href="/om-os/">Om os</a></li>
          <li><a href="/om/emil-rostgaard/">Emil Rostgaard</a></li>
          <li><a href="/saadan-tjener-vi-penge/">Sådan tjener vi penge</a></li>
          <li><a href="/metode/">Vores metode</a></li>
          <li><a href="/kontakt/">Kontakt</a></li>
          <li><a href="/presse/">Presse</a></li>
          <li><a href="/privatlivspolitik/">Privatlivspolitik</a></li>
          <li><a href="/cookiepolitik/">Cookiepolitik</a></li>
        </ul>
      </div>
    </div>
    <div class="fod-bund">
      <span>© {opdateret[-4:] or '2026'} Telemobil. Priser er vejledende og kan ændre sig.</span>
      <span>Telemobil modtager provision fra udvalgte udbydere. <a href="/saadan-tjener-vi-penge/">Læs hvordan</a>.</span>
    </div>
  </div>
</footer>"""


# ---------------------------------------------------------------- Komponenter

def afsloering(kort=False):
    if kort:
        return ('<p class="afsloering"><strong>Sådan tjener vi penge:</strong> Telemobil '
                'modtager provision, når du bestiller via vores links. Det påvirker ikke '
                'rækkefølgen i tabellerne, som altid sorteres efter pris. '
                '<a href="/saadan-tjener-vi-penge/">Læs mere</a>.</p>')
    return ('<p class="afsloering"><strong>Annoncørinformation:</strong> Telemobil er gratis at '
            'bruge. Vi modtager provision fra udvalgte udbydere, når du klikker videre og '
            'bestiller. Det koster dig ikke ekstra, og det ændrer ikke sorteringen i vores '
            'tabeller, som altid er efter pris. Udbydere kan ikke betale sig til en bedre '
            'placering eller en bedre omtale. <a href="/saadan-tjener-vi-penge/">Se hele '
            'forretningsmodellen</a>.</p>')


def forfatterboks(gennemgået=None):
    f = FORFATTER
    return f"""<aside class="forfatter">
  <img src="{f['billede']}" width="88" height="88" alt="{e(f['navn'])}, stifter af Telemobil" loading="lazy">
  <div>
    <h3>{e(f['navn'])}</h3>
    <div class="rolle">{e(f['rolle'])}</div>
    <p>{e(f['bio'])}</p>
    <div class="links">
      <a href="/om/emil-rostgaard/">Om forfatteren</a>
      <a href="{f['linkedin']}" rel="noopener nofollow" target="_blank">LinkedIn</a>
      <a href="/metode/">Sådan tester vi</a>
    </div>
  </div>
</aside>"""


def gennemgangslinje(opdateret, fakta="Alle priser kontrolleret mod udbydernes egne sider"):
    return f"""<div class="gennemgang">
  <span>Skrevet af <b>{e(FORFATTER['navn'])}</b></span>
  <span>Opdateret <b>{e(opdateret)}</b></span>
  <span>{e(fakta)}</span>
</div>"""


def faqblok(sporgsmaal, overskrift="Ofte stillede spørgsmål"):
    dele = "".join(
        f"<details><summary>{e(s['sp'])}</summary><p>{e(s['sv'])}</p></details>"
        for s in sporgsmaal
    )
    return f"""<section class="sektion baand-smal">
  <h2>{e(overskrift)}</h2>
  <div class="faq">{dele}</div>
</section>"""


def laesvidere(links, overskrift="Læs videre"):
    punkter = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in links)
    return f"""<aside class="laesvidere">
  <h3>{e(overskrift)}</h3>
  <ul>{punkter}</ul>
</aside>"""


def ctabaand(titel, tekst, knaptekst="Sammenlign alle abonnementer", href="/billigste-mobilabonnement/"):
    return f"""<section class="sektion baand">
  <div class="ctabaand afslør">
    <h2>{e(titel)}</h2>
    <p>{e(tekst)}</p>
    <a href="{href}" class="knap knap-puls">{e(knaptekst)}</a>
  </div>
</section>"""


# ---------------------------------------------------------------- Tabel

def beregn_maerker(abonnementer):
    """Udpeger hvad hvert abonnement er bedst til — relativt til de viste."""
    m = {}
    def saet(a, tekst, klasse):
        if a:
            m.setdefault(a["id"], [])
            if len(m[a["id"]]) < 2:
                m[a["id"]].append((tekst, klasse))

    betalte = [a for a in abonnementer if a["pris"] > 0 and not a.get("forbrugsafregnet")]
    med_data = [a for a in betalte if a["data_gb"] > 0]
    endelig = [a for a in med_data if a["data_gb"] < 900]
    frie = [a for a in betalte if a["data_gb"] >= 900]

    if betalte:
        saet(min(betalte, key=lambda a: a["pris"]), "Billigst i alt", "puls")
    if endelig:
        saet(min(endelig, key=lambda a: a["pris"] / a["data_gb"]), "Bedste pris pr. GB", "puls")
        saet(max(endelig, key=lambda a: a["data_gb"]), "Mest data", "signal")
    if frie:
        saet(min(frie, key=lambda a: a["pris"]), "Billigste fri data", "signal")
    if med_data:
        saet(max(med_data, key=lambda a: a.get("eu_gb", 0)), "Flest EU-data", "berry")
        saet(min(med_data, key=lambda a: gns12(a) or 9e9), "Lavest over 12 mdr.", "puls")
    intro = [a for a in betalte if a.get("intro_pris") is not None and a.get("intro_mdr")]
    if intro:
        saet(max(intro, key=lambda a: a["intro_mdr"]), "Længst introperiode", "sol")
    stream = [a for a in betalte if a.get("streaming")]
    if stream:
        saet(max(stream, key=lambda a: len(a["streaming"])), "Flest tjenester", "sol")
    return m


def prisrække(a, u, billigst_pr_gb=False, gnsnit_aar=None, dyn=None):
    """Ét abonnement som rækkekort."""
    logo = f"/assets/img/logoer/{u['logo']}"
    forbrug = a.get("forbrugsafregnet")
    pr_gb = a["pris"] / a["data_gb"] if 0 < a["data_gb"] < 900 else 0
    pr_gb_tekst = (f"{pr_gb:.2f}".replace(".", ",") + " kr.") if pr_gb else "—"
    g = gns12(a)
    aar = (g * 12) if g is not None else 0

    # Mærkater — dynamiske først, så det mest øjenfangende står forrest
    maerker = ""
    for tekst, klasse in (dyn or {}).get(a["id"], []):
        maerker += f'<span class="mrk mrk-{klasse}">{e(tekst)}</span>'
    if a.get("intro_pris") is not None and a.get("intro_mdr"):
        maerker += f'<span class="mrk mrk-sol">Tilbud i {a["intro_mdr"]} mdr.</span>'
    if a.get("streaming"):
        n = len(a["streaming"])
        maerker += f'<span class="mrk mrk-berry">{n} streamingtjeneste{"r" if n > 1 else ""}</span>'

    # Statbokse
    stats = [
        (gb_tekst(a["data_gb"]), "data i DK"),
        ("Fri" if a["tale"] == "fri" else e(a["tale"]), "tale"),
        ("—" if a["data_gb"] == 0 else ("Fri" if a.get("eu_gb", 0) >= 900 else f'{a.get("eu_gb", 0)} GB'), "EU-data"),
        (pr_gb_tekst, "pris pr. GB"),
    ]
    statbokse = "".join(f'<div class="stat"><b>{v}</b><span>{t}</span></div>' for v, t in stats)

    # Chips
    chips = ['<span class="chp">Ingen binding</span>' if a["binding"] == 0
             else f'<span class="chp chp-advar">{a["binding"]} mdr. binding</span>']
    if a.get("oprettelse", 0) == 0:
        chips.append('<span class="chp">0 kr. i oprettelse</span>')
    if a.get("esim"):
        chips.append('<span class="chp">eSIM samme dag</span>')
    if a.get("streaming"):
        chips.append('<span class="chp">' + e(", ".join(a["streaming"][:3]))
                     + ("…" if len(a["streaming"]) > 3 else "") + "</span>")

    # Prisblok
    if forbrug:
        prisblok = ('<div class="p-tal"><b>0</b><span>kr./md.</span></div>'
                    '<div class="p-normal">+ takst pr. minut og sms</div>'
                    '<div class="p-gns">Du betaler kun for det, du bruger</div>')
    elif a.get("intro_pris") is not None and a.get("intro_mdr"):
        prisblok = (f'<div class="p-intro">Tilbud i {a["intro_mdr"]} mdr.</div>'
                    f'<div class="p-tal"><b>{kr(a["intro_pris"])}</b><span>kr./md.</span></div>'
                    f'<div class="p-normal">Normalpris {kr(a["pris"])} kr./md.</div>'
                    f'<div class="p-gns">Gns. <strong>{kr(g)} kr./md.</strong> over 12 mdr.</div>')
    else:
        prisblok = (f'<div class="p-tal"><b>{kr(a["pris"])}</b><span>kr./md.</span></div>'
                    f'<div class="p-gns">{kr(aar)} kr. samlet på 12 mdr.</div>')

    spar = ""
    if gnsnit_aar and not forbrug and aar < gnsnit_aar:
        spar = (f'<div class="p-spar">{kr((gnsnit_aar - aar) / 12)} kr./md. '
                "under gennemsnittet</div>")

    klasse = " fremhaev" if billigst_pr_gb else ""
    return f"""<article class="plan{klasse}" data-gb="{a['data_gb']}" data-pris="{a['pris']}"
  data-prgb="{pr_gb:.4f}" data-aar="{aar:.0f}" data-udbyder="{e(u['navn'])}">
  <div class="plan-ident">
    <img src="{logo}" alt="{e(u['navn'])} logo" loading="lazy" height="26">
    <div class="plan-net">
      {'<span class="netbadge">5G</span>' if a.get("femg") and a["data_gb"] > 0 else ''}
      <span class="netnavn">{netlabel(u)}</span>
    </div>
  </div>
  <div class="plan-midt">
    <div class="plan-mrk">{maerker}</div>
    <h3 class="plan-navn">{e(a['navn'])}</h3>
    <div class="plan-stats">{statbokse}</div>
    <div class="plan-chips">{"".join(chips)}</div>
  </div>
  <div class="plan-pris">
    {prisblok}
    {spar}
    <a class="knap knap-primaer" href="{a['link']}" rel="sponsored nofollow noopener" target="_blank"
       data-udgaaende="{e(u['slug'])}" data-abonnement="{e(a['id'])}"
       aria-label="Se tilbud på {e(a['navn'])} hos {e(u['navn'])}">Se tilbud <span aria-hidden="true">→</span></a>
    <a class="p-laes" href="/udbydere/{u['slug']}/">Læs mere om {e(u['navn'])} →</a>
    <small class="p-hos">Annoncelink · vi kan modtage provision</small>
  </div>
</article>"""


def pristabel(abonnementer, udbydere_map, *, titel, undertitel, filtre=True,
              billigst_id=None, id_attr="sammenlign", vis=10):
    betalte = [gns12(x) for x in abonnementer if x["pris"] > 0 and not x.get("forbrugsafregnet")]
    betalte = [x for x in betalte if x]
    gnsnit_aar = (sum(betalte) / len(betalte) * 12) if betalte else None

    dyn = beregn_maerker(abonnementer)
    kort = ""
    for i, a in enumerate(abonnementer):
        u = udbydere_map[a["udbyder"]]
        r = prisrække(a, u, billigst_pr_gb=(a["id"] == billigst_id),
                      gnsnit_aar=gnsnit_aar, dyn=dyn)
        if vis and i >= vis:
            r = r.replace('<article class="plan', '<article hidden class="plan', 1)
        kort += r

    resten = max(0, len(abonnementer) - vis) if vis else 0
    visflere = ""
    if resten:
        visflere = (f'<div class="vis-flere">'
                    f'<button type="button" class="knap knap-linje" data-vis-flere>'
                    f'Vis {min(10, resten)} abonnementer mere</button>'
                    f'<small data-resterende>{resten} abonnementer tilbage</small></div>')

    filterhtml = ""
    if filtre:
        filterhtml = """<div class="filterpanel">
  <div class="fp-raekke">
    <span class="fp-titel">Datamængde</span>
    <div class="fp-valg">
      <button class="chip" data-filter="alle" aria-pressed="true">Alle</button>
      <button class="chip" data-filter="lille" aria-pressed="false">Op til 15 GB</button>
      <button class="chip" data-filter="mellem" aria-pressed="false">15–50 GB</button>
      <button class="chip" data-filter="stor" aria-pressed="false">Over 50 GB</button>
      <button class="chip" data-filter="fri" aria-pressed="false">Fri data</button>
    </div>
  </div>
  <div class="fp-raekke">
    <span class="fp-titel">Pris pr. md.</span>
    <div class="fp-valg">
      <button class="chip" data-pris="alle" aria-pressed="true">Alle</button>
      <button class="chip" data-pris="u50" aria-pressed="false">Under 50 kr.</button>
      <button class="chip" data-pris="50-99" aria-pressed="false">50–99 kr.</button>
      <button class="chip" data-pris="100-199" aria-pressed="false">100–199 kr.</button>
      <button class="chip" data-pris="o200" aria-pressed="false">Over 200 kr.</button>
    </div>
  </div>
  <div class="fp-raekke fp-sort">
    <span class="fp-titel">Sortér efter</span>
    <div class="fp-valg">
      <button class="chip chip-sort" data-sorter="pris" aria-pressed="true">Laveste pris</button>
      <button class="chip chip-sort" data-sorter="aar" aria-pressed="false">Gns. 12 mdr.</button>
      <button class="chip chip-sort" data-sorter="prgb" aria-pressed="false">Pris pr. GB</button>
      <button class="chip chip-sort" data-sorter="gb" aria-pressed="false">Mest data</button>
    </div>
    <span class="fp-antal"><span data-antal-vist>ANTAL</span> abonnementer</span>
  </div>
</div>"""
        filterhtml = filterhtml.replace("ANTAL", str(len(abonnementer)))

    return f"""<section class="sektion baand" id="{id_attr}">
  <div class="sektion-hoved afslør">
    <span class="etiket">Sammenligning</span>
    <h2>{e(titel)}</h2>
    <p class="led">{undertitel}</p>
  </div>
  {filterhtml}
  <div class="listeramme afslør">
    <div class="planliste">{kort}</div>
    {visflere}
    <div class="listefod">
      <span>Sorteret efter laveste månedspris. <strong>Gns. 12 mdr.</strong> regner intropris,
      normalpris og oprettelse sammen — det er den reelle pris.</span>
      <span>Kilde: udbydernes egne prislister</span>
    </div>
  </div>
  {afsloering(kort=True)}
</section>"""
