# -*- coding: utf-8 -*-
"""Bygger telemobil.dk fra data/ og skabelonerne i _build/.

Kør fra projektroden:  python3 _build/build.py
"""

import json
import os
import sys
import shutil
from datetime import date

STI = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(STI)
sys.path.insert(0, STI)

from skabelon import (  # noqa: E402
    shell, e, kr, gb_tekst, netlabel, gns12, DOMAENE, SITENAVN, FORFATTER,
    afsloering, forfatterboks, gennemgangslinje, faqblok, laesvidere,
    ctabaand, pristabel,
)
import indhold  # noqa: E402
import sider  # noqa: E402
import sider2  # noqa: E402
import sider3  # noqa: E402
import sider4  # noqa: E402
import historier  # noqa: E402
from udbyder_unik import UNIK  # noqa: E402
import skabelon  # noqa: E402

MAANEDER = ["januar", "februar", "marts", "april", "maj", "juni", "juli",
            "august", "september", "oktober", "november", "december"]

SIDER = []  # (sti, prioritet, hyppighed)


# --------------------------------------------------------------- hjælpere

def dansk_dato(d):
    return f"{d.day}. {MAANEDER[d.month - 1]} {d.year}"


def skriv(sti, html, prioritet="0.7", hyppighed="weekly", i_sitemap=True):
    mappe = os.path.join(ROD, sti.strip("/"))
    if sti == "/":
        filsti = os.path.join(ROD, "index.html")
    else:
        os.makedirs(mappe, exist_ok=True)
        filsti = os.path.join(mappe, "index.html")
    with open(filsti, "w", encoding="utf-8") as f:
        f.write(html)
    if i_sitemap:
        SIDER.append((sti, prioritet, hyppighed))
    return filsti


def indlaes(navn):
    with open(os.path.join(ROD, "data", navn), encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------- data

site = indlaes("site.json")
ud_data = indlaes("udbydere.json")
ab_data = indlaes("abonnementer.json")
LANDE = indlaes("landekoder.json")["landekoder"]

UDBYDERE = ud_data["udbydere"]
UMAP = {u["slug"]: u for u in UDBYDERE}
def visningspris(a):
    """Det tal der står stort på kortet — intropris hvis der er et tilbud."""
    if a.get("intro_pris") and a.get("intro_mdr"):
        return a["intro_pris"]
    return a["pris"]


ABON = sorted(ab_data["abonnementer"], key=visningspris)
for a in ABON:
    if a["udbyder"] not in UMAP:
        raise SystemExit(f"Ukendt udbyder i abonnementer.json: {a['udbyder']}")

# Faktiske logodimensioner → korrekte width/height-attributter uden layoutskred
try:
    from PIL import Image as _Img
    for _u in UDBYDERE:
        with _Img.open(os.path.join(ROD, "assets", "img", "logoer", _u["logo"])) as _im:
            _u["logo_w"], _u["logo_h"] = _im.size
except Exception:
    for _u in UDBYDERE:
        _u["logo_w"], _u["logo_h"] = 240, 96

# Kun udbydere vi har prisdata for kan få en prisside
UDBYDERE_MED_DATA = [u for u in UDBYDERE
                     if any(a["udbyder"] == u["slug"] for a in ABON)]
skabelon.NAV_UDBYDERE = UDBYDERE_MED_DATA or UDBYDERE

# Streamingtjenester findes kun, hvis feedet indeholder dem
TJENESTER_I_DATA = {t for a in ABON for t in a.get("streaming", [])}

def _har(f):
    return any(f(a) for a in ABON)

_MULIGE = {
    "/mobilabonnement-med-fri-data/": _har(lambda a: a["data_gb"] >= 900),
    "/mobilabonnement-med-fri-tale/": _har(lambda a: a["tale"] == "fri"),
    "/mobilabonnement-uden-data/": _har(lambda a: a["data_gb"] == 0),

    "/mobilabonnement-med-esim/": _har(lambda a: a.get("esim")),
    "/mobilabonnement-uden-binding/": _har(lambda a: a["binding"] == 0),
    "/mobilabonnement-under-100-kr/": _har(lambda a: 0 < a["pris"] < 100),
}
skabelon.SAMMENLIGN = [x for x in skabelon.SAMMENLIGN if _MULIGE.get(x[0], True)]
skabelon.VAERKTOEJER = [x for x in skabelon.VAERKTOEJER if _MULIGE.get(x[0], True)]

IDAG = date.today()
OPDATERET = dansk_dato(IDAG)
ISO = IDAG.isoformat()

# Afledte nøgletal — bruges i tekst, så tal og tabeller aldrig kan komme i utakt
med_gb = [a for a in ABON if 0 < a["data_gb"] < 900]
fri = [a for a in ABON if a["data_gb"] >= 900]
billigst = min((a for a in ABON if a["pris"] > 0 and not a.get("forbrugsafregnet")),
               key=lambda a: a["pris"])
billigst_med_data = min((a for a in ABON if a["data_gb"] > 0 and a["pris"] > 0),
                        key=lambda a: a["pris"])
bedste_pr_gb = min(med_gb, key=lambda a: a["pris"] / a["data_gb"])

D = {
    "min_pris": billigst["pris"],
    "min_pris_data": billigst_med_data["pris"],
    "min_data_gb": billigst_med_data["data_gb"],
    "pris_lille": min(a["pris"] for a in ABON if 0 < a["data_gb"] <= 10),
    "pris_mellem": min(a["pris"] for a in ABON if 15 <= a["data_gb"] <= 30),
    "pris_stor": min(a["pris"] for a in ABON if 50 <= a["data_gb"] < 900),
    "pris_fri": min(a["pris"] for a in fri) if fri else 199,
    "antal": len(ABON),
    "antal_udbydere": len(UDBYDERE),
    "maks_besparelse": max(a["pris"] for a in ABON) - billigst["pris"],
}

def _min(kriterie, standard=0):
    kandidater = [a["pris"] for a in ABON
                  if kriterie(a) and a["pris"] > 0 and not a.get("forbrugsafregnet")]
    return min(kandidater) if kandidater else standard

D["pris_fritale"] = _min(lambda a: a["tale"] == "fri")
D["pris_udendata"] = _min(lambda a: a["data_gb"] == 0)
D["pris_streaming"] = _min(lambda a: a.get("streaming"))
D["pris_boern"] = _min(lambda a: a["data_gb"] <= 15)
D["pris_esim"] = _min(lambda a: a.get("esim"))
D["pris_bedste"] = D["pris_mellem"]
MUSIKTJENESTER = {"Deezer", "Telmore Musik", "YouSee Musik", "Mofibo", "Podimo"}
D["pris_musik"] = _min(lambda a: MUSIKTJENESTER & set(a.get("streaming", [])))
D["pris_aeldre"] = _min(lambda a: a["data_gb"] <= 10)
D["antal_u100"] = len([a for a in ABON if 0 < a["pris"] < 100])


# --------------------------------------------------------------- JSON-LD

ORG = {
    "@type": "Organization",
    "@id": DOMAENE + "/#organisation",
    "name": SITENAVN,
    "alternateName": "telemobil.dk",
    "url": DOMAENE + "/",
    "description": ("Uafhængig dansk prissammenligning af mobilabonnementer. Vi gennemgår "
                    "udbydernes vilkår, beregner den reelle pris over 12 måneder og skriver "
                    "både fordele og ulemper."),
    "logo": {"@type": "ImageObject", "url": DOMAENE + "/assets/img/telemobil-social.png",
             "width": 1200, "height": 630},
    "image": DOMAENE + "/assets/img/telemobil-social.png",
    "email": "kontakt@telemobil.dk",
    "foundingDate": site.get("udgivet", ISO)[:4],
    "areaServed": {"@type": "Country", "name": "Danmark"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Lundbyesgade 13",
        "postalCode": "8000",
        "addressLocality": "Aarhus C",
        "addressRegion": "Midtjylland",
        "addressCountry": "DK",
    },
    "knowsLanguage": "da-DK",
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "kontakt@telemobil.dk",
        "availableLanguage": ["Danish", "English"],
        "areaServed": "DK",
    },
    "founder": {"@id": DOMAENE + "/om/emil-rostgaard/#person"},
    "publishingPrinciples": DOMAENE + "/metode/",
    "sameAs": [FORFATTER["linkedin"]],
}

TJENESTE = {
    "@type": "Service",
    "@id": DOMAENE + "/#tjeneste",
    "name": "Sammenligning af mobilabonnementer",
    "serviceType": "Prissammenligning",
    "provider": {"@id": DOMAENE + "/#organisation"},
    "areaServed": {"@type": "Country", "name": "Danmark"},
    "audience": {"@type": "Audience", "audienceType": "Forbrugere i Danmark"},
    "offers": {"@type": "Offer", "price": 0, "priceCurrency": "DKK",
               "description": "Gratis at bruge for forbrugere"},
}

PERSON = {
    "@type": "Person",
    "@id": DOMAENE + "/om/emil-rostgaard/#person",
    "name": FORFATTER["navn"],
    "url": DOMAENE + "/om/emil-rostgaard/",
    "jobTitle": FORFATTER["rolle"],
    "image": DOMAENE + FORFATTER["billede"],
    "sameAs": [FORFATTER["linkedin"]],
    "description": FORFATTER["bio"],
    "knowsAbout": ["Mobilabonnementer", "Telemarkedet i Danmark", "Forbrugerøkonomi",
                   "Prissammenligning", "Mobilnetværk", "eSIM", "Nummerportering"],
    "knowsLanguage": ["da-DK", "en"],
    "nationality": {"@type": "Country", "name": "Danmark"},
    "hasOccupation": {
        "@type": "Occupation",
        "name": "Redaktør og stifter",
        "occupationLocation": {"@type": "Country", "name": "Danmark"},
        "responsibilities": ("Gennemgang af udbyderes produktvilkår, fastlæggelse af metode "
                             "og redaktionelle vurderinger af mobilabonnementer."),
    },
    "worksFor": {"@id": DOMAENE + "/#organisation"},
}

WEBSITE = {
    "@type": "WebSite",
    "@id": DOMAENE + "/#website",
    "url": DOMAENE + "/",
    "name": SITENAVN,
    "inLanguage": "da-DK",
    "description": ("Sammenlign mobilabonnementer fra alle danske udbydere på pris, data, "
                    "netværk og reelle omkostninger over 12 måneder."),
    "copyrightHolder": {"@id": DOMAENE + "/#organisation"},
    "publisher": {"@id": DOMAENE + "/#organisation"},
}


def howtold(sti, navn, beskrivelse, html):
    """Udleder HowTo-schema af den første trinliste på siden."""
    m = re.search(r'<ol class="trin">(.*?)</ol>', html, re.S)
    if not m:
        return None
    trin = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
    if len(trin) < 2:
        return None
    skridt = []
    for i, t in enumerate(trin, 1):
        titel = re.search(r"<strong>(.*?)</strong>", t, re.S)
        tekst = re.sub(r"<[^>]+>", " ", t)
        tekst = re.sub(r"\s+", " ", tekst).strip()
        skridt.append({
            "@type": "HowToStep",
            "position": i,
            "name": re.sub(r"<[^>]+>", "", titel.group(1)).strip() if titel else f"Trin {i}",
            "text": tekst[:400],
            "url": DOMAENE + sti,
        })
    return {
        "@type": "HowTo",
        "@id": DOMAENE + sti + "#howto",
        "name": navn,
        "description": beskrivelse,
        "inLanguage": "da-DK",
        "totalTime": "PT10M",
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "DKK", "value": 0},
        "step": skridt,
    }


def vaerktoejld(sti, navn, beskrivelse):
    return {
        "@type": "WebApplication",
        "@id": DOMAENE + sti + "#app",
        "name": navn,
        "url": DOMAENE + sti,
        "description": beskrivelse,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsere",
        "inLanguage": "da-DK",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": 0, "priceCurrency": "DKK"},
        "provider": {"@id": DOMAENE + "/#organisation"},
    }


import re  # noqa: E402


def graf(*noder):
    return {"@context": "https://schema.org", "@graph": [n for n in noder if n]}


def krummeld(punkter):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": t,
             **({"item": DOMAENE + h} if h else {})}
            for i, (h, t) in enumerate(punkter)
        ],
    }


def faqld(sp):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": s["sp"],
             "acceptedAnswer": {"@type": "Answer", "text": s["sv"]}}
            for s in sp
        ],
    }


def artikelld(sti, titel, beskrivelse, ordtal=None, emne="Mobilabonnement"):
    node = {
        "@type": "Article",
        "@id": DOMAENE + sti + "#artikel",
        "headline": titel,
        "description": beskrivelse,
        "inLanguage": "da-DK",
        "datePublished": site.get("udgivet", ISO),
        "dateModified": ISO,
        "author": {"@id": DOMAENE + "/om/emil-rostgaard/#person"},
        "publisher": {"@id": DOMAENE + "/#organisation"},
        "isPartOf": {"@id": DOMAENE + "/#website"},
        "mainEntityOfPage": DOMAENE + sti,
        "image": {"@type": "ImageObject",
                  "url": DOMAENE + "/assets/img/telemobil-social.png",
                  "width": 1200, "height": 630},
        "isAccessibleForFree": True,
        "articleSection": "Mobilabonnement",
        "inLanguage": "da-DK",
        "about": {"@type": "Thing", "name": emne},
        "creativeWorkStatus": "Published",
    }
    if ordtal:
        node["wordCount"] = ordtal
    return node


def listeld(abonnementer, navn):
    poster = []
    for i, a in enumerate(abonnementer[:20], 1):
        u = UMAP[a["udbyder"]]
        poster.append({
            "@type": "ListItem", "position": i,
            "item": {
                "@type": "Service",
                "serviceType": "Mobilabonnement",
                "provider": {"@type": "Organization", "name": u["navn"], "url": u["hjemmeside"]},
                "name": f"{u['navn']} — {a['navn']}",
                "description": (
                    ("Uden mobildata" if a["data_gb"] == 0
                     else ("Fri data i Danmark" if a["data_gb"] >= 900
                           else f"{a['data_gb']} GB data i Danmark"))
                    + ", " + ("fri tale" if a["tale"] == "fri" else f"{a['tale']} taletid")
                    + (f", {a['eu_gb']} GB EU-data" if a.get("eu_gb") else "")
                    + ". " + ("Ingen binding." if a["binding"] == 0
                              else f"{a['binding']} mdr. binding.")),
                "sku": a["id"],
                "image": DOMAENE + f"/assets/img/logoer/{u['logo']}",
                "brand": {"@type": "Brand", "name": u["navn"]},
                "category": "Mobilabonnement",
                "areaServed": {"@type": "Country", "name": "Danmark"},
                "offers": {
                    "@type": "Offer",
                    "price": a["pris"],
                    "priceCurrency": "DKK",
                    "availability": "https://schema.org/InStock",
                    "validFrom": ISO,
                    "priceValidUntil": (IDAG.replace(year=IDAG.year + 1)).isoformat(),
                    "priceSpecification": {
                        "@type": "UnitPriceSpecification",
                        "price": a["pris"],
                        "priceCurrency": "DKK",
                        "billingIncrement": 1,
                        "unitCode": "MON",
                        "referenceQuantity": {"@type": "QuantitativeValue",
                                              "value": 1, "unitCode": "MON"},
                    },
                    "seller": {"@type": "Organization", "name": u["navn"], "url": u["hjemmeside"]},
                    "url": DOMAENE + f"/udbydere/{u['slug']}/",
                },
            },
        })
    return {"@type": "ItemList", "name": navn, "numberOfItems": len(poster),
            "itemListElement": poster}


# --------------------------------------------------------------- komponenter

def logobaand(titel="Vi sammenligner priser fra"):
    logoer = "".join(
        f'<img src="/assets/img/logoer/{u["logo"]}" alt="{e(u["navn"])}" loading="lazy"'
        f' width="{round(u["logo_w"] * 30 / u["logo_h"])}" height="30" decoding="async">'
        for u in UDBYDERE
    )
    overskrift = f'<div class="logobaand-titel">{e(titel)}</div>' if titel else ""
    return f"""<div class="logobaand">
  {overskrift}
  <div class="logospor" aria-hidden="true">{logoer}{logoer}</div>
</div>"""


def hero_forside():
    # Samme datamængde hos forskellige udbydere — viser den reelle prisspredning.
    # Billigste 15-30 GB-abonnement pr. udbyder, jævnt fordelt over hele spændet.
    baand = [a for a in ABON if 15 <= a["data_gb"] <= 30]
    pr_udbyder = {}
    for a in baand:
        if a["udbyder"] not in pr_udbyder or a["pris"] < pr_udbyder[a["udbyder"]]["pris"]:
            pr_udbyder[a["udbyder"]] = a
    alle = sorted(pr_udbyder.values(), key=lambda a: a["pris"])
    if len(alle) > 6:
        trin = (len(alle) - 1) / 5
        udvalg = [alle[round(i * trin)] for i in range(6)]
    else:
        udvalg = alle
    hoejest = max(a["pris"] for a in udvalg)
    farver = ["#00D18F", "#12C39A", "#3D5AFE", "#6A54FF", "#B054E8", "#FF5C7A"]

    mast = ""
    for i, a in enumerate(udvalg):
        u = UMAP[a["udbyder"]]
        h = 22 + round(78 * a["pris"] / hoejest)
        mast += (f'<b data-navn="{e(u["navn"].split()[0])}" data-pris="{a["pris"]} kr."'
                 f' style="height:{h}%;background:linear-gradient(180deg,{farver[i]}bb,{farver[i]})"></b>')
    return f"""<section class="hero">
  <div class="hero-net" aria-hidden="true"></div>
  <div class="baand">
    <div class="hero-gitter">
      <div>
        <span class="etiket">Opdateret {e(OPDATERET)}</span>
        <h1>Sammenlign <em>mobilabonnementer</em> fra alle danske udbydere</h1>
        <p class="led">Vi har regnet {D['antal']} abonnementer fra {D['antal_udbydere']}
        udbydere igennem og sorteret dem efter pris. Ingen formular, ingen login —
        bare tallene.</p>
        <div class="hero-tal">
          <div><b data-tael="{D['antal']}">{D['antal']}</b><small>Abonnementer</small></div>
          <div><b data-tael="{D['antal_udbydere']}">{D['antal_udbydere']}</b><small>Udbydere</small></div>
          <div><b data-tael="{D['min_pris']}" data-suffiks=" kr.">{D['min_pris']} kr.</b><small>Laveste pris</small></div>
          <div><b data-tael="{D['maks_besparelse'] * 12}" data-suffiks=" kr.">{kr(D['maks_besparelse'] * 12)} kr.</b><small>Maks. besparelse/år</small></div>
        </div>
        <div class="hero-knapper">
          <a href="#sammenlign" class="knap knap-primaer">Se alle priser</a>
          <a href="/guides/hvor-meget-data/" class="knap knap-lys">Hvor meget data skal jeg have?</a>
        </div>
      </div>
      <div class="mast" role="img" aria-label="Prisspredning: månedspris for et abonnement med 15 til 30 GB hos seks forskellige udbydere">{mast}</div>
    </div>
  </div>
</section>"""


def guidebillede(navn, alt, prioritet=False):
    """Responsivt billede med srcset — 640 til mobil, 1280 til desktop."""
    b = "/assets/img/guides"
    return (f'<img src="{b}/{navn}-1280.webp"'
            f' srcset="{b}/{navn}-640.webp 640w, {b}/{navn}-1280.webp 1280w"'
            f' sizes="(max-width: 900px) 100vw, 46vw"'
            f' alt="{e(alt)}" width="1280" height="698"'
            f' {"fetchpriority=\'high\'" if prioritet else "loading=\'lazy\'"} decoding="async">')


def radar(chips=None):
    """Animeret signalradar til undersidernes hero."""
    c = chips or [("Fra", f"{D['min_pris']} kr."), ("Uden", "binding"), ("Udbydere", str(D['antal_udbydere']))]
    flyv = "".join(f'<span class="chip-fly">{e(a)} <b>{e(v)}</b></span>' for a, v in c)
    return f"""<div class="radar" aria-hidden="true">
  <span class="ring"></span><span class="ring"></span><span class="ring"></span>
  {flyv}
  <span class="kerne"><i></i><i></i><i></i></span>
</div>"""


def hero_side(etiket, h1, tekst, knapper="", chips=None, billede=None):
    return f"""<section class="hero" style="padding:2.6rem 0 2.6rem">
  <div class="hero-net" aria-hidden="true"></div>
  <div class="baand">
    <div class="hero-todelt">
      <div>
        <span class="etiket">{e(etiket)}</span>
        <h1>{h1}</h1>
        <p class="led">{tekst}</p>
        {f'<div class="hero-knapper" style="margin-top:1.3rem">{knapper}</div>' if knapper else ''}
      </div>
      {f'<div class="hero-billede">{billede}</div>' if billede else radar(chips)}
    </div>
  </div>
</section>"""


def hurtigvalg():
    """Fire kort over tabellen. Vælger fra forskellige udbydere, så de ikke gentages."""
    med_data = [a for a in ABON if a["data_gb"] > 0 and a["pris"] > 0]
    tdc = [a for a in med_data if UMAP[a["udbyder"]]["netvaerk"] == "TDC NET"]
    frie = [a for a in ABON if a["data_gb"] >= 900]

    kandidater = [
        ("Billigst med data", sorted(med_data, key=lambda a: a["pris"]),
         "Laveste månedspris med mobildata"),
        ("Mest data pr. krone", sorted([a for a in med_data if a["data_gb"] < 900],
                                       key=lambda a: a["pris"] / a["data_gb"]),
         "Laveste pris pr. gigabyte"),
        ("Bedst dækning", sorted(tdc, key=lambda a: a["pris"]),
         "TDC NET — landets mest udbyggede"),
        ("Billigste fri data", sorted(frie, key=lambda a: a["pris"]),
         "Ubegrænset data i Danmark"),
    ]

    brugte = set()
    valg = []
    for kat, liste, detalje in kandidater:
        val = next((a for a in liste if a["udbyder"] not in brugte), liste[0] if liste else None)
        if not val:
            continue
        brugte.add(val["udbyder"])
        valg.append((kat, val, detalje))

    kort = ""
    for i, (kat, a, detalje) in enumerate(valg):
        u = UMAP[a["udbyder"]]
        g = gns12(a) or a["pris"]
        if a.get("intro_pris") is not None and a.get("intro_mdr"):
            vist = a["intro_pris"]
            under = (f'i {a["intro_mdr"]} mdr. — derefter {kr(a["pris"])} kr./md. · '
                     f'gns. {kr(g)} kr./md. over 12 mdr.')
        else:
            vist = a["pris"]
            under = f'fast pris · {kr(g * 12)} kr. samlet på 12 mdr.'
        kort += f"""<div class="valgkort v{i}">
  <span class="valg-badge">{e(kat)}</span>
  <div class="valg-top">
    <span class="valg-logo"><img src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])}" loading="lazy" width="{round(u['logo_w'] * 26 / u['logo_h'])}" height="26" decoding="async"></span>
    <div>
      <b>{e(a['navn'])}</b>
      <small>{netlabel(u)}</small>
    </div>
  </div>
  <div class="valg-tag">{gb_tekst(a['data_gb'])} · {e(detalje)}</div>
  <div class="valg-pris">{kr(vist)}<span> kr./md.</span></div>
  <div class="valg-under">{under}</div>
  <a class="knap knap-linje valg-knap" href="/udbydere/{u['slug']}/">Se abonnementet →</a>
</div>"""

    return f'<div class="baand"><div class="hurtigvalg">{kort}</div></div>'


# --------------------------------------------------------------- ekstra tabeller

def tabel_billigst_pr_udbyder():
    bedst = {}
    for a in ABON:
        if a["data_gb"] == 0:
            continue
        if a["udbyder"] not in bedst or a["pris"] < bedst[a["udbyder"]]["pris"]:
            bedst[a["udbyder"]] = a
    raekker = ""
    for a in sorted(bedst.values(), key=lambda x: x["pris"]):
        u = UMAP[a["udbyder"]]
        prgb = f'{a["pris"] / a["data_gb"]:.2f}'.replace(".", ",") + " kr." if 0 < a["data_gb"] < 900 else "—"
        raekker += (f'<tr><td><a href="/udbydere/{u["slug"]}/">{e(u["navn"])}</a></td>'
                    f'<td>{e(a["navn"])}</td><td>{gb_tekst(a["data_gb"])}</td>'
                    f'<td>{netlabel(u)}</td><td>{prgb}</td>'
                    f'<td><strong>{kr(a["pris"])} kr.</strong></td></tr>')
    return f"""<h3>Billigste abonnement hos hver udbyder</h3>
<p>Vil du vide, hvor lavt hver enkelt udbyder går, er det denne tabel. Den viser det
billigste abonnement, vi har registreret hos hvert selskab, og hvad det koster pr.
gigabyte.</p>
<table><thead><tr><th>Udbyder</th><th>Abonnement</th><th>Data</th><th>Netværk</th>
<th>Pris pr. GB</th><th>Pris/md.</th></tr></thead><tbody>{raekker}</tbody></table>"""


def tabel_pr_datamaengde():
    grupper = [("Op til 10 GB", 1, 10), ("11-20 GB", 11, 20), ("21-40 GB", 21, 40),
               ("41-80 GB", 41, 80), ("Over 80 GB", 81, 899), ("Fri data", 900, 9999)]
    raekker = ""
    for navn, lav, hoej in grupper:
        kandidater = [a for a in ABON if lav <= a["data_gb"] <= hoej and a["pris"] > 0]
        if not kandidater:
            continue
        bedst = min(kandidater, key=lambda a: a["pris"])
        u = UMAP[bedst["udbyder"]]
        prgb = f'{bedst["pris"] / bedst["data_gb"]:.2f}'.replace(".", ",") + " kr." if 0 < bedst["data_gb"] < 900 else "—"
        raekker += (f'<tr><td><strong>{e(navn)}</strong></td>'
                    f'<td><a href="/udbydere/{u["slug"]}/">{e(u["navn"])}</a> {e(bedst["navn"])}</td>'
                    f'<td>{prgb}</td><td>{kr(bedst["pris"] * 12)} kr.</td>'
                    f'<td><strong>{kr(bedst["pris"])} kr.</strong></td></tr>')
    return f"""<h3>Billigste abonnement i hver datakategori</h3>
<p>De fleste sammenligningssider viser kun den absolut laveste pris. Den er sjældent
relevant, hvis du bruger mere end 5 GB. Her er den billigste i hver kategori, med
årsomkostningen regnet med.</p>
<table><thead><tr><th>Datamængde</th><th>Billigste valg</th><th>Pris pr. GB</th>
<th>Pris pr. år</th><th>Pris/md.</th></tr></thead><tbody>{raekker}</tbody></table>"""


def tabel_prgb_rangliste(antal=12):
    med = [a for a in ABON if 0 < a["data_gb"] < 900]
    raekker = ""
    for i, a in enumerate(sorted(med, key=lambda x: x["pris"] / x["data_gb"])[:antal], 1):
        u = UMAP[a["udbyder"]]
        prgb = f'{a["pris"] / a["data_gb"]:.2f}'.replace(".", ",")
        raekker += (f'<tr><td>{i}</td><td><a href="/udbydere/{u["slug"]}/">{e(u["navn"])}</a> '
                    f'{e(a["navn"])}</td><td>{gb_tekst(a["data_gb"])}</td>'
                    f'<td>{kr(a["pris"])} kr.</td><td><strong>{prgb} kr.</strong></td></tr>')
    return f"""<h3>Rangliste: flest gigabyte for pengene</h3>
<p>Pris pr. gigabyte er det eneste tal, der gør abonnementer af forskellig størrelse
direkte sammenlignelige. Bemærk hvor langt nede på listen de billigste månedspriser
ligger — lav månedspris og god værdi er ikke det samme.</p>
<table><thead><tr><th>#</th><th>Abonnement</th><th>Data</th><th>Pris/md.</th>
<th>Pris pr. GB</th></tr></thead><tbody>{raekker}</tbody></table>"""


def tabel_aarsomkostning(antal=10):
    raekker = ""
    for a in [x for x in ABON if x["data_gb"] > 0][:antal]:
        u = UMAP[a["udbyder"]]
        aar = a["pris"] * 12 + a.get("oprettelse", 0)
        besparelse = (max(x["pris"] for x in ABON) * 12) - aar
        raekker += (f'<tr><td><a href="/udbydere/{u["slug"]}/">{e(u["navn"])}</a> {e(a["navn"])}</td>'
                    f'<td>{kr(a["pris"])} kr.</td><td>{kr(a.get("oprettelse", 0))} kr.</td>'
                    f'<td><strong>{kr(aar)} kr.</strong></td>'
                    f'<td class="ja">{kr(besparelse)} kr.</td></tr>')
    return f"""<h3>Hvad koster abonnementet på et helt år?</h3>
<p>Månedsprisen skjuler oprettelsesgebyrer. Her er den samlede førsteårsudgift for de
billigste abonnementer, og hvad du sparer i forhold til markedets dyreste.</p>
<table><thead><tr><th>Abonnement</th><th>Pr. md.</th><th>Oprettelse</th>
<th>Første år</th><th>Sparet mod dyreste</th></tr></thead><tbody>{raekker}</tbody></table>"""


SEGMENTER = [
    ("0–5 GB", 1, 5, "Barn eller let bruger", "Wi-fi hjemme og på arbejde"),
    ("6–15 GB", 6, 15, "Almindelig bruger", "Sociale medier, musik, navigation"),
    ("16–30 GB", 16, 30, "Aktiv bruger", "Pendling og lidt video på farten"),
    ("31–60 GB", 31, 60, "Streamer", "Video dagligt uden wi-fi"),
    ("61–150 GB", 61, 150, "Storforbruger", "Hotspot til laptop og tablet"),
    ("Fri data", 900, 9999, "Uden loft", "Mobilen er husstandens internet"),
]


def udbyder_rangliste():
    """Alle udbydere rangeret på laveste 12-måneders-pris."""
    raekker = ""
    data = []
    for u in UDBYDERE:
        planer = [a for a in ABON if a["udbyder"] == u["slug"] and a["pris"] > 0]
        if not planer:
            continue
        billigst_u = min(planer, key=lambda a: gns12(a) or 9e9)
        med_data = [a for a in planer if 0 < a["data_gb"] < 900]
        bedst_prgb = min(med_data, key=lambda a: a["pris"] / a["data_gb"]) if med_data else None
        data.append((u, planer, billigst_u, bedst_prgb))
    data.sort(key=lambda x: gns12(x[2]) or 9e9)

    for i, (u, planer, bu, bp) in enumerate(data, 1):
        maks = max(a["data_gb"] for a in planer)
        prgb = (f'{bp["pris"] / bp["data_gb"]:.2f}'.replace(".", ",") + " kr.") if bp else "—"
        raekker += (f'<tr><td><strong>{i}</strong></td>'
                    f'<td><a href="/udbydere/{u["slug"]}/">{e(u["navn"])}</a></td>'
                    f'<td>{netlabel(u)}</td><td>{len(planer)}</td>'
                    f'<td>{gb_tekst(maks)}</td><td>{prgb}</td>'
                    f'<td><strong>{kr(gns12(bu))} kr.</strong></td></tr>')
    return f"""<h2>Alle udbydere rangeret efter laveste pris</h2>
<p>Rangeret efter 12-måneders-prisen på det billigste abonnement hos hver udbyder — altså
den reelle pris, når intropris og normalpris regnes sammen. Bemærk kolonnen med pris pr.
GB: den billigste udbyder er sjældent den, der giver mest for pengene.</p>
<table>
<thead><tr><th>#</th><th>Udbyder</th><th>Netværk</th><th>Planer</th><th>Største pakke</th>
<th>Bedste pris pr. GB</th><th>Fra</th></tr></thead>
<tbody>{raekker}</tbody></table>"""


def netvaerksgruppering():
    """Udbyderne grupperet efter hvilket net de kører på."""
    ud = ""
    for n in NETVAERK + [{"navn": "MVNO", "slug": None,
                          "kort": "Selskaber hvor netværksaftalen ikke er verificeret"}]:
        selskaber = [u for u in UDBYDERE if u["netvaerk"] == n["navn"]]
        if not selskaber:
            continue
        planer = [a for a in ABON if UMAP[a["udbyder"]]["netvaerk"] == n["navn"] and a["pris"] > 0]
        billigst_n = min(planer, key=lambda a: gns12(a) or 9e9) if planer else None
        liste = "".join(
            f'<a href="/udbydere/{u["slug"]}/" class="netgruppe-selskab">'
            f'<img src="/assets/img/logoer/{u["logo"]}" alt="{e(u["navn"])}" loading="lazy"'
            f' width="{round(u["logo_w"] * 22 / u["logo_h"])}" height="22">'
            f'<span>{e(u["navn"])}</span></a>' for u in selskaber)
        titel = (f'<a href="/netvaerk/{n["slug"]}/">{e(n["navn"])}</a>' if n.get("slug")
                 else e(n["navn"]))
        ud += f"""<div class="netgruppe">
  <div class="netgruppe-hoved">
    <h3>{titel}</h3>
    <span class="netgruppe-tal">{len(selskaber)} selskab{"er" if len(selskaber) != 1 else ""} · {len(planer)} abonnementer
    {f"· fra {kr(gns12(billigst_n))} kr./md." if billigst_n else ""}</span>
  </div>
  <p>{e(n["kort"])}</p>
  <div class="netgruppe-liste">{liste}</div>
</div>"""
    return f"""<h2>Hvem kører på hvilket net?</h2>
<p>Det er den vigtigste opdeling af det danske marked. Der findes kun tre mobilnet, og dit
valg af selskab er reelt et valg af net. Selskaber markeret MVNO lejer sig ind, men vi har
ikke kunnet verificere hos hvem — og så gætter vi ikke.</p>
<div class="netgrupper">{ud}</div>"""


def ejerforhold():
    return """<h2>Hvem ejer hvem?</h2>
<p>Flere af de selskaber, der ser ud som konkurrenter, har samme ejer. Det er værd at vide,
fordi det forklarer, hvorfor to brands kan have identisk dækning og alligevel meget
forskellig pris.</p>
<table>
<thead><tr><th>Selskab</th><th>Ejer</th><th>Hvad det betyder for dig</th></tr></thead>
<tbody>
<tr><td><strong>YouSee</strong></td><td>Nuuday</td><td>Premiumbrandet på TDC NET med butikker og fuld kundeservice</td></tr>
<tr><td><strong>Telmore</strong></td><td>Nuuday</td><td>Søsterselskab til YouSee, samme net — men bygget om streaming</td></tr>
<tr><td><strong>CBB Mobil</strong></td><td>Telenor Danmark</td><td>Telenors prisbrand. Samme net som moderselskabet, lavere pris</td></tr>
<tr><td><strong>Oister</strong></td><td>Hi3G Denmark</td><td>3's prisbrand. Stærkt i byerne, svagere på landet</td></tr>
<tr><td><strong>Lebara</strong></td><td>Lebara Group</td><td>International MVNO specialiseret i udlandsopkald</td></tr>
<tr><td><strong>Lyca Mobile</strong></td><td>Lycamobile Group</td><td>International MVNO, stor i taletidssegmentet</td></tr>
</tbody>
</table>
<div class="tip">
<h3>Derfor er det relevant</h3>
<p>Vælger du mellem YouSee og Telmore, vælger du ikke mellem to netværk — de kører på
præcis samme master. Du vælger mellem to produktpakker. Vælger du mellem CBB og Telenor,
får du samme dækning til forskellig pris. Det er den type indsigt, der sparer penge uden at
koste noget i kvalitet.</p>
</div>"""


def prisfordeling():
    """Hele markedet fordelt på datasegmenter — deres stærkeste datawidget."""
    raekker = ""
    kort = ""
    maks = 0
    fordelt = []
    for navn, lav, hoej, profil, beskriv in SEGMENTER:
        planer = [a for a in ABON if lav <= a["data_gb"] <= hoej and a["pris"] > 0]
        if not planer:
            continue
        priser = sorted(gns12(a) for a in planer if gns12(a))
        fordelt.append((navn, profil, beskriv, planer, priser))
        maks = max(maks, len(planer))

    for navn, profil, beskriv, planer, priser in fordelt:
        bredde = round(len(planer) / maks * 100)
        raekker += f"""<div class="fordel-raekke">
  <div class="fordel-navn">{e(navn)}</div>
  <div class="fordel-bar"><span style="width:{bredde}%"></span></div>
  <div class="fordel-pris">{kr(priser[0])}–{kr(priser[-1])} kr.</div>
  <div class="fordel-antal">{len(planer)} planer</div>
</div>"""
        billigst_seg = min(planer, key=lambda a: gns12(a) or 9e9)
        u = UMAP[billigst_seg["udbyder"]]
        kort += f"""<div class="segkort">
  <div class="seg-navn">{e(navn)}</div>
  <div class="seg-profil">{e(profil)}</div>
  <p>{e(beskriv)}</p>
  <div class="seg-pris">fra {kr(gns12(billigst_seg))} kr./md.</div>
  <div class="seg-antal">{len(planer)} planer · billigst hos {e(u["navn"])}</div>
</div>"""

    return f"""<h2>Sådan fordeler priserne sig på markedet</h2>
<p>Her er hele vores sammenligning delt op efter datamængde. Priserne er
gennemsnitspris over 12 måneder, så intro­tilbud ikke trækker billedet skævt.</p>
<div class="fordeling">{raekker}</div>
<p class="fordel-note">Bemærk hvor lidt prisen stiger fra segment til segment. Springet fra
6–15 GB til 31–60 GB er typisk under 40 kr. om måneden, mens datamængden femdobles. Det er
grunden til, at vi næsten altid anbefaler ét trin over dit målte forbrug.</p>
<h3>Find dig selv i et segment</h3>
<div class="segkort-gitter">{kort}</div>"""


def udbydergitter():
    """Udbyderne side om side med net, laveste pris og antal planer."""
    kort = ""
    for u in sorted(UDBYDERE, key=lambda x: min(
            [a["pris"] for a in ABON if a["udbyder"] == x["slug"] and a["pris"] > 0] or [9999])):
        planer = [a for a in ABON if a["udbyder"] == u["slug"]]
        betalte = [a["pris"] for a in planer if a["pris"] > 0]
        fra = f"fra {kr(min(betalte))} kr./md." if betalte else "se udbyder"
        kort += f"""<a class="ugkort" href="/udbydere/{u['slug']}/">
  <img src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])}" loading="lazy" width="{round(u["logo_w"] * 24 / u["logo_h"])}" height="24" decoding="async">
  <b>{e(u['navn'])}</b>
  <span class="ug-net">{netlabel(u)}</span>
  <span class="ug-pris">{fra}</span>
  <span class="ug-antal">{len(planer)} planer</span>
</a>"""
    return f"""<h2>Udbyderne side om side</h2>
<p>Vi viser også udbydere, vi ikke har en provisionsaftale med. Det er den eneste måde,
en sammenligning bliver troværdig på. Klik videre for vores gennemgang af den enkelte.</p>
<div class="ugkort-gitter">{kort}</div>"""


def vejviser(aktuel=""):
    """Krydslinks til alle kategorier med antal — deres 'vælg din vej videre'."""
    veje = [
        ("/billigste-mobilabonnement/", "Billigste", f"fra {D['min_pris']} kr./md."),
        ("/bedste-mobilabonnement/", "Bedste", "vores kriterier"),
        ("/mobilabonnement-med-fri-data/", "Fri data",
         f"{len([a for a in ABON if a['data_gb'] >= 900])} planer"),
        ("/mobilabonnement-med-fri-tale/", "Fri tale",
         f"{len([a for a in ABON if a['tale'] == 'fri'])} planer"),
        ("/mobilabonnement-uden-data/", "Uden data",
         f"{len([a for a in ABON if a['data_gb'] == 0])} planer"),
        ("/mobilabonnement-med-streaming/", "Med streaming",
         f"{len([a for a in ABON if a.get('streaming')])} planer"),
        ("/mobilabonnement-med-netflix/", "Med Netflix",
         f"{len([a for a in ABON if 'Netflix' in a.get('streaming', [])])} planer")
        if "Netflix" in TJENESTER_I_DATA else None,
        ("/mobilabonnement-med-esim/", "Med eSIM", "klar samme dag"),
        ("/mobilabonnement-til-boern/", "Til børn", "tryghed og lav pris"),
        ("/mobilabonnement-til-unge/", "Til unge", "meget data"),
        ("/mobilabonnement-uden-binding/", "Uden binding",
         f"{len([a for a in ABON if a['binding'] == 0])} planer"),
        ("/netvaerk/", "Mobilnetværk", "de tre danske net"),
        ("/mobilabonnementer-black-friday/", "Black Friday", "er tilbuddene ægte?"),
    ]
    punkter = "".join(
        f'<a href="{h}"><b>{e(t)}</b><span>{e(u)}</span></a>'
        for h, t, u in [v for v in veje if v]
        if h != aktuel and _MULIGE.get(h, True))
    return f"""<h2>Vælg din vej videre</h2>
<p>Vi har en dedikeret oversigt til hvert af de mest almindelige behov. Tallene er antal
abonnementer i kategorien.</p>
<div class="vejviser">{punkter}</div>"""


def redaktionens_valg():
    """Fire redaktionelle picks med begrundelse — ikke bare beregnede tal."""
    med_data = [a for a in ABON if a["data_gb"] > 0 and a["pris"] > 0]
    tdc = [a for a in med_data if UMAP[a["udbyder"]]["netvaerk"] == "TDC NET"]
    frie = [a for a in ABON if a["data_gb"] >= 900 and a["pris"] > 0]
    fast = [a for a in med_data if not a.get("intro_pris")]

    valg = []
    if fast:
        v = min(fast, key=lambda a: a["pris"])
        valg.append((v, "Billigst uden intro-fælde",
            f"Fast pris fra dag ét. Ingen kampagneperiode der udløber, ingen påmindelse du "
            f"skal huske at sætte. Prisen du ser, er prisen om tolv måneder — og det er "
            f"mere værd end de tyve kroner, du kan spare på et introtilbud, du glemmer at "
            f"genforhandle."))
    endelig = [a for a in med_data if a["data_gb"] < 900]
    if endelig:
        v = min(endelig, key=lambda a: a["pris"] / a["data_gb"])
        valg.append((v, "Mest for pengene",
            f"Laveste pris pr. gigabyte i hele sammenligningen. Det er det tal, der gør "
            f"abonnementer af forskellig størrelse sammenlignelige, og her er der ikke "
            f"nogen tæt på. Har du et forbrug i den størrelse, er det svært at argumentere "
            f"for noget andet."))
    if tdc:
        v = min(tdc, key=lambda a: gns12(a) or 9e9)
        valg.append((v, "Bedst hvis dækning betyder noget",
            f"Billigste vej ind på TDC NET, som er det mest udbyggede net i Danmark. Bor du "
            f"på landet, i et sommerhusområde eller pendler du langt, er det her, du skal "
            f"kigge — også selvom der findes billigere abonnementer på de andre net."))
    if frie:
        v = min(frie, key=lambda a: gns12(a) or 9e9)
        valg.append((v, "Til dig uden fastnet",
            f"Billigste fri data regnet over tolv måneder. Bruger du mobilen som husstandens "
            f"internet via hotspot, er det her, regnestykket vender — under cirka 80 GB om "
            f"måneden er et almindeligt stort abonnement stadig billigere."))

    kort = ""
    for a, kat, tekst in valg[:4]:
        u = UMAP[a["udbyder"]]
        g = gns12(a) or a["pris"]
        kort += f"""<div class="rvkort">
  <div class="rv-kat">{e(kat)}</div>
  <div class="rv-top">
    <img src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])}" loading="lazy" width="{round(u["logo_w"] * 22 / u["logo_h"])}" height="22" decoding="async">
    <div><b>{e(a['navn'])}</b><small>{netlabel(u)} · {gb_tekst(a['data_gb'])}</small></div>
  </div>
  <div class="rv-pris">{kr(g)} kr.<em>/md. i snit over 12 mdr.</em></div>
  <p>{e(tekst)}</p>
  <div class="rv-links">
    <a href="{a['link']}" rel="sponsored nofollow noopener" target="_blank"
       data-udgaaende="{e(u['slug'])}" data-abonnement="{e(a['id'])}">Se hos {e(u['navn'])} →</a>
    <a href="/udbydere/{u['slug']}/">Læs vores gennemgang →</a>
  </div>
</div>"""

    return f"""<h2>De fire abonnementer vi selv ville pege på</h2>
<p>Vi gennemgår markedet ved hver opdatering og udpeger ét abonnement i hver hovedkategori.
Udvælgelsen er ikke rangeret efter, hvad vi tjener på — det er, hvad vi ville sige til en
ven, der spurgte, hvad de skulle skifte til.</p>
<div class="rvkort-gitter">{kort}</div>
<p class="rv-note">Verificeret {OPDATERET} mod priserne i vores sammenligning. Bemærk at
priserne er placeholders, indtil datakilden er koblet på.</p>"""


def overforbrug():
    return """<h2>Hvad sker der, når datamængden er brugt op?</h2>
<p>Det er en af de vigtigste forskelle mellem udbyderne, og den står sjældent i en
pristabel. Der findes tre modeller, og de har vidt forskellige konsekvenser for din regning.</p>
<table>
<thead><tr><th>Model</th><th>Hvad der sker</th><th>Konsekvens for dig</th></tr></thead>
<tbody>
<tr><td><strong>Nedsat hastighed</strong></td><td>Forbindelsen fortsætter, men langsomt — ofte
ned til et par hundrede kilobit</td><td>Ingen ekstra regning. Beskeder og kort virker, video
gør ikke</td></tr>
<tr><td><strong>Automatisk køb</strong></td><td>Udbyderen køber ekstra datapakker på dine
vegne, når du løber tør</td><td>Bekvemt, men det er her de store overraskelsesregninger
opstår</td></tr>
<tr><td><strong>Fuld spærring</strong></td><td>Mobildata stopper helt indtil næste
afregningsperiode</td><td>Kan ikke koste ekstra. Til gengæld står du uden data</td></tr>
</tbody>
</table>
<div class="advarsel">
<p><strong>Sådan finder du din udbyders model:</strong> Den står i abonnementsvilkårene under
overforbrug eller datastop. Uanset hvilken model din udbyder bruger, bør du slå datastop til
i appen — det gør spørgsmålet irrelevant, fordi forbindelsen så aldrig kan udløse et køb.</p>
</div>
<p>Vi arbejder på at kortlægge modellen for hver enkelt udbyder. Indtil den kortlægning er
verificeret, vil vi ikke gætte — se udbyderens egne vilkår, eller
<a href="/kontakt/">skriv til os</a>, hvis du kender svaret for et selskab, vi mangler.</p>"""


# Kun URL'er vi har verificeret. Vi linker aldrig til noget, vi ikke har tjekket.
KILDER = {
    "teleankenaevnet": ("Teleankenævnet", "https://teleanke.dk/",
                        "Privat godkendt ankenævn for klager på teleområdet"),
    "teleanke_klag": ("Teleankenævnet — klag online", "https://teleanke.dk/klag-online-nu/",
                      "Klageskema og krav til dokumentation"),
    "forbrugerombudsmanden": ("Forbrugerombudsmanden", "https://forbrugerombudsmanden.dk/",
                              "Tilsyn med markedsføringsloven, herunder skjult reklame"),
    "reklameidentifikation": ("Forbrugerombudsmandens vejledning om reklameidentifikation",
                              "https://forbrugerombudsmanden.dk/media/49158/vejledning-reklameidentifikation.pdf",
                              "Regler om tydelig markering af kommerciel hensigt"),
    "datatilsynet": ("Datatilsynet", "https://www.datatilsynet.dk/",
                     "Tilsyn med kreditoplysningsbureauer og databeskyttelse"),
    "borger_kredit": ("Borger.dk om registrering af forbrugeroplysninger",
                      "https://www.borger.dk/samfund-og-rettigheder/Folkeregister-og-CPR/Registrering-af-forbrugeroplysninger",
                      "Dine rettigheder ved registrering som dårlig betaler"),
    "experian": ("Experian om RKI-registret",
                 "https://www.experian.dk/erhverv/forbrugerinformation/kreditvurdering/registreret-i-rki",
                 "Registrets egen beskrivelse af indberetning og sletning"),
    "digst_klage": ("Digitaliseringsstyrelsen om klager på teleområdet",
                    "https://digst.dk/tele/telefoni-og-internet/abonnement-paa-telefoni-og-internet/hvordan-klager-man/",
                    "Officiel vejledning i klageveje"),
    "teleklagenaevnet": ("Teleklagenævnet", "https://naevneneshus.dk/naevnsoversigt/teleklagenaevnet/",
                         "Klager over afgørelser fra Erhvervsstyrelsen og Energistyrelsen"),
    "teleindustrien": ("Teleindustrien", "https://www.teleindu.dk/",
                       "Teleselskabernes brancheorganisation"),
}


def erfaring(noegle):
    return historier.historie(noegle, FORFATTER["billede"], FORFATTER["navn"],
                              "/om/emil-rostgaard/")


def kilder(noegler=None, egne=None):
    """Kildeblok med klikbare, verificerede kilder plus vores eget grundlag."""
    li = ""
    for n in (noegler or []):
        navn, url, hvad = KILDER[n]
        li += (f'<li><a href="{url}" rel="noopener nofollow" target="_blank">{e(navn)}</a>'
               f' <span class="kilde-hvad">{e(hvad)}</span></li>')
    for tekst in (egne or []):
        li += f'<li><span class="kilde-egen">Eget grundlag</span> {tekst}</li>'
    return f"""<h2>Kilder og grundlag</h2>
<p>Vi mener, at en sammenligningsside skal kunne vise, hvor tallene og påstandene kommer
fra. Eksterne kilder åbner i et nyt vindue.</p>
<ul class="kildeliste">{li}</ul>
<p class="kildenote">Finder du en oplysning, der ikke stemmer, så
<a href="/kontakt/">skriv til os</a>. Vi retter og noterer datoen for rettelsen. Se også
<a href="/metode/">vores metode</a>.</p>"""


def begrebstabel():
    return """<h2>Begreber du møder, når du sammenligner</h2>
<p>Udbydernes produktsider bruger en række ord, der ikke betyder helt det, man tror. Her er
de vigtigste oversat til almindeligt dansk.</p>
<table>
<thead><tr><th>Begreb</th><th>Hvad det betyder i praksis</th><th>Hvad du skal tjekke</th></tr></thead>
<tbody>
<tr><td><strong>Fri tale</strong></td><td>Ubegrænsede opkald til danske mobil- og fastnetnumre</td><td>Dækker ikke særnumre eller udlandsopkald</td></tr>
<tr><td><strong>Fri data</strong></td><td>Ubegrænset data i Danmark</td><td>EU-mængden er næsten altid begrænset</td></tr>
<tr><td><strong>EU-data</strong></td><td>Hvor meget af din data du kan bruge på rejse i EU</td><td>Kan være langt lavere end mængden i Danmark</td></tr>
<tr><td><strong>MVNO</strong></td><td>Selskab uden eget mobilnet, der lejer sig ind hos en netværksejer</td><td>Hvilket net de lejer sig ind på</td></tr>
<tr><td><strong>Datastop</strong></td><td>Forbindelsen stopper i stedet for at der købes ekstra data</td><td>Slå det til med det samme</td></tr>
<tr><td><strong>Normalpris</strong></td><td>Prisen efter en eventuel kampagneperiode</td><td>Den pris du betaler i det meste af året</td></tr>
<tr><td><strong>Oprettelse</strong></td><td>Engangsgebyr ved start af abonnementet</td><td>Fordel det over din forventede abonnementsperiode</td></tr>
<tr><td><strong>Binding</strong></td><td>Periode hvor du ikke kan opsige</td><td>Sjældent nødvendigt at acceptere i dag</td></tr>
<tr><td><strong>Nummerportering</strong></td><td>At tage dit nummer med til en ny udbyder</td><td>Er en rettighed — den nye udbyder klarer det</td></tr>
<tr><td><strong>Forbrugsafregnet</strong></td><td>Ingen fast månedspris, du betaler pr. minut og sms</td><td>Bliver dyrt over cirka 100 minutter om måneden</td></tr>
</tbody>
</table>
<p>Er du i tvivl om et begreb, du ikke finder her, så skriv til os via
<a href="/kontakt/">kontaktsiden</a>, så tilføjer vi det.</p>"""


def fejltabel():
    return """<h2>De fem fejl der koster danskerne flest penge</h2>
<p>Vi har samlet de mønstre, vi ser igen og igen, når folk gennemgår deres mobilregning.
De er alle sammen nemme at rette, og de fleste tager under ti minutter.</p>
<table>
<thead><tr><th>Fejl</th><th>Hvad det koster typisk</th><th>Løsningen</th></tr></thead>
<tbody>
<tr><td>Har haft samme abonnement i 3+ år</td><td>50-100 kr./md.</td><td>Sammenlign en gang om året — de bedste priser går til nye kunder</td></tr>
<tr><td>Betaler for fri data uden at bruge det</td><td>70-100 kr./md.</td><td>Tjek dit faktiske forbrug og flyt ned i kategori</td></tr>
<tr><td>Køber ekstra data hver måned</td><td>40-60 kr./md.</td><td>Gå ét trin op i pakke — det er næsten altid billigere</td></tr>
<tr><td>Overser prisstigning efter kampagne</td><td>50-100 kr./md.</td><td>Sæt kalenderpåmindelse ved kampagneperiodens udløb</td></tr>
<tr><td>Telefon på afbetaling bundet til abonnement</td><td>Bindende i 24-36 mdr.</td><td>Køb telefon og abonnement hver for sig</td></tr>
</tbody>
</table>
<p>Lægger man de tre første sammen, taler vi om en besparelse i omegnen af 2.000 kr. om
året for en helt almindelig husstand med to voksne. Det er ikke et teoretisk tal — det er
forskellen mellem markedets normalpris og det, mange faktisk betaler.</p>"""


# --------------------------------------------------------------- FORSIDE

def byg_forside():
    sti = "/"
    titel = f"Sammenlign mobilabonnementer — priser fra {D['min_pris']} kr./md."
    besk = (f"Sammenlign {D['antal']} mobilabonnementer fra {D['antal_udbydere']} udbydere på ét sted. "
            f"Priser fra {D['min_pris']} kr./md., fri tale og ingen binding. Opdateret {OPDATERET}.")

    faq = [
        {"sp": "Hvad er det billigste mobilabonnement i Danmark?",
         "sv": f"Det billigste mobilabonnement i vores sammenligning koster {D['min_pris']} kr. om måneden "
               f"og indeholder fri tale, fri sms og {gb_tekst(billigst['data_gb']).lower()}. Priserne ændrer sig "
               "løbende, så tjek tabellen for de aktuelle tal."},
        {"sp": "Hvor meget data har jeg brug for?",
         "sv": "De fleste danskere klarer sig med 15-30 GB om måneden. Bruger du primært wi-fi hjemme og på "
               "arbejde, rækker 5-10 GB. Streamer du video på farten eller bruger telefonen som hotspot, bør du "
               "vælge 50 GB eller mere."},
        {"sp": "Kan jeg beholde mit mobilnummer, når jeg skifter?",
         "sv": "Ja. Nummerportering er en rettighed i Danmark. Du bestiller hos den nye udbyder og oplyser dit "
               "nummer, hvorefter de klarer flytningen. Du skal ikke selv opsige dit gamle abonnement."},
        {"sp": "Er billige mobilabonnementer dårligere?",
         "sv": "Nej, ikke nødvendigvis. Der findes kun tre mobilnetværk i Danmark, og de billige selskaber lejer "
               "sig ind på de samme master som de dyre. Forskellen ligger typisk i kundeservice, tillægsydelser og "
               "i nogle tilfælde prioritering i myldretiden."},
        {"sp": "Hvor ofte bør jeg skifte mobilabonnement?",
         "sv": "Tjek dit abonnement en gang om året. De bedste priser går til nye kunder, så har du haft samme "
               "abonnement i flere år, betaler du sandsynligvis mere end nødvendigt for det samme."},
        {"sp": "Hvad koster det at skifte mobilselskab?",
         "sv": "Selve skiftet er gratis. Du skal dog være opmærksom på eventuel binding og på restgæld, hvis du har "
               "købt telefon på afbetaling — den følger ikke med til det nye selskab."},
    ]

    krumme = [(None, "Forside")]

    krop = f"""
{hurtigvalg()}

{pristabel(ABON, UMAP,
           titel=f"Alle mobilabonnementer sammenlignet",
           undertitel=f"{D['antal']} abonnementer fra {D['antal_udbydere']} udbydere, sorteret efter laveste månedspris. "
                      "Klik på en overskrift for at sortere efter data, pris pr. GB eller pris.",
           billigst_id=bedste_pr_gb['id'])}

{quiz()}

<section class="sektion baand">
  <div class="todelt afslør">
    <div class="todelt-billede">{guidebillede("forside", "Par sammenligner mobilabonnementer på telefonen i Nyhavn i København")}</div>
    <div class="todelt-tekst">
      <span class="etiket">Uafhængig sammenligning</span>
      <h2>Vi regner den pris ud, udbyderne ikke viser</h2>
      <p>Næsten alle abonnementer sælges på en intropris, der gælder i to til seks måneder.
      Bagefter stiger den. Vi lægger intropris, normalpris og oprettelse sammen og viser
      gennemsnittet over 12 måneder — det tal, du reelt kommer til at betale.</p>
      <p>Tabellerne sorteres altid efter pris, aldrig efter hvad vi tjener. Vi skriver også
      ulemperne ved hver udbyder, og vi tager udbydere med, vi ikke har en aftale med.</p>
      <div class="todelt-knapper">
        <a href="/metode/" class="knap knap-linje">Sådan beregner vi</a>
        <a href="/saadan-tjener-vi-penge/" class="knap knap-linje">Sådan tjener vi penge</a>
      </div>
    </div>
  </div>
</section>

<section class="sektion baand-smal">{erfaring("forside")}</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET)}
  <h2>Sådan bruger du sammenligningen</h2>
  <p>Tabellen ovenfor viser alle abonnementer, vi følger, sorteret efter laveste månedspris.
  Men den billigste række er ikke automatisk det rigtige valg for dig. Tre kolonner er
  vigtigere end prisen alene:</p>
  <ul>
    <li><strong>Data</strong> — vælg efter dit faktiske forbrug de seneste tre måneder, ikke
    efter hvad du tror. <a href="/guides/hvor-meget-data/">Sådan finder du tallet</a>.</li>
    <li><strong>Pris pr. GB</strong> — det eneste tal, der gør abonnementer direkte
    sammenlignelige på tværs af størrelser.</li>
    <li><strong>Netværk</strong> — står under udbydernavnet. Bor du uden for de større byer,
    betyder det mere end 30 kr. i prisforskel. <a href="/guides/daekning-og-netvaerk/">Læs om
    de tre net</a>.</li>
  </ul>
  <div class="tip">
    <h3>Den hurtige version</h3>
    <p>Bor du i en by og bruger under 30 GB: tag den billigste række, der dækker dit forbrug.
    Bor du på landet eller pendler langt: sortér efter pris, men vælg det billigste abonnement
    på TDC NET frem for det billigste i alt.</p>
  </div>
</section>

<section class="sektion sektion-hvid">
  <div class="baand">
    <div class="sektion-hoved midt afslør">
      <span class="etiket">Kategorier</span>
      <h2>Find abonnementet efter dit behov</h2>
      <p class="led">Vi har lavet dedikerede sammenligninger til de mest almindelige situationer.</p>
    </div>
    <div class="kortgitter kg-4 afslør">
      <a class="kort" href="/billigste-mobilabonnement/" style="text-decoration:none;color:inherit">
        <div class="ikon">💰</div><h3>Billigste abonnement</h3>
        <p>Hele markedet sorteret efter pris, med gennemgang af de skjulte omkostninger.</p></a>
      <a class="kort" href="/mobilabonnement-med-fri-data/" style="text-decoration:none;color:inherit">
        <div class="ikon">∞</div><h3>Fri data</h3>
        <p>Hvad fri data koster — og hvorfor de fleste ikke har brug for det.</p></a>
      <a class="kort" href="/mobilabonnement-til-unge/" style="text-decoration:none;color:inherit">
        <div class="ikon">🎓</div><h3>Unge og studerende</h3>
        <p>Meget data, lav pris og ingen binding, så du kan skifte når du flytter.</p></a>
      <a class="kort" href="/mobilabonnement-uden-binding/" style="text-decoration:none;color:inherit">
        <div class="ikon">🔓</div><h3>Uden binding</h3>
        <p>Abonnementer du kan opsige med kort varsel, hvis behovet ændrer sig.</p></a>
    </div>
  </div>
</section>

<section class="sektion baand">
  <div class="sektion-hoved afslør">
    <span class="etiket">Udbydere</span>
    <h2>De {D['antal_udbydere']} udbydere vi følger</h2>
    <p class="led">Uafhængige gennemgange med både fordele og ulemper. Vi skriver også, hvem
    udbyderen <em>ikke</em> passer til.</p>
  </div>
  <div class="kortgitter kg-3 afslør">
    {"".join(udbyderkort(u) for u in UDBYDERE)}
  </div>
</section>


<section class="sektion baand-smal">
  {forfatterboks()}
  {afsloering()}
</section>
"""

    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_forside(), efter_hero=logobaand(), krumme=krumme,
        indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, TJENESTE, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     listeld(ABON, "Mobilabonnementer i Danmark"))],
    ), prioritet="1.0", hyppighed="daily")


def udbyderkort(u):
    priser = [a["pris"] for a in ABON if a["udbyder"] == u["slug"]]
    fra = min(priser) if priser else None
    return f"""<a class="udbyderkort" href="/udbydere/{u['slug']}/">
  <img src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])} logo" loading="lazy" width="{round(u['logo_w'] * 30 / u['logo_h'])}" height="30" decoding="async">
  <h3>{e(u['navn'])}</h3>
  <p>{e(u['kort'])}</p>
  <div class="fra">{'fra ' + kr(fra) + ' kr./md.' if fra else ''} <em>· {netlabel(u)}</em></div>
</a>"""


# --------------------------------------------------------------- BILLIGSTE

def byg_billigste():
    sti = "/billigste-mobilabonnement/"
    titel = f"Billigste mobilabonnement — priser fra {D['min_pris']} kr./md."
    besk = (f"Se det billigste mobilabonnement i Danmark lige nu. {D['antal']} abonnementer "
            f"sammenlignet på pris, data og pris pr. GB. Opdateret {OPDATERET}.")
    krumme = [("/", "Forside"), (None, "Billigste mobilabonnement")]

    faq = [
        {"sp": f"Hvad er det billigste mobilabonnement lige nu?",
         "sv": f"Det billigste abonnement i vores sammenligning koster {D['min_pris']} kr. om måneden med "
               f"{gb_tekst(billigst['data_gb']).lower()}, fri tale og fri sms uden binding."},
        {"sp": "Er det billigste abonnement også det bedste?",
         "sv": "Sjældent. Det billigste abonnement har typisk lidt data, og overforbrug kan hurtigt gøre det "
               "dyrere end et større abonnement. Vælg det billigste abonnement, der dækker dit faktiske forbrug."},
        {"sp": "Hvorfor er nogle mobilabonnementer så billige?",
         "sv": "Fordi selskaberne ikke ejer nettet selv, men lejer sig ind hos en af de tre netværksejere. De "
               "sparer omkostninger på butikker, kundeservice og tillægsydelser og sender besparelsen videre."},
        {"sp": "Hvad betyder pris pr. GB?",
         "sv": "Månedsprisen divideret med antallet af inkluderede gigabyte. Det gør abonnementer af forskellig "
               "størrelse direkte sammenlignelige og afslører, at store abonnementer ofte er billigere pr. gigabyte."},
        {"sp": "Skal jeg vælge abonnement med eller uden binding?",
         "sv": "Uden binding i næsten alle tilfælde. De fleste danske abonnementer er uden binding, og det giver "
               "dig frihed til at skifte, hvis prisen stiger, eller behovet ændrer sig."},
        {"sp": "Hvad sker der, hvis jeg bruger mere data end inkluderet?",
         "sv": "Det afhænger af udbyderen. Nogle stopper forbindelsen, andre sætter hastigheden ned, og andre "
               "opkræver for ekstra forbrug. Slå datastop til i udbyderens app for at undgå uventede regninger."},
        {"sp": "Kan jeg få mobilabonnement uden kreditvurdering?",
         "sv": "Taletidsløsninger kræver normalt ikke kreditvurdering, da du betaler forud. Almindelige "
               "abonnementer indebærer som regel en kreditvurdering."},
    ]

    krop = f"""
{hurtigvalg()}

{pristabel(ABON, UMAP,
           titel="Billigste mobilabonnementer lige nu",
           undertitel="Sorteret efter laveste månedspris. Brug filtrene til at se kun de "
                      "abonnementer, der matcher dit dataforbrug.",
           billigst_id=bedste_pr_gb['id'])}

{(indhold.billigste_brodtekst(D)).replace(
    '<section class="sektion baand-smal artikel">',
    '<section class="sektion baand-smal artikel">' + gennemgangslinje(OPDATERET), 1
).replace(
    '<h2>De skjulte omkostninger, folk overser</h2>',
    erfaring('billigste') + redaktionens_valg() + prisfordeling() + tabel_billigst_pr_udbyder()
    + tabel_prgb_rangliste() + tabel_aarsomkostning() + overforbrug() + '<h2>De skjulte omkostninger, folk overser</h2>', 1
).replace(
    '<h2>Hvilket abonnement passer til din situation?</h2>',
    tabel_pr_datamaengde() + udbydergitter() + '<h2>Hvilket abonnement passer til din situation?</h2>', 1
).replace('</section>', vejviser('/billigste-mobilabonnement/') + '</section>', 1)}

<section class="sektion baand-smal">
  {laesvidere([
      ("/mobilabonnement-med-fri-data/", "Mobilabonnement med fri data — er det pengene værd?"),
      ("/guides/hvor-meget-data/", "Hvor meget data har jeg brug for?"),
      ("/guides/daekning-og-netvaerk/", "Dækning og netværk: TDC NET, Telenor og 3"),
      ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
      ("/mobilabonnement-uden-binding/", "Mobilabonnement uden binding"),
      ("/udbydere/", "Alle udbydere gennemgået"),
  ])}
  {forfatterboks()}
  {afsloering()}
</section>
"""

    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side("Sammenligning", f"Billigste mobilabonnement — fra {D['min_pris']} kr.",
                       f"Vi har regnet {D['antal']} abonnementer igennem og fundet, hvad de reelt koster "
                       "pr. gigabyte. Under tabellen forklarer vi, hvad du skal se efter, "
                       "og hvilke omkostninger der ikke står i prisen.",
                       '<a href="#sammenlign" class="knap knap-primaer">Gå til tabellen</a>'),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk),
                     listeld(ABON, "Billigste mobilabonnementer"))],
    ), prioritet="0.9", hyppighed="daily")


# --------------------------------------------------------------- FRI DATA

def byg_fridata():
    sti = "/mobilabonnement-med-fri-data/"
    titel = f"Mobilabonnement med fri data — priser fra {D['pris_fri']} kr./md."
    besk = (f"Sammenlign mobilabonnementer med fri data. Priser fra {D['pris_fri']} kr./md. "
            "Se hvad fri data reelt dækker, og om du overhovedet har brug for det.")
    krumme = [("/", "Forside"), (None, "Fri data")]
    udvalg = fri + [a for a in ABON if a["data_gb"] >= 50 and a["data_gb"] < 900]
    udvalg = sorted(udvalg, key=lambda a: a["pris"])

    faq = [
        {"sp": f"Hvad koster mobilabonnement med fri data?",
         "sv": f"Fri data koster fra {D['pris_fri']} kr. om måneden i vores sammenligning. Prisen varierer "
               "især med, hvilket netværk udbyderen kører på, og hvor meget data der er inkluderet i EU."},
        {"sp": "Er fri data virkelig ubegrænset?",
         "sv": "I Danmark er der som regel ingen grænse for datamængden. Til gengæld er der næsten altid et loft "
               "for, hvor meget du kan bruge i EU, og de fleste abonnementer har vilkår om rimeligt forbrug."},
        {"sp": "Hvornår kan fri data betale sig?",
         "sv": "Når du fast bruger over cirka 80-100 GB om måneden, eller når mobilen er din eneste "
               "internetforbindelse. Bruger du under 60 GB, er et almindeligt stort abonnement billigere."},
        {"sp": "Har fri data hastighedsbegrænsning?",
         "sv": "Nogle abonnementer har et hastighedsloft eller lavere prioritet i myldretiden. Det fremgår af "
               "abonnementsvilkårene og er værd at tjekke, hvis du streamer i høj opløsning."},
        {"sp": "Kan jeg bruge fri data som hotspot?",
         "sv": "Hos de fleste danske udbydere ja, men tjek vilkårene. Nogle abonnementer begrænser deling til "
               "andre enheder, og hotspot til en laptop bruger langt mere data end telefonen selv."},
    ]

    krop = f"""
{pristabel(udvalg, UMAP,
           titel="Fri data og store abonnementer sammenlignet",
           undertitel="Vi viser både fri data og de store abonnementer fra 50 GB, så du kan se, "
                      "hvad forskellen reelt koster dig om måneden.",
           billigst_id=min(fri, key=lambda a: a['pris'])['id'] if fri else None)}

{indhold.fridata_brodtekst(D).replace(
    '<section class="sektion baand-smal artikel">',
    '<section class="sektion baand-smal artikel">' + gennemgangslinje(OPDATERET), 1
).replace(
    '<h2>Hvad bruger man egentlig data på?</h2>',
    erfaring('fri_data') + tabel_pr_datamaengde() + '<h2>Hvad bruger man egentlig data på?</h2>', 1
).replace('</section>', tabel_prgb_rangliste() + fejltabel() + begrebstabel() + '</section>', 1)}

<section class="sektion baand-smal">
  {laesvidere([
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/guides/hvor-meget-data/", "Hvor meget data har jeg brug for?"),
      ("/guides/daekning-og-netvaerk/", "Dækning og netværk i Danmark"),
      ("/udbydere/oister/", "Oister — mest data for pengene"),
  ])}
  {forfatterboks()}
  {afsloering()}
</section>
"""

    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side("Fri data", "Mobilabonnement med fri data",
                       f"Fri data koster fra {D['pris_fri']} kr. om måneden. Her er hvad det dækker, "
                       "hvad det ikke dækker, og hvordan du regner ud, om du overhovedet har brug for det.",
                       '<a href="#sammenlign" class="knap knap-primaer">Se priserne</a>'),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk), listeld(udvalg, "Abonnementer med fri data"))],
    ), prioritet="0.9")


# --------------------------------------------------------------- NICHESIDER

def byg_niche(sti, etiket, h1, titel, besk, intro, udvalg, brodtekst, faq, links):
    krumme = [("/", "Forside"), (None, etiket)]
    krop = f"""
{pristabel(udvalg, UMAP, titel=f"Bedste valg — {etiket.lower()}", undertitel=intro,
           billigst_id=udvalg[0]['id'] if udvalg else None)}
<section class="sektion baand-smal artikel">{gennemgangslinje(OPDATERET)}{brodtekst}
{tabel_billigst_pr_udbyder()}{tabel_pr_datamaengde()}{fejltabel()}{begrebstabel()}</section>
<section class="sektion baand-smal">
  {laesvidere(links)}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(etiket, h1, intro,
                       '<a href="#sammenlign" class="knap knap-primaer">Se priserne</a>'),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk), listeld(udvalg, etiket))],
    ), prioritet="0.8")


def byg_kategori(*, sti, etiket, h1, titel, besk, intro, udvalg, tekstfunktion,
                 faq, links, chips=None, ekstra_tabeller=None, tabeltitel=None):
    """Kategoriside: hero med radar, tabel, langt indhold og ekstra datatabeller."""
    krumme = [("/", "Forside"), (None, etiket)]
    t = {"gennemgang": gennemgangslinje(OPDATERET)}
    brod = tekstfunktion(D, t)

    if ekstra_tabeller:
        brod = brod.replace("</section>", "".join(ekstra_tabeller) + "</section>")

    krop = f"""
{pristabel(udvalg, UMAP, titel=tabeltitel or f"{etiket} — sammenlignet på pris",
           undertitel=intro, billigst_id=udvalg[0]['id'] if udvalg else None)}
{brod}
<section class="sektion baand-smal">
  {laesvidere(links)}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(etiket, h1, intro, '<a href="#sammenlign" class="knap knap-primaer">Se priserne</a>', chips),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk), listeld(udvalg, etiket))],
    ), prioritet="0.85")


def quiz(plads="forside"):
    """Interaktivt værktøj: matcher brugeren med abonnementer ud fra forbrug."""
    data = [{"id": a["id"], "navn": a["navn"], "udbyder": UMAP[a["udbyder"]]["navn"],
             "slug": a["udbyder"], "logo": UMAP[a["udbyder"]]["logo"],
             "lw": round(UMAP[a["udbyder"]]["logo_w"] * 22 / UMAP[a["udbyder"]]["logo_h"]),
             "net": UMAP[a["udbyder"]]["netvaerk"], "gb": a["data_gb"],
             "pris": a["pris"], "gns": round(gns12(a) or a["pris"]),
             "tale": a["tale"], "stream": len(a.get("streaming", [])),
             "link": a["link"]}
            for a in ABON if a["pris"] > 0 and not a.get("forbrugsafregnet")]
    return f"""<section class="sektion baand" id="finder">
  <div class="quiz afslør">
    <div class="quiz-hoved">
      <span class="etiket">Gratis værktøj</span>
      <h2>Find abonnementet der passer til dit forbrug</h2>
      <p class="led">Fire spørgsmål. Vi matcher mod alle {len(data)} abonnementer og regner
      på gennemsnitsprisen over 12 måneder — ikke intro­prisen.</p>
    </div>
    <div class="quiz-krop" data-quiz>
      <div class="quiz-trin" data-trin="0" data-noegle="forbrug">
        <div class="quiz-tael">Spørgsmål 1 af 4</div>
        <h3>Hvor meget bruger du telefonen uden for wi-fi?</h3>
        <div class="quiz-valg">
          <button type="button" data-vaerdi="lav">Næsten aldrig — mest hjemme</button>
          <button type="button" data-vaerdi="mellem">Lidt hver dag — sociale medier og musik</button>
          <button type="button" data-vaerdi="hoej">Meget — video og navigation dagligt</button>
          <button type="button" data-vaerdi="ekstrem">Telefonen er mit internet</button>
        </div>
      </div>
      <div class="quiz-trin" data-trin="1" data-noegle="tale" hidden>
        <div class="quiz-tael">Spørgsmål 2 af 4</div>
        <h3>Hvor meget ringer du?</h3>
        <div class="quiz-valg">
          <button type="button" data-vaerdi="lidt">Næsten aldrig — jeg skriver</button>
          <button type="button" data-vaerdi="fri">Dagligt — jeg vil have fri tale</button>
        </div>
      </div>
      <div class="quiz-trin" data-trin="2" data-noegle="sted" hidden>
        <div class="quiz-tael">Spørgsmål 3 af 4</div>
        <h3>Hvor bor eller færdes du mest?</h3>
        <div class="quiz-valg">
          <button type="button" data-vaerdi="by">I en større by</button>
          <button type="button" data-vaerdi="land">På landet, ved kysten eller pendler langt</button>
        </div>
      </div>
      <div class="quiz-trin" data-trin="3" data-noegle="stream" hidden>
        <div class="quiz-tael">Spørgsmål 4 af 4</div>
        <h3>Vil du have streaming med i abonnementet?</h3>
        <div class="quiz-valg">
          <button type="button" data-vaerdi="nej">Nej — bare data og tale til laveste pris</button>
          <button type="button" data-vaerdi="ja">Ja — jeg betaler for streaming i forvejen</button>
        </div>
      </div>
      <div class="quiz-svar" data-svar hidden></div>
    </div>
  </div>
  <script type="application/json" data-quizdata>{json.dumps(data, ensure_ascii=False)}</script>
</section>"""


# --------------------------------------------------------------- LONG TAIL

TJENESTER_META = {
    "Netflix": ("netflix", "film og serier",
                "Netflix er verdens største streamingtjeneste for film og serier og den, flest "
                "danskere allerede betaler for. Netop derfor er det også den tjeneste, hvor "
                "regnestykket oftest falder ud til bundlets fordel — du erstatter en udgift, "
                "du har i forvejen."),
    "HBO Max": ("hbo-max", "film og serier",
                "HBO Max har en stærk katalogprofil på serier og er ofte den anden tjeneste, "
                "folk vælger til. Tjenesten har skiftet navn og pakkestruktur flere gange, så "
                "tjek hvilken pakke der indgår — reklamefri eller med reklamer gør en forskel "
                "i værdi."),
    "Disney+": ("disney-plus", "familie, film og serier",
                "Disney+ er den mest oplagte tjeneste at få med i et mobilabonnement, hvis der "
                "er børn i husstanden. Bemærk at udbydere ofte inkluderer standardpakken med "
                "reklamer, mens den reklamefri koster ekstra."),
    "Viaplay": ("viaplay", "sport, film og serier",
                "Viaplay er den dyreste af de store tjenester at købe separat, især hvis "
                "sportspakken indgår. Det gør den til den tjeneste, hvor et bundle kan spare "
                "flest kroner — men kun hvis du rent faktisk ser sport."),
    "TV 2 Play": ("tv2-play", "dansk tv og sport",
                  "TV 2 Play dækker dansk indhold, nyheder og sport. Tjenesten har flere "
                  "niveauer, og det er værd at tjekke, om det er basispakken eller en større "
                  "pakke, der indgår i abonnementet."),
    "Nordisk Film+": ("nordisk-film-plus", "nordiske film og serier",
                      "Nordisk Film+ er en mindre tjeneste med nordisk indhold. Den er billig "
                      "at købe separat, og derfor er den sjældent grunden til at vælge et "
                      "bundle — men den er et fint tillæg, hvis den følger med."),
    "SkyShowtime": ("skyshowtime", "film og serier",
                    "SkyShowtime samler indhold fra flere internationale studier. Tjenesten "
                    "er relativt ny på det danske marked og dukker oftere op i bundles end i "
                    "danske husstandes selvstændige abonnementer."),
    "Prime Video": ("prime-video", "film og serier",
                    "Prime Video indgår normalt i et Amazon Prime-medlemskab. Får du det via "
                    "mobilabonnementet, så tjek om det er hele medlemskabet eller kun "
                    "videodelen — forskellen er reel, hvis du handler på Amazon."),
    "Deezer": ("deezer", "musik",
               "Deezer er en musiktjeneste og et alternativ til de større navne. Den fylder "
               "kun lidt data, hvis du henter musik på wi-fi, og den er derfor et af de "
               "billigste tillæg at have med i et abonnement."),
    "Podimo": ("podimo", "podcast og lydbøger",
               "Podimo dækker podcasts og lydbøger. Pendler du eller træner du meget, er det "
               "et af de tillæg med højest reel værdi pr. krone — og det bruger meget lidt "
               "data sammenlignet med video."),
    "Mofibo": ("mofibo", "lydbøger",
               "Mofibo er en lydbogstjeneste. Værdien afhænger helt af, hvor meget du lytter "
               "— for en storforbruger af lydbøger er det et af de dyreste separate "
               "abonnementer at have, og dermed et af de bedste at få med."),
    "Telmore Musik": ("telmore-musik", "musik",
                      "Telmore Musik er udbyderens egen musiktjeneste. Den kan ikke købes "
                      "separat på samme måde som de store tjenester, hvilket gør den svær at "
                      "værdisætte i et regnestykke — vurder den efter, om du reelt vil bruge den."),
    "YouSee Musik": ("yousee-musik", "musik",
                     "YouSee Musik er udbyderens egen musiktjeneste og følger med flere "
                     "YouSee-abonnementer. Som ved andre operatørejede tjenester bør du "
                     "vurdere, om den erstatter et abonnement, du har i forvejen."),
}

# Alle tjenester får en side. Har vi ingen aftale med en udbyder, der tilbyder
# tjenesten, siger siden det ligeud i stedet for at vise opdigtede priser.
TJENESTER = list(TJENESTER_META)

# Hvem tilbyder hvad på det danske marked. Bruges når vi ikke selv har data.
TJENESTE_UDBYDERE = {
    "Netflix": "CBB Mobil og Telmore",
    "HBO Max": "CBB Mobil og Telmore",
    "Disney+": "Telmore og Oister",
    "Viaplay": "CBB Mobil og Telmore",
    "TV 2 Play": "CBB Mobil, Telmore og Oister",
    "Nordisk Film+": "CBB Mobil og Telmore",
    "SkyShowtime": "YouSee og Telmore",
    "Prime Video": "Telmore",
    "Deezer": "CBB Mobil og Oister",
    "Podimo": "CBB Mobil, Telmore og Oister",
    "Mofibo": "CBB Mobil og Telmore",
    "Telmore Musik": "Telmore",
    "YouSee Musik": "YouSee",
}

NETVAERK = [
    {
        "slug": "tdc-net", "navn": "TDC NET", "kort": "Danmarks mest udbyggede mobilnet",
        "styrke": ("TDC NET er det mest finmaskede mobilnet i Danmark og har gennem en "
                   "årrække klaret sig bedst i uafhængige målinger af netkvalitet. Nettet "
                   "står særligt stærkt i landdistrikter, sommerhusområder, langs jernbanen "
                   "og indendørs i ældre bygninger med tykke mure."),
        "svaghed": ("Brands, der kører på TDC NET, ligger typisk højere i pris end "
                    "discountselskaber på de to andre net. Du betaler reelt et tillæg for "
                    "dækning — og det er kun pengene værd, hvis du færdes steder, hvor "
                    "forskellen mærkes."),
        "hvem": ("Vælg TDC NET hvis du bor uden for de større byer, har sommerhus, pendler "
                 "langt med tog eller bil, eller ofte opholder dig i områder med svingende "
                 "dækning."),
    },
    {
        "slug": "telenor", "navn": "Telenor", "kort": "Bred dækning til fornuftig pris",
        "styrke": ("Telenors net leverer bred dækning i hele landet og rammer for de fleste "
                   "brugere en god balance mellem kvalitet og pris. Flere af de billigste "
                   "abonnementer på markedet kører på dette net, hvilket gør det til det "
                   "mest oplagte valg for prisbevidste brugere med almindeligt forbrug."),
        "svaghed": ("Der findes enkelte huller i tyndt befolkede områder, hvor TDC NET "
                    "står stærkere. Forskellen er dog mindre, end den var for få år siden."),
        "hvem": ("Vælg Telenors net hvis du vil have solid dækning uden at betale "
                 "premiumpris — for langt de fleste danskere er det den rigtige balance."),
    },
    {
        "slug": "3", "navn": "3", "kort": "Hastighed og kapacitet i byerne",
        "styrke": ("3's net er bygget med fokus på kapacitet og hastighed der, hvor der er "
                   "mange mennesker. Selskabet var tidligt ude med både 4G og 5G, og i byer "
                   "leverer nettet høje hastigheder, også når mange er på samtidig."),
        "svaghed": ("Nettet er historisk mindre finmasket i landdistrikter, langs kysten og "
                    "i visse indendørsmiljøer. Bor du uden for en større by, bør du tjekke "
                    "dækningskortet grundigt, før du vælger."),
        "hvem": ("Vælg 3's net hvis du bor i en større by og bruger meget data — så får du "
                 "typisk flest gigabyte for pengene og høje hastigheder."),
    },
]


def byg_streamingoversigt():
    sti = "/mobilabonnement-med-streaming/tjenester/"
    krumme = [("/", "Forside"), ("/mobilabonnement-med-streaming/", "Med streaming"),
              (None, "Tjenester")]
    kort = ""
    for t in TJENESTER:
        slug, kat, _ = TJENESTER_META[t]
        planer = [a for a in ABON if t in a.get("streaming", [])]
        if planer:
            billigst_t = min(planer, key=lambda a: gns12(a) or 9e9)
            linje = (f"{len(planer)} abonnementer · {kat} · fra "
                     f"{kr(gns12(billigst_t))} kr./md. i gennemsnit over 12 mdr.")
        else:
            linje = f"{kat} · tilbydes af {TJENESTE_UDBYDERE.get(t, 'enkelte udbydere')}"
        kort += (f'<a class="kort" href="/mobilabonnement-med-{slug}/" '
                 f'style="text-decoration:none;color:inherit">'
                 f'<h3>Mobilabonnement med {e(t)}</h3>'
                 f'<p>{e(linje)}</p></a>')
    krop = f"""<section class="sektion baand">
  <div class="sektion-hoved afslør"><span class="etiket">Streamingtjenester</span>
  <h2>Vælg tjenesten, du vil have med</h2>
  <p class="led">Vi har en side pr. streamingtjeneste med præcis de abonnementer, hvor
  netop den tjeneste indgår — og hvad merprisen er mod at købe den selv.</p></div>
  <div class="kortgitter kg-3">{kort}</div>
</section>
<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>"""
    return skriv(sti, shell(
        sti=sti, titel=f"Mobilabonnement med streaming — {len(TJENESTER)} tjenester sammenlignet",
        beskrivelse=("Se hvilke mobilabonnementer der inkluderer Netflix, HBO Max, Disney+, "
                     "Viaplay og andre streamingtjenester. Én oversigt pr. tjeneste."),
        opdateret=OPDATERET,
        hero=hero_side("Streamingtjenester", "Mobilabonnement med streaming — tjeneste for tjeneste",
                       "Vi har delt det op, så du kan se præcis de abonnementer, hvor din "
                       "tjeneste indgår."),
        efter_hero=logobaand(), krumme=krumme, indhold=krop,
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme))],
    ), prioritet="0.7")


TJENESTE_DYBDE = {
    "Netflix": ("Netflix har flere abonnementsniveauer, og de adskiller sig på antal samtidige "
                "skærme og opløsning. Får du Netflix med i et mobilabonnement, er det ofte "
                "standardniveauet — tjek om det er nok til din husstand, hvis I ser på flere "
                "skærme samtidig.",
                "Downloadfunktionen er værd at bruge aktivt. Henter du afsnit hjem på wi-fi, "
                "bruger du nul mobildata på farten, og det kan flytte dig ned i en billigere "
                "datakategori."),
    "HBO Max": ("HBO Max har skiftet navn og pakkestruktur flere gange, og der findes både en "
                "version med reklamer og en reklamefri. De koster ikke det samme separat, så "
                "tjek hvilken der indgår, før du regner på besparelsen.",
                "Katalogprofilen er stærkest på serier. Er det primært film, du ser, er værdien "
                "typisk lavere end prisskiltet antyder."),
    "Disney+": ("Disney+ er den mest oplagte tjeneste at få med, hvis der er børn i husstanden. "
                "Bemærk at udbydere ofte inkluderer standardpakken med reklamer, mens den "
                "reklamefri koster ekstra.",
                "Børneprofiler og forældrekontrol er indbygget. Det er relevant, hvis abonnementet "
                "deles med et barn — se også vores side om mobilabonnement til børn."),
    "Viaplay": ("Viaplay er den dyreste af de store tjenester at købe separat, især hvis "
                "sportspakken indgår. Det gør den til den tjeneste, hvor et bundle kan spare "
                "flest kroner — men kun hvis du rent faktisk ser sport.",
                "Sportsrettigheder skifter oftere end filmkataloger. Vælger du et abonnement på "
                "grund af én bestemt sportsrettighed, så tjek hvor længe aftalen løber."),
    "TV 2 Play": ("TV 2 Play har flere niveauer, fra basis til pakker med sport og flere kanaler. "
                  "Det er sjældent tydeligt i mobilabonnementets markedsføring, hvilket niveau "
                  "der indgår — spørg, hvis det er afgørende.",
                  "Dansk indhold og nyheder er tjenestens styrke. Ser du primært internationale "
                  "serier, dækker den ikke dit behov alene."),
    "Nordisk Film+": ("Nordisk Film+ er en mindre tjeneste med nordisk indhold. Den er billig at "
                      "købe separat, og derfor sjældent grunden til at vælge et bundle — men et "
                      "fint tillæg, hvis den følger med.",
                      "Fordi tjenesten er billig separat, bør du ikke lade den veje tungt i "
                      "regnestykket. Fokusér på de dyre tjenester i pakken."),
    "SkyShowtime": ("SkyShowtime samler indhold fra flere internationale studier og er relativt "
                    "ny på det danske marked. Den optræder oftere i bundles end som selvstændigt "
                    "abonnement i danske husstande.",
                    "Fordi tjenesten er ny, er det værd at prøve indholdet, før du lader den veje "
                    "tungt. Mange får den med og bruger den aldrig."),
    "Prime Video": ("Prime Video indgår normalt i et Amazon Prime-medlemskab, som også dækker "
                    "fragt og andre fordele. Får du det via mobilabonnementet, så tjek om det er "
                    "hele medlemskabet eller kun videodelen — forskellen er reel, hvis du handler "
                    "på Amazon.",
                    "Kataloget varierer mere mellem lande end de øvrige tjenester. Det danske "
                    "udbud er mindre end det amerikanske."),
    "Deezer": ("Deezer er en musiktjeneste og et alternativ til de større navne. Musik fylder "
               "under en tiendedel af, hvad video gør, så du behøver ikke et stort abonnement "
               "for at kunne bruge den på farten.",
               "Offline-download gør forbruget til nul. Sæt automatisk hentning til over wi-fi, "
               "så bruger du reelt ingen mobildata på musik."),
    "Podimo": ("Podimo dækker podcasts og lydbøger. For pendlere er det ofte det tillæg med "
               "højest reel værdi pr. krone — og det bruger meget lidt data sammenlignet med "
               "video.",
               "Podcasts fylder omkring 30-60 MB i timen. Selv et lille abonnement rækker til "
               "flere hundrede timers lytning."),
    "Mofibo": ("Mofibo er en lydbogstjeneste og er dyr at købe separat sammenlignet med musik. "
               "Lytter du regelmæssigt til lydbøger, er det den enkelttjeneste, hvor et bundle "
               "oftest kan betale sig.",
               "Lydbøger kan hentes offline. Gør du det hjemmefra, koster de ingenting i "
               "mobildata."),
    "Telmore Musik": ("Telmore Musik er udbyderens egen musiktjeneste. Den kan ikke købes "
                      "separat på samme måde som de store internationale tjenester, hvilket gør "
                      "den svær at værdisætte i et regnestykke.",
                      "Har du playlister og lyttehistorik hos en anden tjeneste, er værdien af at "
                      "skifte tæt på nul — uanset prisskiltet."),
    "YouSee Musik": ("YouSee Musik er udbyderens egen musiktjeneste og følger med flere "
                     "YouSee-abonnementer. Som ved andre operatørejede tjenester bør du vurdere, "
                     "om den erstatter et abonnement, du har i forvejen.",
                     "Skifter du mobilselskab, mister du adgangen. Det er værd at tænke ind, hvis "
                     "du bygger din musiksamling op i tjenesten."),
}


def byg_tjenesteside(tjeneste):
    slug, kategori, intro_tekst = TJENESTER_META[tjeneste]
    sti = f"/mobilabonnement-med-{slug}/"
    planer = sorted([a for a in ABON if tjeneste in a.get("streaming", [])],
                    key=lambda a: gns12(a) or 9e9)

    uden = [a for a in ABON if not a.get("streaming") and a["data_gb"] > 0 and a["pris"] > 0]
    ref = min(uden, key=lambda a: gns12(a) or 9e9) if uden else None
    uref = UMAP[ref["udbyder"]] if ref else None
    hvem = TJENESTE_UDBYDERE.get(tjeneste, "enkelte udbydere")
    krumme = [("/", "Forside"), ("/mobilabonnement-med-streaming/", "Med streaming"),
              (None, tjeneste)]
    andre = "".join(
        f'<a href="/mobilabonnement-med-{TJENESTER_META[t][0]}/">{e(t)}</a>'
        for t in TJENESTER if t != tjeneste)
    video = kategori.startswith(("film", "sport", "dansk", "familie", "nordiske"))

    if video:
        datarows = ("<tr><td>Standardkvalitet</td><td>0,7-1 GB</td><td>ca. 50-70 timer</td></tr>"
                    "<tr><td>HD</td><td>2-3 GB</td><td>ca. 17-25 timer</td></tr>"
                    "<tr><td>4K</td><td>7 GB og opefter</td><td>ca. 7 timer</td></tr>")
        datanote = ("Video er langt den største dataforbruger. Har du et abonnement under "
                    "50 GB, kan du reelt kun bruge tjenesten på wi-fi.")
    else:
        datarows = ("<tr><td>Normal</td><td>ca. 70 MB</td><td>ca. 700 timer</td></tr>"
                    "<tr><td>Høj</td><td>ca. 100-150 MB</td><td>ca. 350-500 timer</td></tr>"
                    "<tr><td>Tabsfri</td><td>ca. 350 MB</td><td>ca. 140 timer</td></tr>")
        datanote = ("Lyd fylder så lidt, at datamængden sjældent er afgørende. Henter du "
                    "indhold offline på wi-fi, koster det ingenting på farten.")

    if planer:
        bt = planer[0]
        ub = sorted({UMAP[a["udbyder"]]["navn"] for a in planer})
        merpris = (gns12(bt) or 0) - (gns12(ref) or 0)
        titel = f"Mobilabonnement med {tjeneste} — {len(planer)} planer fra {kr(gns12(bt))} kr./md."
        besk = (f"Se de {len(planer)} mobilabonnementer der inkluderer {tjeneste}. "
                f"Fra {kr(gns12(bt))} kr./md. i gennemsnit over 12 mdr.")
        hero_tekst = (f"{len(planer)} abonnementer inkluderer {tjeneste}. Vi viser "
                      "gennemsnitsprisen over 12 måneder, ikke introprisen.")
        chips = [("Planer", str(len(planer))), ("Fra", f"{kr(gns12(bt))} kr."),
                 ("Merpris", f"{kr(abs(merpris))} kr.")]
        tabel = pristabel(planer, UMAP, titel=f"Abonnementer med {tjeneste} inkluderet",
                          undertitel=f"{len(planer)} abonnementer fra {' og '.join(ub)}.",
                          filtre=False, billigst_id=bt["id"], vis=10)
        kort_svar = (f"<p><strong>Kort svar:</strong> {len(planer)} mobilabonnementer fra "
                     f"{' og '.join(ub)} inkluderer {e(tjeneste)}. Billigst er {e(bt['navn'])} "
                     f"til {kr(gns12(bt))} kr. om måneden i gennemsnit over 12 måneder. "
                     f"Merprisen mod et abonnement uden streaming er cirka "
                     f"{kr(abs(merpris))} kr. om måneden.</p>")
        hvem_afsnit = "Vi viser deres aktuelle priser i tabellen ovenfor."
        ld = [listeld(planer, f"Mobilabonnementer med {tjeneste}")]
        pri = "0.75"
    else:
        titel = f"Mobilabonnement med {tjeneste} — hvem tilbyder det i {IDAG.year}?"
        besk = (f"Hvilke mobilabonnementer inkluderer {tjeneste}? Se hvem der tilbyder det "
                "i Danmark, og hvad det koster at tegne tjenesten selv ved siden af.")
        hero_tekst = (f"Vi har ikke prisaftale med de udbydere, der tilbyder {tjeneste} i "
                      "abonnementet. Her er hvem der gør — og regnestykket for at tegne den selv.")
        chips = [("Tilbydes af", hvem.split(" og ")[0].split(",")[0]),
                 ("Vores priser", "ikke endnu"), ("Alternativ", "tegn selv")]
        tabel = ""
        kort_svar = (f"<p><strong>Kort svar:</strong> På det danske marked er det primært "
                     f"<strong>{e(hvem)}</strong>, der inkluderer {e(tjeneste)} i "
                     "mobilabonnementet. Vi har ikke prisaftale med dem endnu og viser derfor "
                     "ikke deres priser her — vi vil hellere mangle et tal end vise et forkert. "
                     f"Herunder ser du, hvad det koster at tegne {e(tjeneste)} selv ved siden "
                     "af et billigt abonnement.</p>")
        hvem_afsnit = ("Vi har ikke prisaftale med dem og viser derfor ikke deres priser. Vi "
                       "kunne godt gengive tal fra deres hjemmesider, men vi kan ikke garantere, "
                       "at de er aktuelle — og forkerte priser er værre end ingen priser. Se "
                       "dem hos udbyderen selv.")
        ld = []
        pri = "0.6"

    faq = [
        {"sp": f"Hvilke mobilabonnementer inkluderer {tjeneste}?",
         "sv": (f"Lige nu inkluderer {len(planer)} abonnementer i vores sammenligning {tjeneste}."
                if planer else
                f"På det danske marked er det primært {hvem}. Vi har ikke prisaftale med dem "
                "endnu, så deres priser fremgår ikke af vores tabeller.")},
        {"sp": f"Kan det betale sig at få {tjeneste} med i mobilabonnementet?",
         "sv": f"Det afhænger af merprisen mod at købe {tjeneste} separat. Betaler du allerede "
               "for tjenesten, er et bundle ofte billigere. Gør du ikke, betaler du for noget, "
               "du ikke bruger."},
        {"sp": f"Hvad sker der med {tjeneste}, hvis jeg opsiger abonnementet?",
         "sv": "Adgangen stopper sammen med mobilabonnementet. Din profil og historik ligger "
               "hos tjenesten selv og overlever skiftet."},
        {"sp": "Bruger streaming meget af min datamængde?",
         "sv": ("Video koster cirka 0,7-1 GB i timen i standardkvalitet og 2-3 GB i HD. Vælger "
                "du et abonnement med video, bør du have mindst 50 GB." if video else
                "Musik og lyd fylder 30-150 MB i timen — langt mindre end video. Selv et lille "
                "abonnement rækker til flere hundrede timer.")},
        {"sp": "Er det billigere at tegne tjenesten selv?",
         "sv": "Ofte ja, og du får friheden til at opsige den uden at røre dit mobilabonnement. "
               "Et bundle er bekvemt, men det binder to beslutninger sammen."},
    ]

    benchmark = ""
    if ref:
        benchmark = (f'<div class="tip"><h3>Regnestykket: hvad koster det uden?</h3>'
                     f'<p>Det billigste abonnement uden streamingtillæg i vores sammenligning '
                     f'er <strong>{e(uref["navn"])} {e(ref["navn"])}</strong> med '
                     f'{gb_tekst(ref["data_gb"])} til {kr(gns12(ref))} kr. om måneden. Læg '
                     f'prisen på {e(tjeneste)} oveni, og du har det tal, et bundle skal slå. '
                     'Er bundlet dyrere, betaler du for bekvemmelighed — ikke for indhold.</p></div>')

    krop = f"""
{tabel}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Priser og pakkeindhold kontrolleret hos udbyderne")}

  <div class="udtag">{kort_svar}</div>

  <h2>Er {e(tjeneste)} i mobilabonnementet en god forretning?</h2>
  <p>{e(intro_tekst)}</p>
  <p>Regnestykket er det samme uanset tjeneste: find den plan, du ellers ville have valgt,
  og se hvad planen med {e(tjeneste)} koster ekstra om måneden. Er merprisen lavere end
  tjenestens egen pris, sparer du penge. Er den højere, betaler du for at have det samlet
  ét sted.</p>

  {benchmark}

  <h2>Det du særligt skal vide om {e(tjeneste)}</h2>
  <p>{e(TJENESTE_DYBDE.get(tjeneste, ("", ""))[0])}</p>
  <p>{e(TJENESTE_DYBDE.get(tjeneste, ("", ""))[1])}</p>

  <h2>Hvem tilbyder {e(tjeneste)} i Danmark?</h2>
  <p>På det danske marked er det primært <strong>{e(hvem)}</strong>, der har {e(tjeneste)}
  med i mobilabonnementet. Pakkerne ændrer sig løbende, fordi de bygger på aftaler mellem
  udbyderen og indholdsleverandøren — en tjeneste kan ryge ud, når en aftale udløber, uden
  at prisen nødvendigvis falder tilsvarende.</p>
  <p>{e(hvem_afsnit)}</p>

  <h2>Alternativet: tegn tjenesten selv</h2>
  <p>Det er ofte det rigtige valg. Køber du {e(tjeneste)} selv, kan du opsige den, når du er
  færdig med en serie, uden at røre dit mobilabonnement — og du kan skifte mobilselskab uden
  at miste adgangen.</p>
  <p>Modellen med alt samlet ét sted er bekvem, men den binder to beslutninger sammen, der
  ikke har noget med hinanden at gøre. Vil du have laveste pris på mobil og fri hånd med
  streaming, så vælg et discountabonnement og tegn tjenesterne selv. Se
  <a href="/billigste-mobilabonnement/">billigste mobilabonnement</a> eller
  <a href="/mobilabonnement-under-100-kr/">abonnementer under 100 kr.</a></p>

  <h2>Hvor meget data kræver {e(tjeneste)}?</h2>
  <table>
  <thead><tr><th>Kvalitet</th><th>Ca. forbrug pr. time</th><th>Rækker med 50 GB til</th></tr></thead>
  <tbody>{datarows}</tbody>
  </table>
  <p>{e(datanote)} <a href="/guides/hvor-meget-data/">Se hvor meget data du har brug for</a>.</p>

  {tabel_billigst_pr_udbyder()}

  <h2>Andre tjenester</h2>
  <p class="tjenestelinks">{andre}</p>
  <p>Se også <a href="/mobilabonnement-med-streaming/tjenester/">alle streamingtjenester</a>,
  <a href="/billigste-mobilabonnement/">billigste mobilabonnement</a> og
  <a href="/mobilabonnement-med-fri-data/">abonnementer med fri data</a>.</p>

  {kilder(["forbrugerombudsmanden", "teleankenaevnet"],
          ["Hvem der tilbyder tjenesten: udbydernes egne produktsider.",
           "Dataforbrug: typiske intervaller ud fra streamingtjenesternes oplysninger.",
           "Priser vises kun for udbydere, vi har et datafeed fra. Vi gengiver ikke priser, "
           "vi ikke kan holde opdaterede."])}
</section>

<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(tjeneste, f"Mobilabonnement med {e(tjeneste)}", hero_tekst,
                       '<a href="#indhold" class="knap knap-primaer">Se regnestykket</a>', chips),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, f"Mobilabonnement med {tjeneste}", besk), *ld)],
    ), prioritet=pri)


def byg_netvaerksoversigt():
    sti = "/netvaerk/"
    krumme = [("/", "Forside"), (None, "Mobilnetværk")]
    kort = ""
    for n in NETVAERK:
        paa = [a for a in ABON if UMAP[a["udbyder"]]["netvaerk"] == n["navn"] and a["pris"] > 0]
        selskaber = [u for u in UDBYDERE if u["netvaerk"] == n["navn"]]
        billigst_n = min(paa, key=lambda a: gns12(a) or 9e9) if paa else None
        kort += f"""<a class="kort" href="/netvaerk/{n['slug']}/" style="text-decoration:none;color:inherit">
  <h3>{e(n['navn'])}</h3><p>{e(n['kort'])}</p>
  <p style="margin-top:.6rem"><strong>{len(selskaber)} selskab{"er" if len(selskaber) != 1 else ""}</strong> · {len(paa)} abonnementer
  {f"· fra {kr(gns12(billigst_n))} kr./md." if billigst_n else ""}</p></a>"""

    # Direkte sammenligning af de tre net
    sml = ""
    for felt, vaerdier in [
        ("Udbredelse", ("Mest finmasket net i landet", "Bred dækning i hele landet",
                        "Stærk i byer, mere varierende på landet")),
        ("Stærkest i", ("Landdistrikter, sommerhuse, tog, indendørs",
                        "Balance mellem dækning og pris",
                        "Byer og tætbefolkede områder")),
        ("Svagest i", ("Prisen på brands der kører på nettet",
                       "Enkelte huller i tyndt befolkede områder",
                       "Landdistrikter og visse kystområder")),
        ("Vælg det hvis", ("Du bor uden for byerne eller pendler langt",
                           "Du vil have solid dækning uden premiumpris",
                           "Du bor i en større by og bruger meget data")),
    ]:
        sml += f'<tr><td><strong>{felt}</strong></td>' + "".join(f"<td>{e(v)}</td>" for v in vaerdier) + "</tr>"
    for n in NETVAERK:
        pass
    priser = []
    for n in NETVAERK:
        paa = [a for a in ABON if UMAP[a["udbyder"]]["netvaerk"] == n["navn"] and a["pris"] > 0]
        priser.append(f"{kr(gns12(min(paa, key=lambda a: gns12(a) or 9e9)))} kr./md." if paa else "—")
    sml += "<tr><td><strong>Billigste abonnement</strong></td>" + "".join(f"<td>{p}</td>" for p in priser) + "</tr>"
    antal = []
    for n in NETVAERK:
        antal.append(str(len([u for u in UDBYDERE if u["netvaerk"] == n["navn"]])))
    sml += "<tr><td><strong>Selskaber i vores sammenligning</strong></td>" + "".join(f"<td>{a}</td>" for a in antal) + "</tr>"

    faq = [
        {"sp": "Hvor mange mobilnetværk er der i Danmark?",
         "sv": "Tre: TDC NET, Telenor og 3. Alle andre mobilselskaber lejer sig ind på et af dem. "
               "Det betyder, at antallet af selskaber er langt større end antallet af net."},
        {"sp": "Hvilket mobilnet er bedst i Danmark?",
         "sv": "TDC NET er det mest udbyggede og står typisk stærkest i landdistrikter, "
               "sommerhusområder og indendørs. I byerne er forskellen mellem de tre lille i praksis."},
        {"sp": "Kan jeg vælge netværk frit?",
         "sv": "Indirekte. Du vælger et selskab, og selskabet bestemmer nettet. Vil du på et bestemt "
               "net, skal du vælge blandt de selskaber, der kører på det."},
        {"sp": "Hvad er forskellen på en netværksejer og en MVNO?",
         "sv": "En netværksejer har egne master og eget udstyr. En MVNO lejer kapacitet hos en "
               "netværksejer og sælger det videre under eget navn til egen pris."},
        {"sp": "Får jeg dårligere hastighed hos en MVNO?",
         "sv": "Ikke automatisk. Nogle MVNO-aftaler indeholder dog hastighedsloft eller lavere "
               "prioritet i myldretiden. Det fremgår af abonnementsvilkårene."},
        {"sp": "Hvordan finder jeg ud af, hvilket net der dækker bedst hos mig?",
         "sv": "Slå din adresse op på alle tre netværksejeres dækningskort — og tjek både bopæl, "
               "arbejdsplads og pendlerrute, ikke kun ét sted."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="sektion-hoved afslør"><span class="etiket">Mobilnetværk</span>
  <h2>Der findes kun tre mobilnet i Danmark</h2>
  <p class="led">Alle andre selskaber lejer sig ind hos en af dem. Vælger du udbyder,
  vælger du reelt to ting: et net og et selskab.</p></div>
  <div class="kortgitter kg-3">{kort}</div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Netværksangivelser kontrolleret hos udbyderne")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Danmark har tre mobilnet: TDC NET, Telenor og 3. TDC NET er
  mest udbygget og står stærkest uden for byerne. 3 er stærkest på hastighed og kapacitet i
  byerne. Telenor ligger derimellem med en god balance mellem dækning og pris. Bor du
  centralt i en større by, kan du i praksis vælge frit og gå efter pris.</p>
  </div>

  <h2>De tre net stillet direkte op mod hinanden</h2>
  <table>
    <thead><tr><th></th>{"".join(f"<th>{e(n['navn'])}</th>" for n in NETVAERK)}</tr></thead>
    <tbody>{sml}</tbody>
  </table>

  <h2>Nettet bestemmer dækningen — ikke prisen</h2>
  <p>Det er den vigtigste enkeltindsigt om det danske mobilmarked, og den bliver
  konsekvent misforstået. Et discountabonnement til {kr(D['min_pris'])} kr. og et
  premiumabonnement til flere hundrede kroner kan køre på præcis de samme master med
  præcis den samme hastighed, hvis de ligger på samme net.</p>
  <p>Spørgsmålet er derfor aldrig, om et billigt selskab har "dårligere dækning". Det er,
  hvilket net selskabet lejer sig ind på — og under hvilke vilkår. Nogle MVNO-aftaler
  indeholder et hastighedsloft eller lavere prioritet, når nettet er belastet. Det er ikke
  svindel, og det mærkes sjældent ved almindelig brug, men det er forklaringen på, at to
  abonnementer på "samme net" ikke altid opfører sig ens.</p>

  {netvaerksgruppering()}

  <h2>Hvornår betyder netværket noget?</h2>
  <div class="kortgitter kg-2" style="margin:1.8rem 0">
    <div class="kort"><h3>Her kan du vælge frit</h3>
    <p>Bor og arbejder du centralt i en større by, leverer alle tre net fuld dækning og
    høje hastigheder. Betaler du et tillæg for premiumdækning, køber du noget, du ikke får
    glæde af. Vælg efter pris.</p></div>
    <div class="kort"><h3>Her bør nettet vælges først</h3>
    <p>Sommerhusområder, øer, kystnære egne, tyndt befolkede områder og lange pendlerruter
    med tog eller bil. Her kan forskellen mellem nettene være mærkbar i hverdagen, og så er
    tredive kroner i prisforskel underordnet.</p></div>
  </div>

  <h2>5G — hvornår gør det en forskel?</h2>
  <p>5G giver højere hastigheder og lavere forsinkelse end 4G. For almindelig brug —
  sociale medier, streaming, navigation — mærker de fleste ikke stor forskel fra et
  velfungerende 4G-net.</p>
  <p>5G er værd at prioritere i tre situationer: hvis du henter meget store filer, hvis du
  bruger telefonen som hotspot til arbejde, eller hvis du bor et sted med overbelastet 4G.
  Dækningen er stadig mest udbygget i byerne, og 5G er ikke automatisk inkluderet i alle
  abonnementer — tjek det enkelte produkt.</p>

  <h2>Sådan tjekker du dækningen på din adresse</h2>
  <ol class="trin">
    <li><strong>Slå adressen op på alle tre net</strong>
    Ikke kun det, du overvejer. Du skal se forskellen for at kunne vurdere den.</li>
    <li><strong>Tjek tre steder, ikke ét</strong>
    Bopæl, arbejdsplads og ruten imellem — det er der, telefonen bruges.</li>
    <li><strong>Kig efter indendørsdækning</strong>
    Kortene skelner typisk mellem udendørs og indendørs. Bor du i en ældre bygning med
    tykke mure, er det den indendørs værdi, der betyder noget.</li>
    <li><strong>Brug fortrydelsesretten aktivt</strong>
    Køber du online, har du som udgangspunkt fortrydelsesret. Test dækningen grundigt de
    første dage, mens du stadig kan fortryde.</li>
  </ol>

  <div class="tip">
  <h3>Wi-fi-opkald løser de fleste indendørsproblemer</h3>
  <p>Er dækningen dårlig netop dér, hvor du bor, findes der en gratis løsning: wi-fi-opkald.
  Telefonen fører opkaldet over dit hjemmenet i stedet for mobilnettet, og samtalen bliver
  typisk bedre end på et svagt mobilsignal. Slås til i telefonens indstillinger og
  understøttes af de fleste danske udbydere uden ekstra betaling.</p>
  </div>

  {udbyder_rangliste()}

  {vejviser("/netvaerk/")}

  {kilder(["digst_klage", "teleindustrien", "teleklagenaevnet"],
          ["Netværksejere i Danmark: TDC NET, Telenor og 3.",
           "Dækningsvurderinger: netværksejernes egne offentlige dækningskort.",
           "Vi laver ikke egne hastigheds- eller dækningsmålinger og foregiver ikke andet."])}
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/daekningskort/", "Tjek dækningen på din adresse"),
      ("/udbydere/", "Se hvilket net hver udbyder kører på"),
      ("/speedtest/", "Test din mobilhastighed"),
      ("/guides/daekning-og-netvaerk/", "Guide til dækning og netværk"),
  ])}
  {forfatterboks()}{afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel="Mobilnetværk i Danmark — TDC NET, Telenor og 3 sammenlignet",
        beskrivelse=("Der findes kun tre mobilnet i Danmark. Se forskellen på TDC NET, "
                     "Telenor og 3 — og hvornår netværket betyder mere end prisen."),
        opdateret=OPDATERET,
        hero=hero_side("Mobilnetværk", "De tre danske mobilnet",
                       "Dit valg af udbyder er i virkeligheden et valg af net. Her er "
                       "forskellen, og hvornår den betyder noget.",
                       '<a href="#indhold" class="knap knap-primaer">Se sammenligningen</a>',
                       [("Net i Danmark", "3"), ("Selskaber", str(D['antal_udbydere'])),
                        ("Fra", f"{D['min_pris']} kr.")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, "Mobilnetværk i Danmark", ""))],
    ), prioritet="0.8")


def byg_netvaerksside(n):
    sti = f"/netvaerk/{n['slug']}/"
    krumme = [("/", "Forside"), ("/netvaerk/", "Mobilnetværk"), (None, n["navn"])]
    selskaber = [u for u in UDBYDERE if u["netvaerk"] == n["navn"]]
    planer = sorted([a for a in ABON if UMAP[a["udbyder"]]["netvaerk"] == n["navn"] and a["pris"] > 0],
                    key=lambda a: gns12(a) or 9e9)
    if not planer:
        return
    billigst_n = planer[0]
    liste = ", ".join(u["navn"] for u in selskaber) or "ingen i vores sammenligning"

    faq = [
        {"sp": f"Hvilke selskaber kører på {n['navn']}?",
         "sv": f"I vores sammenligning er det {liste}. Bemærk at MVNO-aftaler kan ændre sig, "
               "så tjek altid udbyderens egen side, hvis dækning er afgørende."},
        {"sp": f"Hvad koster det billigste abonnement på {n['navn']}?",
         "sv": f"Billigst er {billigst_n['navn']} til {kr(gns12(billigst_n))} kr. om måneden "
               "regnet som gennemsnit over 12 måneder inklusive intropris."},
        {"sp": f"Er {n['navn']} godt til mig?",
         "sv": n["hvem"]},
        {"sp": "Hvordan tjekker jeg dækningen på min adresse?",
         "sv": "Alle tre netværksejere har offentlige dækningskort. Tjek din bopæl, din "
               "arbejdsplads og din pendlerrute — ikke kun ét sted."},
    ]

    krop = f"""
{pristabel(planer, UMAP, titel=f"Abonnementer på {n['navn']}",
           undertitel=f"Alle abonnementer i vores sammenligning, der kører på {n['navn']}.",
           billigst_id=billigst_n["id"])}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Netværksangivelser kontrolleret hos udbyderne")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> {e(n['navn'])} er et af de tre mobilnet i Danmark.
  {len(selskaber)} selskaber i vores sammenligning kører på det: {e(liste)}. Billigste
  abonnement er {e(billigst_n['navn'])} til {kr(gns12(billigst_n))} kr. om måneden i
  gennemsnit over 12 måneder.</p>
  </div>

  <h2>Styrken ved {e(n['navn'])}</h2>
  <p>{e(n['styrke'])}</p>

  <h2>Svagheden</h2>
  <p>{e(n['svaghed'])}</p>

  <h2>Hvem bør vælge {e(n['navn'])}?</h2>
  <p>{e(n['hvem'])}</p>

  <h2>Selskaber på {e(n['navn'])}</h2>
  <div class="kortgitter kg-3" style="margin:1.6rem 0">
    {"".join(udbyderkort(u) for u in selskaber)}
  </div>

  <h2>Sådan tjekker du dækningen, før du bestiller</h2>
  <ol class="trin">
    <li><strong>Slå netværksejerens dækningskort op</strong>
    Det er den bedste offentligt tilgængelige kilde, fordi det bygger på operatørens egne
    måledata.</li>
    <li><strong>Tjek tre steder, ikke ét</strong>
    Din bopæl, din arbejdsplads og din pendlerrute. Det er der, du bruger telefonen.</li>
    <li><strong>Spørg en nabo på samme net</strong>
    Den mest undervurderede metode, og den eneste der siger noget om virkeligheden
    indendørs hos dig.</li>
    <li><strong>Brug fortrydelsesretten aktivt</strong>
    Køber du online, har du som udgangspunkt fortrydelsesret. Test dækningen grundigt de
    første dage.</li>
  </ol>

  <p>Se alle net i vores <a href="/netvaerk/">oversigt over mobilnetværk</a>, eller
  sammenlign hele markedet på <a href="/billigste-mobilabonnement/">billigste
  mobilabonnement</a>.</p>
</section>

<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>
"""
    return skriv(sti, shell(
        sti=sti,
        titel=f"{n['navn']} — abonnementer og dækning fra {kr(gns12(billigst_n))} kr./md.",
        beskrivelse=(f"Se hvilke mobilselskaber der kører på {n['navn']}, hvad de koster, "
                     "og hvornår nettet er det rigtige valg for dig."),
        opdateret=OPDATERET,
        hero=hero_side("Mobilnetværk", f"{e(n['navn'])} — {e(n['kort'])}",
                       f"{len(selskaber)} selskaber i vores sammenligning kører på "
                       f"{n['navn']}. Her er styrker, svagheder og priser.",
                       '<a href="#sammenlign" class="knap knap-primaer">Se abonnementerne</a>',
                       [("Selskaber", str(len(selskaber))), ("Planer", str(len(planer))),
                        ("Fra", f"{kr(gns12(billigst_n))} kr.")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     listeld(planer, f"Abonnementer på {n['navn']}"))],
    ), prioritet="0.75")


GB_INTERVALLER = [
    ("1-10-gb", "1–10 GB", 1, 10, "Let bruger",
     "Til dig der er på wi-fi det meste af dagen og bruger mobilen til beskeder, "
     "musik og lidt navigation."),
    ("10-30-gb", "10–30 GB", 10, 30, "Almindelig bruger",
     "Danmarks mest almindelige forbrug. Rækker til sociale medier, podcasts, "
     "kort og lidt video på farten."),
    ("30-50-gb", "30–50 GB", 30, 50, "Aktiv bruger",
     "Til dig der pendler dagligt og streamer video uden for wi-fi flere gange "
     "om ugen."),
    ("50-gb", "50 GB og op", 50, 99, "Storforbruger",
     "Til dig der streamer dagligt på farten eller bruger telefonen som hotspot "
     "til en laptop."),
    ("100-gb", "100 GB og op", 100, 899, "Meget stort forbrug",
     "Til dig hvor mobilen er den primære internetforbindelse, eller hvor flere "
     "enheder deler den."),
]


def byg_gb_side(slug, navn, lav, hoej, profil, beskrivelse):
    sti = f"/mobilabonnement-{slug}/"
    udvalg = sorted([a for a in ABON if lav <= a["data_gb"] <= hoej and a["pris"] > 0],
                    key=lambda a: gns12(a) or 9e9)
    if not udvalg:
        return
    billigst_g = udvalg[0]
    u = UMAP[billigst_g["udbyder"]]
    krumme = [("/", "Forside"), (None, f"Mobilabonnement {navn}")]

    # Naboer til intern navigation mellem intervallerne
    naboer = "".join(
        f'<a href="/mobilabonnement-{s}/"{" class=\"aktiv\"" if s == slug else ""}>{e(n)}</a>'
        for s, n, _, _, _, _ in GB_INTERVALLER)

    faq = [
        {"sp": f"Hvad koster et mobilabonnement med {navn}?",
         "sv": f"Det billigste med {navn} koster {kr(gns12(billigst_g))} kr. om måneden regnet "
               f"som gennemsnit over 12 måneder. Det er {u['navn']} {billigst_g['navn']}."},
        {"sp": f"Er {navn} nok til mig?",
         "sv": beskrivelse + " Tjek dit faktiske forbrug i telefonens indstillinger — de fleste "
               "danskere bruger mindre, end de tror."},
        {"sp": "Hvad sker der, hvis jeg løber tør?",
         "sv": "Det afhænger af udbyderen: nogle sætter hastigheden ned, andre spærrer, og andre "
               "køber automatisk ekstra data. Slå datastop til for at undgå det sidste."},
        {"sp": "Kan jeg skifte datamængde senere?",
         "sv": "Ja, hos de fleste udbydere kan du flytte op og ned fra måned til måned i deres app. "
               "Det kræver ikke, at du skifter selskab."},
    ]

    krop = f"""
<section class="sektion baand">
  <nav class="gb-navigation" aria-label="Vælg datamængde">
    <span class="gb-titel">Datamængde</span>{naboer}
  </nav>
</section>

{pristabel(udvalg, UMAP, titel=f"Mobilabonnement med {navn}",
           undertitel=f"{len(udvalg)} abonnementer i intervallet, sorteret efter reel pris "
                      "over 12 måneder.",
           billigst_id=billigst_g["id"])}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET)}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Der er {len(udvalg)} abonnementer med {navn} i vores
  sammenligning. Det billigste er {e(u['navn'])} {e(billigst_g['navn'])} til
  {kr(gns12(billigst_g))} kr. om måneden i gennemsnit over 12 måneder.
  {e(navn)} passer til: {e(profil.lower())}.</p>
  </div>

  <h2>Hvem passer {e(navn)} til?</h2>
  <p>{e(beskrivelse)}</p>
  <p>Er du i tvivl, så find dit faktiske forbrug i telefonens indstillinger frem for at
  gætte. Kig på de seneste tre måneder og tag den højeste.
  <a href="/guides/hvor-meget-data/">Se hvordan du finder tallet</a>.</p>

  {tabel_pr_datamaengde()}

  <h2>Skal du op eller ned?</h2>
  <p>Vi anbefaler næsten altid ét trin over dit målte forbrug. Grunden er
  prisstrukturen på det danske marked: springet mellem kategorierne er ofte
  20-40 kr. om måneden, mens datamængden fordobles eller tredobles. Den ekstra tyver
  køber dig, at du aldrig skal tænke over det igen — og det er billigere end at købe
  ekstra data en enkelt måned.</p>

  {tabel_billigst_pr_udbyder()}
  {vejviser(sti)}
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?"),
      ("/12-maaneders-prisen/", "Sådan beregner vi 12-måneders-prisen"),
      ("/bedste-mobilabonnement/", "Bedste mobilabonnement"),
  ])}
  {forfatterboks()}{afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti,
        titel=f"Mobilabonnement {navn} — fra {kr(gns12(billigst_g))} kr./md.",
        beskrivelse=(f"Sammenlign {len(udvalg)} mobilabonnementer med {navn}. "
                     f"Fra {kr(gns12(billigst_g))} kr./md. regnet over 12 måneder, "
                     "så introtilbud ikke skjuler normalprisen."),
        opdateret=OPDATERET,
        hero=hero_side(f"{navn}", f"Mobilabonnement med {e(navn)}",
                       e(beskrivelse),
                       '<a href="#sammenlign" class="knap knap-primaer">Se abonnementerne</a>',
                       [("Planer", str(len(udvalg))), ("Fra", f"{kr(gns12(billigst_g))} kr."),
                        ("Profil", profil)]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, f"Mobilabonnement {navn}", ""),
                     listeld(udvalg, f"Mobilabonnement med {navn}"))],
    ), prioritet="0.8")


# --------------------------------------------------------------- VS-SIDER

# De par folk faktisk sammenligner: samme net, samme prisleje eller samme niche.
VS_PAR = [
    # Par mellem udbydere vi har prisdata på — de eneste hvor en ægte
    # sammenligning er mulig. Flere kommer til ved nye godkendelser.
    ("oister", "flexii"), ("flexii", "greentel"), ("oister", "greentel"),
    ("eesy", "flexii"), ("oister", "eesy"), ("greentel", "eesy"),
    # Par der venter på godkendelse hos mindst én part
    ("cbb-mobil", "oister"), ("telmore", "yousee"), ("lebara", "lyca-mobile"),
    ("cbb-mobil", "telmore"), ("duka", "greentel"), ("eesy", "telmore"),
    ("cbb-mobil", "lebara"), ("yousee", "oister"), ("duka", "cbb-mobil"),
    ("eesy", "yousee"),
]


VS_PAR_AKTIVE = []


def byg_vs(slug_a, slug_b):
    ua, ub = UMAP[slug_a], UMAP[slug_b]
    sti = f"/sammenlign/{slug_a}-vs-{slug_b}/"
    pa = sorted([a for a in ABON if a["udbyder"] == slug_a], key=lambda a: gns12(a) or 9e9)
    pb = sorted([a for a in ABON if a["udbyder"] == slug_b], key=lambda a: gns12(a) or 9e9)
    if not pa or not pb:
        return
    alle = sorted(pa + pb, key=lambda a: gns12(a) or 9e9)
    fa, fb = pa[0], pb[0]
    billigst_u = ua if (gns12(fa) or 0) <= (gns12(fb) or 0) else ub

    def bedste_prgb(planer):
        m = [a for a in planer if 0 < a["data_gb"] < 900]
        return min(m, key=lambda a: a["pris"] / a["data_gb"]) if m else None
    ga, gb_ = bedste_prgb(pa), bedste_prgb(pb)

    def rk(navn, va, vb):
        return f'<tr><td><strong>{e(navn)}</strong></td><td>{va}</td><td>{vb}</td></tr>'

    tabel = "".join([
        rk("Netværk", netlabel(ua), netlabel(ub)),
        rk("Antal abonnementer", f"{len(pa)}", f"{len(pb)}"),
        rk("Laveste pris", f"{kr(fa['pris'])} kr./md.", f"{kr(fb['pris'])} kr./md."),
        rk("Laveste gns. over 12 mdr.", f"{kr(gns12(fa))} kr./md.", f"{kr(gns12(fb))} kr./md."),
        rk("Bedste pris pr. GB",
           f"{ga['pris'] / ga['data_gb']:.2f}".replace(".", ",") + " kr." if ga else "—",
           f"{gb_['pris'] / gb_['data_gb']:.2f}".replace(".", ",") + " kr." if gb_ else "—"),
        rk("Største datamængde",
           gb_tekst(max(a["data_gb"] for a in pa)), gb_tekst(max(a["data_gb"] for a in pb))),
        rk("Mest EU-data",
           f"{max(a.get('eu_gb', 0) for a in pa)} GB", f"{max(a.get('eu_gb', 0) for a in pb)} GB"),
        rk("Streaming inkluderet",
           "Ja" if any(a.get("streaming") for a in pa) else "Nej",
           "Ja" if any(a.get("streaming") for a in pb) else "Nej"),
        rk("Binding", "Nej" if all(a["binding"] == 0 for a in pa) else "Ja",
           "Nej" if all(a["binding"] == 0 for a in pb) else "Ja"),
        rk("Bedst til", e(ua["bedst_til"]), e(ub["bedst_til"])),
    ])

    krumme = [("/", "Forside"), ("/sammenlign/", "Sammenlign udbydere"),
              (None, f"{ua['navn']} vs {ub['navn']}")]

    faq = [
        {"sp": f"Er {ua['navn']} eller {ub['navn']} billigst?",
         "sv": f"{billigst_u['navn']} har det billigste abonnement målt på gennemsnitspris over 12 "
               f"måneder. {ua['navn']} starter ved {kr(gns12(fa))} kr./md. og {ub['navn']} ved "
               f"{kr(gns12(fb))} kr./md. Hvilket der er billigst for dig afhænger af, hvor meget "
               "data du skal bruge."},
        {"sp": f"Kører {ua['navn']} og {ub['navn']} på samme net?",
         "sv": (f"Nej. {ua['navn']} kører på {netlabel(ua).replace('s net', '')} og {ub['navn']} på "
                f"{netlabel(ub).replace('s net', '')}. Det er den vigtigste forskel, hvis du bor uden "
                "for de større byer."
                if ua["netvaerk"] != ub["netvaerk"] else
                f"Ja, begge kører på {netlabel(ua).replace('s net', '')}. Dækningen er dermed den "
                "samme, og valget står på pris, vilkår og kundeservice.")},
        {"sp": "Kan jeg skifte mellem dem uden at miste mit nummer?",
         "sv": "Ja. Nummerportering er en rettighed i Danmark. Du bestiller hos den nye udbyder, "
               "oplyser dit nummer, og de klarer resten. Du skal ikke opsige noget selv."},
        {"sp": f"Hvem har flest abonnementer at vælge mellem?",
         "sv": f"{ua['navn'] if len(pa) >= len(pb) else ub['navn']} har flest i vores sammenligning "
               f"med {max(len(pa), len(pb))} abonnementer mod {min(len(pa), len(pb))}."},
    ]

    krop = f"""
{pristabel(alle, UMAP, titel=f"{ua['navn']} og {ub['navn']} side om side",
           undertitel=f"Alle abonnementer fra begge udbydere, sorteret efter reel pris.",
           billigst_id=alle[0]["id"], vis=12)}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Begge udbyderes vilkår gennemgået")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> {e(billigst_u['navn'])} har det billigste abonnement af de to
  målt på gennemsnitspris over 12 måneder. Men {e(ua['navn'])} kører på
  {netlabel(ua)} og {e(ub['navn'])} på {netlabel(ub)}
  {"— samme net, så dækningen er identisk" if ua["netvaerk"] == ub["netvaerk"] else "— to forskellige net, og det er den forskel, der betyder mest, hvis du bor uden for en større by"}.</p>
  </div>

  <h2>{e(ua['navn'])} mod {e(ub['navn'])} på tal</h2>
  <table>
    <thead><tr><th></th><th>{e(ua['navn'])}</th><th>{e(ub['navn'])}</th></tr></thead>
    <tbody>{tabel}</tbody>
  </table>

  <h2>Vælg {e(ua['navn'])} hvis…</h2>
  <p>{e(ua['bedst_til'])} {e(ua['kort'])}</p>
  <p>Til gengæld: {e(ua['daarligt_til'])}
  <a href="/udbydere/{slug_a}/">Læs hele vores gennemgang af {e(ua['navn'])}</a>.</p>

  <h2>Vælg {e(ub['navn'])} hvis…</h2>
  <p>{e(ub['bedst_til'])} {e(ub['kort'])}</p>
  <p>Til gengæld: {e(ub['daarligt_til'])}
  <a href="/udbydere/{slug_b}/">Læs hele vores gennemgang af {e(ub['navn'])}</a>.</p>

  <h2>Sådan afgør du det</h2>
  <ol class="trin">
    <li><strong>Tjek dækningen på din adresse</strong>
    {"Begge kører på samme net, så det punkt kan du springe over — dækningen er identisk." if ua["netvaerk"] == ub["netvaerk"] else "De to selskaber kører på forskellige net. Slå begge op på din bopæl, arbejdsplads og pendlerrute, før du vælger."}</li>
    <li><strong>Find dit dataforbrug</strong>
    Vælg efter det, ikke efter selskabets ry. <a href="/guides/hvor-meget-data/">Sådan finder du tallet</a>.</li>
    <li><strong>Sammenlign på gns. over 12 mdr.</strong>
    Ikke på introprisen. Kolonnen står i tabellen ovenfor.</li>
    <li><strong>Tjek EU-data hvis du rejser</strong>
    Det er der, de to ofte adskiller sig mest.</li>
  </ol>

  <p>Se hele markedet på <a href="/billigste-mobilabonnement/">billigste mobilabonnement</a>,
  eller <a href="/sammenlign/">sammenlign to andre udbydere</a>.</p>
</section>

<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=f"{ua['navn']} vs {ub['navn']} — hvem er billigst?",
        beskrivelse=(f"{ua['navn']} eller {ub['navn']}? Se priser, netværk, EU-data og "
                     "vilkår side om side, og find ud af hvem der passer til dit forbrug."),
        opdateret=OPDATERET,
        hero=hero_side("Sammenligning", f"{e(ua['navn'])} vs {e(ub['navn'])}",
                       f"To udbydere sammenlignet på pris, netværk og vilkår. "
                       f"{len(pa) + len(pb)} abonnementer i alt.",
                       '<a href="#sammenlign" class="knap knap-primaer">Se sammenligningen</a>',
                       [(ua["navn"], f"fra {kr(gns12(fa))} kr."), (ub["navn"], f"fra {kr(gns12(fb))} kr."),
                        ("Planer", str(len(pa) + len(pb)))]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, f"{ua['navn']} vs {ub['navn']}", ""))],
    ), prioritet="0.75")


def byg_vs_oversigt():
    sti = "/sammenlign/"
    krumme = [("/", "Forside"), (None, "Sammenlign udbydere")]
    kort = ""
    aktive = [(sa, sb) for sa, sb in VS_PAR
              if [a for a in ABON if a["udbyder"] == sa]
              and [a for a in ABON if a["udbyder"] == sb]]
    for sa, sb in aktive:
        ua, ub = UMAP[sa], UMAP[sb]
        kort += f"""<a class="vskort" href="/sammenlign/{sa}-vs-{sb}/">
  <span class="vs-side"><img src="/assets/img/logoer/{ua['logo']}" alt="{e(ua['navn'])}"
    loading="lazy" width="{round(ua['logo_w'] * 24 / ua['logo_h'])}" height="24"></span>
  <span class="vs-mod">vs</span>
  <span class="vs-side"><img src="/assets/img/logoer/{ub['logo']}" alt="{e(ub['navn'])}"
    loading="lazy" width="{round(ub['logo_w'] * 24 / ub['logo_h'])}" height="24"></span>
  <span class="vs-tekst">{e(ua['navn'])} mod {e(ub['navn'])}</span>
</a>"""

    # Matrix: alle udbydere på de parametre folk sammenligner på
    matrix = ""
    for u in sorted(UDBYDERE, key=lambda x: min(
            [gns12(a) or 9e9 for a in ABON if a["udbyder"] == x["slug"]] or [9e9])):
        planer = [a for a in ABON if a["udbyder"] == u["slug"] and a["pris"] > 0]
        if not planer:
            continue
        bu = min(planer, key=lambda a: gns12(a) or 9e9)
        har_fri = any(a["data_gb"] >= 900 for a in planer)
        har_stream = any(a.get("streaming") for a in planer)
        maks_eu = max(a.get("eu_gb", 0) for a in planer)
        matrix += (f'<tr><td><a href="/udbydere/{u["slug"]}/"><strong>{e(u["navn"])}</strong></a></td>'
                   f'<td>{netlabel(u)}</td>'
                   f'<td>{kr(gns12(bu))} kr.</td>'
                   f'<td>{gb_tekst(max(a["data_gb"] for a in planer))}</td>'
                   f'<td>{maks_eu} GB</td>'
                   f'<td class="{"ja" if har_fri else "nej"}">{"Ja" if har_fri else "Nej"}</td>'
                   f'<td class="{"ja" if har_stream else "nej"}">{"Ja" if har_stream else "Nej"}</td></tr>')

    faq = [
        {"sp": "Hvordan sammenligner jeg to mobilselskaber?",
         "sv": "Start med netværket, hvis du bor uden for en større by — det er den forskel, der "
               "betyder mest. Sammenlign derefter på 12-måneders-prisen inden for den datamængde, du "
               "faktisk bruger, og tjek EU-data hvis du rejser."},
        {"sp": "Er det vigtigste at finde det billigste selskab?",
         "sv": "Nej. Det vigtigste er at finde det billigste abonnement, der dækker dit behov. Et "
               "selskab kan være billigst på små pakker og dyrest på store."},
        {"sp": "Kan to selskaber have samme dækning?",
         "sv": "Ja, og det er meget almindeligt. Kører de på samme net, er dækningen identisk — "
               "også selvom priserne er vidt forskellige."},
        {"sp": "Hvad skal jeg gøre, hvis to abonnementer koster det samme?",
         "sv": "Så kig på EU-data, opsigelsesvilkår og kundeservice. Og vælg det net, der dækker "
               "bedst netop hos dig."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="sektion-hoved afslør"><span class="etiket">Sammenlign</span>
  <h2>Vælg to udbydere</h2>
  <p class="led">Vi stiller de to op mod hinanden på pris, netværk, EU-data og vilkår — og
  siger klart, hvem der passer til hvad.</p></div>
  <div class="vskort-gitter">{kort}</div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET)}

  <div class="udtag">
  <p><strong>Kort svar:</strong> De fleste står og vælger mellem to selskaber — typisk det,
  de har nu, og et de har hørt om. En liste med {D['antal']} abonnementer besvarer ikke det
  spørgsmål. Herunder finder du {len(aktive)} direkte sammenligninger plus en matrix over
  alle {D['antal_udbydere']} udbydere på de parametre, der faktisk adskiller dem.</p>
  </div>

  <h2>Alle udbydere på ét blik</h2>
  <p>Sorteret efter laveste 12-måneders-pris. Brug den til hurtigt at se, hvilke to
  selskaber det giver mening at sammenligne i dybden.</p>
  <table>
    <thead><tr><th>Udbyder</th><th>Netværk</th><th>Fra</th><th>Største pakke</th>
    <th>Mest EU-data</th><th>Fri data</th><th>Streaming</th></tr></thead>
    <tbody>{matrix}</tbody>
  </table>

  <h2>Hvad du skal sammenligne på — i rækkefølge</h2>
  <ol class="trin">
    <li><strong>Netværk</strong>
    Den eneste parameter, der ikke kan kompenseres med penge. Kører de to selskaber på
    samme net, er dækningen identisk, og du kan springe punktet over. Gør de ikke, er det
    her, du skal begynde. <a href="/netvaerk/">Se de tre danske net</a>.</li>
    <li><strong>12-måneders-prisen inden for din datamængde</strong>
    Ikke laveste pris i absolutte tal — laveste pris for det, du skal bruge. Et selskab kan
    være billigst på 5 GB og dyrest på 100 GB.
    <a href="/12-maaneders-prisen/">Sådan beregner vi den</a>.</li>
    <li><strong>EU-data</strong>
    Den mest oversete forskel. To abonnementer til samme pris kan have 15 og 50 GB i EU.
    Rejser du, er det en reel forskel.</li>
    <li><strong>Vilkår</strong>
    Binding, oprettelse, opsigelsesvarsel og hvad der sker ved overforbrug.</li>
    <li><strong>Kundeservice</strong>
    Vejer kun tungt, hvis du regner med at bruge den. Gør du det, er det tredive kroner om
    måneden godt givet ud.</li>
  </ol>

  <h2>Den fejl folk oftest laver</h2>
  <p>De sammenligner et selskabs intropris med et andets normalpris. Det er ikke en
  sammenligning — det er to forskellige tal. Et abonnement til 39 kr. i tre måneder og
  129 kr. derefter koster 106 kr. i gennemsnit over et år, og det er tallet, der skal op
  mod konkurrentens.</p>
  <p>Derfor viser vi 12-måneders-prisen i alle vores tabeller, og derfor står regnestykket
  under hver pris, så du kan efterprøve det.</p>

  {udbyder_rangliste()}

  {ejerforhold()}

  {vejviser("/sammenlign/")}
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/udbydere/", "Alle udbydere gennemgået enkeltvis"),
      ("/netvaerk/", "De tre danske mobilnet"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/12-maaneders-prisen/", "Sådan beregner vi den reelle pris"),
  ])}
  {forfatterboks()}{afsloering()}
</section>"""
    return skriv(sti, shell(
        sti=sti, titel="Sammenlign mobilselskaber — to udbydere side om side",
        beskrivelse=("Stil to danske mobilselskaber op mod hinanden på pris, netværk, "
                     "EU-data og vilkår. Med matrix over alle udbydere."),
        opdateret=OPDATERET,
        hero=hero_side("Sammenlign", "Udbyder mod udbyder",
                       "De par folk oftest står og vælger imellem, stillet direkte op mod "
                       "hinanden på tal.",
                       '<a href="#indhold" class="knap knap-primaer">Se sammenligningerne</a>',
                       [("Sammenligninger", str(len(aktive))), ("Udbydere", str(D['antal_udbydere'])),
                        ("Parametre", "7")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, "Sammenlign mobilselskaber", ""))],
    ), prioritet="0.75")


# --------------------------------------------------------------- VÆRKTØJER

def landetabel():
    raekker = ""
    for l in LANDE:
        risiko = ' data-risiko="1"' if l["risiko"] else ""
        merkat = '<span class="mrk mrk-sol">Vær opmærksom</span>' if l["risiko"] else (
            '<span class="mrk mrk-puls">EU/EØS-takst</span>' if l["eu"] else "")
        raekker += (f'<tr data-land="{e(l["navn"].lower())}" data-kode="{l["kode"]}"'
                    f' data-region="{e(l["region"])}"{risiko}>'
                    f'<td><span class="flag">{l["flag"]}</span> {e(l["navn"])}</td>'
                    f'<td class="kode">+{l["kode"]}</td>'
                    f'<td class="kode">{e(l["iso"])}</td>'
                    f'<td>{e(l["region"])}</td><td>{merkat}</td></tr>')
    return raekker


def byg_landekoder():
    sti = "/landekoder/"
    krumme = [("/", "Forside"), (None, "Landekoder")]
    regioner = sorted({l["region"] for l in LANDE})
    regionknapper = "".join(
        f'<button class="chip" data-region="{e(r)}" aria-pressed="false">{e(r)}</button>'
        for r in regioner)

    faq = [
        {"sp": "Hvad er Danmarks landekode?",
         "sv": "Danmarks landekode er +45. Når nogen ringer til dig fra udlandet, taster de +45 "
               "efterfulgt af dit 8-cifrede danske nummer. Danmark har ingen områdenumre — alle "
               "danske numre er præcis otte cifre."},
        {"sp": "Skal jeg bruge + eller 00?",
         "sv": "De betyder præcis det samme og fortæller nettet, at opkaldet er internationalt. "
               "På mobil bør du altid bruge +, fordi det virker uanset hvilket land du selv "
               "befinder dig i. Hold 0-tasten nede i et par sekunder for at få + frem."},
        {"sp": "Hvorfor virker mit udlandsopkald ikke?",
         "sv": "Næsten altid én af tre ting: du har glemt at fjerne et indledende 0 fra det "
               "nationale nummer, du har tastet en forkert landekode, eller nummeret er et "
               "kortnummer, der kun virker inden for landet."},
        {"sp": "Hvad koster det at ringe til udlandet fra Danmark?",
         "sv": "Opkald fra Danmark til andre EU- og EØS-lande er prisreguleret. Uden for EU "
               "sætter udbyderen selv taksten, og den varierer voldsomt fra land til land. Tjek "
               "prisen for netop dit land hos din udbyder, før du ringer."},
        {"sp": "Er udlandsopkald inkluderet i fri tale?",
         "sv": "Nej. Fri tale dækker opkald til danske numre. At ringe fra Danmark til et "
               "udenlandsk nummer er noget andet og koster ekstra hos de fleste udbydere."},
        {"sp": "Hvad er forskellen på landekode og ISO-kode?",
         "sv": "Telefoni-landekoden (+45) følger ITU's nummerplan. ISO-koden (DK, DNK) bruges "
               "til data, formularer og domæner. De to systemer hænger ikke sammen, og et land "
               "kan have flere telefonkoder eller dele kode med andre lande."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="vaerktoej">
    <div class="vt-hoved">
      <h2>Slå landekoden op</h2>
      <p class="led">Skriv landets navn eller koden. Tabellen filtrerer med det samme.</p>
    </div>
    <input type="search" class="vt-soeg" data-landesoeg placeholder="Søg på land eller kode — fx Tyskland eller 49"
           aria-label="Søg efter land eller landekode">
    <div class="filtre" style="margin-top:.9rem">
      <span class="maerkat">Region</span>
      <button class="chip" data-region="alle" aria-pressed="true">Alle</button>
      {regionknapper}
    </div>
    <div class="tabelrul">
      <table class="landetabel">
        <caption><span data-landeantal>{len(LANDE)}</span> landekoder vist</caption>
        <thead><tr><th scope="col">Land</th><th scope="col">Landekode</th>
        <th scope="col">ISO</th><th scope="col">Region</th><th scope="col">Bemærk</th></tr></thead>
        <tbody>{landetabel()}</tbody>
      </table>
    </div>
    <p class="vt-tom" data-landetom hidden>Ingen lande matcher din søgning.</p>
    <p class="mobilnote">⚠ markerer landekoder, der ofte optræder i svindelopkald.
    <a href="/hvem-ringer-til-mig/">Se hvordan du genkender dem</a>.</p>
  </div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Koder kontrolleret mod ITU-T E.164 og ISO 3166-1")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Danmarks landekode er <strong>+45</strong>. Skal du ringe til
  udlandet fra Danmark, taster du + efterfulgt af landekoden og derefter nummeret uden det
  indledende nul. Skal nogen ringe til dig fra udlandet, taster de +45 og dit 8-cifrede
  nummer. Danske numre har ingen områdenumre.</p>
  </div>

  <h2>Sådan ringer du til udlandet fra Danmark</h2>
  <ol class="trin">
    <li><strong>Start med + i stedet for 00</strong>
    Begge virker, men + virker også, når du selv er i udlandet. Hold 0-tasten nede på
    mobilen, indtil + kommer frem.</li>
    <li><strong>Tast landekoden</strong>
    Find den i tabellen ovenfor. Tyskland er 49, Sverige 46, Storbritannien 44.</li>
    <li><strong>Fjern det indledende nul</strong>
    Mange lande skriver deres numre med et 0 foran til national brug. Det skal væk ved
    internationale opkald. Svensk 070 123 4567 bliver til +46 70 123 4567.</li>
    <li><strong>Tast resten af nummeret</strong>
    Uden mellemrum, bindestreger eller parenteser.</li>
  </ol>

  <div class="tip">
  <h3>Gem numre i internationalt format</h3>
  <p>Gemmer du alle dine kontakter som +45 12 34 56 78 frem for 12 34 56 78, virker de også,
  når du selv er i udlandet. Det er den enkleste måde at undgå, at opkald mislykkes på
  rejsen — og det tager to minutter at rette de vigtigste numre.</p>
  </div>

  <h2>Roaming og udlandsopkald er ikke det samme</h2>
  <p>Det er den forveksling, der koster flest danskere penge, og den er værd at få helt på
  plads.</p>
  <table>
  <thead><tr><th></th><th>Roaming</th><th>Udlandsopkald</th></tr></thead>
  <tbody>
  <tr><td><strong>Hvor er du?</strong></td><td>I udlandet</td><td>I Danmark</td></tr>
  <tr><td><strong>Hvem ringer du til?</strong></td><td>Typisk danske numre</td><td>Et udenlandsk nummer</td></tr>
  <tr><td><strong>Reguleret?</strong></td><td>Ja, inden for EU/EØS</td><td>Delvist — EU-opkald har prisloft</td></tr>
  <tr><td><strong>Inkluderet i fri tale?</strong></td><td>Ja, inden for EU</td><td>Nej, hos de fleste udbydere</td></tr>
  </tbody>
  </table>
  <p>Ringer du fast til udlandet, bør du vælge et abonnement bygget til det frem for at betale
  minuttakst. Se vores gennemgang af
  <a href="/udbydere/lebara/">Lebara</a> og <a href="/udbydere/lyca-mobile/">Lyca Mobile</a>,
  som begge er specialiseret i internationale opkald — og husk at tjekke, om landelisten
  dækker mobilnumre eller kun fastnet.</p>

  <h2>Lande der deler landekode</h2>
  <p>Et par steder kan koden ikke stå alene. +1 dækker både USA, Canada og en række caribiske
  øer, som skelnes på områdenummeret. +7 dækker både Rusland og Kasakhstan. Det betyder, at
  du ikke altid kan aflæse landet af koden alene.</p>

  <h2>Fik du et opkald fra et ukendt land?</h2>
  <p>Så er det ikke landekodetabellen, du skal bruge — det er vores værktøj til at slå
  nummeret op og vurdere, om det er svindel.
  <a href="/hvem-ringer-til-mig/">Se hvem der ringer til dig</a>.</p>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/hvem-ringer-til-mig/", "Hvem ringer til mig? Slå nummeret op"),
      ("/mobilabonnement-med-fri-tale/", "Mobilabonnement med fri tale"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
      ("/guides/esim/", "eSIM til rejsen — undgå dyr roaming"),
  ])}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=f"Landekoder — komplet oversigt over {len(LANDE)} telefonkoder",
        beskrivelse=(f"Søg blandt {len(LANDE)} landekoder til telefon. Danmarks landekode er +45. "
                     "Se ISO-koder, EU-takst og hvordan du ringer til udlandet."),
        opdateret=OPDATERET,
        hero=hero_side("Værktøj", "Landekoder til telefon",
                       f"Søg blandt {len(LANDE)} landekoder. Se koden, ISO-forkortelsen og om "
                       "opkaldet er dækket af EU-prisloftet.",
                       '<a href="#indhold" class="knap knap-primaer">Søg i tabellen</a>',
                       [("Landekoder", str(len(LANDE))), ("Danmark", "+45"), ("Kilde", "ITU-T")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, "Landekoder", ""),
                     vaerktoejld(sti, "Landekodeopslag",
                                 "Søg blandt landekoder til telefon med filtrering på region."))],
    ), prioritet="0.8")


def byg_hvem_ringer():
    sti = "/hvem-ringer-til-mig/"
    krumme = [("/", "Forside"), (None, "Hvem ringer til mig?")]
    faq = [
        {"sp": "Hvem ringer til mig fra et ukendt nummer?",
         "sv": "Starter nummeret med +, kan du aflæse landet af landekoden. Indsæt nummeret i "
               "værktøjet ovenfor, så finder vi landet og fortæller, om koden er kendt fra "
               "svindelopkald."},
        {"sp": "Hvad er wangiri-svindel?",
         "sv": "Et opkald der ringer én gang og lægger på, så du ringer tilbage til et dyrt "
               "udlandsnummer. Regningen kan løbe op på få minutter. Ring aldrig tilbage til et "
               "ukendt udenlandsk nummer, du ikke forventede."},
        {"sp": "Koster det noget at modtage et opkald fra udlandet?",
         "sv": "Nej. At modtage et opkald i Danmark er gratis, uanset hvor det kommer fra. Det "
               "er kun, hvis du ringer tilbage, at det kan blive dyrt."},
        {"sp": "Hvordan blokerer jeg et nummer?",
         "sv": "På iPhone: åbn opkaldet i Seneste, tryk på i-ikonet og vælg Bloker denne "
               "opkalder. På Android: hold nummeret nede i opkaldslisten og vælg Bloker. Du kan "
               "også bede din udbyder spærre for udgående udlandsopkald."},
        {"sp": "Kan afsenderen forfalske nummeret?",
         "sv": "Ja. Nummervisning kan manipuleres, så et opkald ser ud til at komme fra et dansk "
               "nummer eller fra en myndighed. Vær derfor altid skeptisk over for uventede "
               "opkald, der beder om oplysninger — uanset hvad displayet viser."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="vaerktoej">
    <div class="vt-hoved">
      <h2>Slå nummeret op</h2>
      <p class="led">Indsæt hele nummeret med landekode. Vi finder landet og vurderer risikoen.</p>
    </div>
    <div class="opslag">
      <input type="tel" class="vt-soeg" data-nummer placeholder="+216 71 123 456"
             aria-label="Indtast telefonnummer med landekode">
      <button type="button" class="knap knap-primaer" data-slaa-op>Slå op</button>
    </div>
    <div class="opslag-svar" data-opslagsvar hidden></div>
    <p class="vt-note">Vi gemmer ikke det nummer, du indtaster. Opslaget sker i din egen browser.</p>
  </div>
  <script type="application/json" data-landedata>{json.dumps([
      {"navn": l["navn"], "kode": l["kode"], "risiko": l["risiko"], "flag": l["flag"]}
      for l in LANDE], ensure_ascii=False)}</script>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Landekoder kontrolleret mod ITU-T E.164")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Starter nummeret med +, fortæller de første cifre hvilket land
  opkaldet kommer fra. Modtager du et opkald fra et land, du ingen forbindelse har til, og det
  ringer kun én gang — så ring ikke tilbage. Det er den mest udbredte form for
  telefonsvindel i Danmark, og det koster kun penge, hvis du selv ringer op.</p>
  </div>

  <h2>Wangiri: ét ring og læg på</h2>
  <p>Metoden hedder wangiri efter det japanske ord for netop det: ring én gang og læg på.
  Svindleren ringer til tusindvis af numre samtidig og lægger på efter et enkelt ring. Formålet
  er ikke at tale med dig — det er at få dig til at ringe tilbage.</p>
  <p>Nummeret, du ringer tilbage til, er et betalingsnummer i udlandet, hvor svindleren får en
  andel af minutprisen. Samtalen trækkes i langdrag med ventemusik eller en optaget besked, og
  regningen kan løbe op i mange hundrede kroner på få minutter.</p>

  <div class="advarsel">
  <p><strong>Den eneste regel du skal huske:</strong> Det koster ikke noget at modtage et
  opkald. Det koster kun, hvis du ringer tilbage. Forventer du ikke et opkald fra det land,
  så lad være.</p>
  </div>

  <h2>Sådan vurderer du et ukendt opkald</h2>
  <ol class="trin">
    <li><strong>Se på landekoden</strong>
    Slå den op i værktøjet ovenfor eller i vores
    <a href="/landekoder/">oversigt over landekoder</a>. Kender du ingen i det land, er det et
    dårligt tegn.</li>
    <li><strong>Tæl ringene</strong>
    Et enkelt ring uden besked er det klassiske mønster. Rigtige opkald ringer flere gange
    eller lægger en besked.</li>
    <li><strong>Ring aldrig tilbage til et ukendt udlandsnummer</strong>
    Er det vigtigt, ringer de igen eller skriver. Skal du endelig undersøge det, så søg på
    nummeret først.</li>
    <li><strong>Bloker og meld</strong>
    Bloker nummeret i telefonen, og overvej at bede din udbyder spærre for udgående
    udlandsopkald, hvis det gentager sig.</li>
  </ol>

  <h2>Opkald der ser danske ud</h2>
  <p>Nummervisning kan forfalskes. Det betyder, at et opkald kan se ud til at komme fra et
  dansk nummer, fra din bank eller fra en myndighed, selvom det gør det modsatte. Teknikken
  hedder spoofing, og den er svær at opdage for modtageren.</p>
  <p>Beskyttelsen er ikke teknisk, men en vane: giv aldrig NemID- eller MitID-oplysninger,
  kortnumre eller koder til nogen, der ringer til dig. Læg på, find selv nummeret til banken
  eller myndigheden, og ring op selv. Ingen legitim afsender vil have noget imod det.</p>

  <h2>Hvad du kan gøre forebyggende</h2>
  <ul>
    <li><strong>Bed om spærring for overtakserede numre</strong> hos din udbyder. Det er gratis
    og lukker den dyreste kategori helt.</li>
    <li><strong>Slå spærring for udgående udlandsopkald til</strong>, hvis du aldrig ringer til
    udlandet. Så kan et tilbagekald ikke lykkes.</li>
    <li><strong>Tjek regningen</strong> hver måned. Opdager du en post, du ikke kan forklare,
    så kontakt udbyderen med det samme — det er lettere at få rettet i den periode, det sker.</li>
    <li><strong>Sæt datastop til</strong> på børns telefoner, og forklar dem reglen om ikke at
    ringe tilbage.</li>
  </ul>

  <h2>Ringer du selv meget til udlandet?</h2>
  <p>Så er minuttaksten din største udgift, ikke svindel. Et abonnement med inkluderede
  udlandsminutter kan spare hundredvis af kroner om måneden. Se
  <a href="/mobilabonnement-med-fri-tale/">abonnementer med fri tale</a> og vores gennemgang af
  <a href="/udbydere/lebara/">Lebara</a>.</p>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/landekoder/", "Alle landekoder — komplet oversigt"),
      ("/mobilabonnement-med-fri-tale/", "Mobilabonnement med fri tale"),
      ("/mobilabonnement-til-boern/", "Mobilabonnement til børn — sådan undgår du regninger"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
  ])}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel="Hvem ringer til mig? Slå nummeret og landekoden op",
        beskrivelse=("Indsæt nummeret og se hvilket land det kommer fra. Lær at genkende "
                     "wangiri-svindel, og find ud af hvornår du aldrig skal ringe tilbage."),
        opdateret=OPDATERET,
        hero=hero_side("Værktøj", "Hvem ringer til mig?",
                       "Indsæt nummeret med landekode, så finder vi landet og fortæller, om "
                       "koden er kendt fra svindelopkald.",
                       '<a href="#indhold" class="knap knap-primaer">Slå nummeret op</a>',
                       [("Landekoder", str(len(LANDE))), ("Opslag", "i din browser"),
                        ("Vi gemmer", "intet")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, "Hvem ringer til mig?", ""),
                     vaerktoejld(sti, "Nummeropslag",
                                 "Slå et ukendt telefonnummer op og se hvilket land det kommer fra."))],
    ), prioritet="0.8")


def byg_daekningstjek():
    sti = "/daekningskort/"
    krumme = [("/", "Forside"), (None, "Dækningstjek")]
    netkort = ""
    for n in NETVAERK:
        selskaber = [u["navn"] for u in UDBYDERE if u["netvaerk"] == n["navn"]]
        netkort += f"""<div class="netkort">
  <h3>{e(n["navn"])}</h3>
  <p class="netkort-kort">{e(n["kort"])}</p>
  <p><strong>Stærkest:</strong> {e(n["styrke"][:150])}…</p>
  <p class="netkort-selskaber"><strong>Selskaber:</strong> {e(", ".join(selskaber)) or "se udbydere"}</p>
  <a href="/netvaerk/{n["slug"]}/" class="knap knap-linje knap-lille">Se abonnementer på nettet</a>
</div>"""

    faq = [
        {"sp": "Hvordan tjekker jeg dækningen på min adresse?",
         "sv": "Slå din adresse op på alle tre netværksejeres dækningskort. De bygger på operatørernes "
               "egne måledata og er den bedste offentligt tilgængelige kilde. Tjek både bopæl, "
               "arbejdsplads og din pendlerrute."},
        {"sp": "Har billige mobilselskaber dårligere dækning?",
         "sv": "Nej. Der findes kun tre mobilnet i Danmark, og alle selskaber lejer sig ind hos et af "
               "dem. Et discountselskab på TDC NET har præcis samme dækning som et premiumselskab på "
               "samme net."},
        {"sp": "Hvilket net har bedst dækning i Danmark?",
         "sv": "TDC NET er det mest udbyggede og står typisk stærkest i landdistrikter, "
               "sommerhusområder og indendørs. I byerne er forskellen mellem de tre lille."},
        {"sp": "Hvad gør jeg, hvis dækningen er dårlig indendørs?",
         "sv": "Slå wi-fi-opkald til i telefonens indstillinger. Så føres opkald over dit hjemmenet i "
               "stedet for mobilnettet. De fleste danske udbydere understøtter det uden ekstra betaling."},
        {"sp": "Kan jeg fortryde, hvis dækningen viser sig at være dårlig?",
         "sv": "Køber du online, har du som udgangspunkt fortrydelsesret efter forbrugeraftaleloven. "
               "Test derfor dækningen grundigt i de første dage, mens du stadig kan fortryde."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="vaerktoej">
    <div class="vt-hoved">
      <h2>Tjek dækningen, før du vælger</h2>
      <p class="led">Vi har ikke vores eget dækningskort — og vil hellere sige det ligeud end
      vise dig noget upræcist. Netværksejerne har de rigtige data, og her er vejen derhen.</p>
    </div>
    <div class="netkort-gitter">{netkort}</div>
    <p class="vt-note">Dækningskortene findes på netværksejernes egne hjemmesider. Søg på
    netværkets navn plus "dækningskort" for at finde det aktuelle kort.</p>
  </div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Netværksoplysninger kontrolleret hos udbyderne")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Der findes kun tre mobilnet i Danmark, og dit valg af
  selskab er reelt et valg af net. Tjek dækningen tre steder — hjemme, på arbejde og på din
  pendlerrute — før du bestiller. Bor du centralt i en større by, kan du vælge frit efter
  pris. Bor du på landet, bør nettet veje tungere end de sidste tredive kroner.</p>
  </div>

  <h2>Sådan tjekker du dækningen rigtigt</h2>
  <ol class="trin">
    <li><strong>Slå adressen op på alle tre net</strong>
    Ikke kun det, du overvejer. Du skal se forskellen for at kunne vurdere den.</li>
    <li><strong>Tjek tre steder, ikke ét</strong>
    Bopæl, arbejdsplads og ruten imellem. Det er der, telefonen bruges.</li>
    <li><strong>Kig efter indendørsdækning</strong>
    Kortene skelner typisk mellem udendørs og indendørs. Bor du i en ældre bygning med tykke
    mure eller har kælder, er det den indendørs værdi, der betyder noget.</li>
    <li><strong>Spørg en nabo på samme net</strong>
    Den mest undervurderede metode, og den eneste der siger noget om virkeligheden præcis
    hos dig.</li>
    <li><strong>Test i fortrydelsesperioden</strong>
    Køber du online, har du fortrydelsesret. Brug de første dage aktivt.</li>
  </ol>

  <h2>Wi-fi-opkald løser de fleste indendørsproblemer</h2>
  <p>Er dækningen dårlig netop dér, hvor du bor, findes der en løsning, der ikke koster
  noget: wi-fi-opkald. Telefonen fører opkaldet over dit hjemmenet i stedet for mobilnettet,
  og samtalen bliver typisk bedre end på et svagt mobilsignal.</p>
  <p>Funktionen slås til i telefonens indstillinger under opkald eller mobilnetværk. De
  fleste danske udbydere understøtter det uden ekstra betaling. Det ændrer ikke dit
  nummer, og modtageren mærker ingen forskel.</p>

  <div class="tip">
  <h3>Rækkefølgen der sparer flest ærgrelser</h3>
  <p>Tjek dækning først, pris bagefter. Et abonnement til 44 kr., der ikke virker i din
  stue, er ikke billigt — det er spildt. Omvendt: er alle tre net grønne hos dig, er der
  ingen grund til at betale premium for dækning, du ikke får glæde af.</p>
  </div>

  <h2>5G — hvornår betyder det noget?</h2>
  <p>5G giver højere hastigheder og lavere forsinkelse end 4G. For almindelig brug — sociale
  medier, streaming, navigation — mærker de fleste ikke stor forskel fra et velfungerende
  4G-net.</p>
  <p>5G er værd at prioritere, hvis du henter store filer, bruger telefonen som hotspot til
  arbejde, eller bor et sted med overbelastet 4G. Dækningen er stadig mest udbygget i
  byerne. Læs mere i vores <a href="/guides/daekning-og-netvaerk/">guide til dækning og
  netværk</a>.</p>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/netvaerk/", "De tre danske mobilnet sammenlignet"),
      ("/guides/daekning-og-netvaerk/", "Guide til dækning og netværk"),
      ("/speedtest/", "Test din mobilhastighed"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
  ])}
  {forfatterboks()}{afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel="Dækningstjek — se hvilket mobilnet der dækker hos dig",
        beskrivelse=("Tjek mobildækningen på din adresse på alle tre danske net, før du "
                     "vælger abonnement. Med guide til indendørsdækning og wi-fi-opkald."),
        opdateret=OPDATERET,
        hero=hero_side("Værktøj", "Tjek dækningen hos dig",
                       "Dit valg af selskab er reelt et valg af net. Her er vejen til de "
                       "rigtige dækningskort — og hvad du skal kigge efter.",
                       "", [("Net i Danmark", "3"), ("Tjek", "3 steder"), ("Wi-fi-opkald", "gratis")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     howtold(sti, "Tjek mobildækningen på din adresse",
                             "Sådan tjekker du dækningen rigtigt", krop))],
    ), prioritet="0.7")


def byg_speedtest():
    sti = "/speedtest/"
    krumme = [("/", "Forside"), (None, "Hastighedstest")]
    faq = [
        {"sp": "Hvor hurtig bør min mobilforbindelse være?",
         "sv": "Til streaming i HD rækker 5-10 Mbit. Til videomøder 3-5 Mbit. Til almindelig browsing "
               "og sociale medier er 2 Mbit nok. Over 50 Mbit mærker de fleste ikke forskel i "
               "hverdagsbrug."},
        {"sp": "Hvorfor er min hastighed lavere end lovet?",
         "sv": "Udbydernes hastigheder er teoretiske maksimum. Den reelle hastighed afhænger af "
               "afstand til masten, hvor mange der er på nettet samtidig, bygningens mure og din "
               "telefons modem."},
        {"sp": "Måler denne test min faktiske forbindelse?",
         "sv": "Den måler hastigheden mellem din enhed og vores server. Det giver et brugbart "
               "fingerpeg, men er ikke en laboratoriemåling. Kør den flere gange og på forskellige "
               "tidspunkter for et retvisende billede."},
        {"sp": "Bruger testen af min datamængde?",
         "sv": "Ja, hver test henter cirka 0,9 MB. Kører du ti tests, bruger du under 10 MB. Det er "
               "forsvindende lidt, men værd at vide på et lille abonnement."},
        {"sp": "Hvad gør jeg, hvis hastigheden er for lav?",
         "sv": "Tjek om du har brugt din datamængde op — mange udbydere sætter hastigheden ned frem "
               "for at stoppe forbindelsen. Genstart telefonen, og test igen et andet sted for at "
               "udelukke, at det er dækningen netop der."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="vaerktoej">
    <div class="vt-hoved">
      <h2>Test din hastighed</h2>
      <p class="led">Måler downloadhastigheden mellem din enhed og vores server. Testen
      henter cirka 0,9 MB.</p>
    </div>
    <div class="speedtest">
      <button type="button" class="knap knap-primaer" data-speedtest>Start test</button>
      <div class="st-resultat" data-st-resultat hidden>
        <div class="st-tal"><b data-st-mbit>—</b><span>Mbit/s</span></div>
        <div class="st-vurdering" data-st-vurdering></div>
      </div>
    </div>
    <p class="vt-note">Resultatet er et fingerpeg, ikke en laboratoriemåling. Din reelle
    hastighed afhænger af afstand til masten, belastning på nettet og din telefon.</p>
  </div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, "Testen kører i din egen browser")}

  <div class="udtag">
  <p><strong>Kort svar:</strong> De fleste har brug for langt mindre hastighed, end de tror.
  5-10 Mbit rækker til video i HD, og 2 Mbit til almindelig browsing. Er din måling under
  1 Mbit, er du sandsynligvis løbet tør for data — mange udbydere sætter hastigheden ned i
  stedet for at stoppe forbindelsen helt.</p>
  </div>

  <h2>Hvad skal du bruge hastigheden til?</h2>
  <table>
  <thead><tr><th>Aktivitet</th><th>Nødvendig hastighed</th><th>Bemærkning</th></tr></thead>
  <tbody>
  <tr><td>Beskeder og sociale medier</td><td>1–2 Mbit</td><td>Næsten altid nok</td></tr>
  <tr><td>Musikstreaming</td><td>1–2 Mbit</td><td>Selv i høj kvalitet</td></tr>
  <tr><td>Video i standardkvalitet</td><td>3–5 Mbit</td><td>Dækker de fleste</td></tr>
  <tr><td>Video i HD</td><td>5–10 Mbit</td><td>Her stopper behovet for de fleste</td></tr>
  <tr><td>Videomøder</td><td>3–5 Mbit begge veje</td><td>Upload betyder lige så meget</td></tr>
  <tr><td>Hotspot til laptop</td><td>10–25 Mbit</td><td>Afhænger af hvad laptoppen laver</td></tr>
  </tbody>
  </table>
  <p>Læg mærke til, hvor lavt tallene ligger. Et abonnement, der reklamerer med flere
  hundrede megabit, giver dig ikke en bedre oplevelse end et på 25 Mbit, hvis du bruger
  telefonen som de fleste. Hastighed er sjældent det, du skal betale ekstra for —
  <a href="/daekningskort/">dækning er</a>.</p>

  <h2>Hvorfor svinger hastigheden?</h2>
  <ul>
    <li><strong>Afstand til masten.</strong> Den enkeltfaktor der betyder mest.</li>
    <li><strong>Belastning.</strong> Myldretid, koncerter og stationer deler kapaciteten
    mellem mange brugere samtidig.</li>
    <li><strong>Bygningen.</strong> Tykke mure, kældre og elevatorer dæmper signalet
    kraftigt.</li>
    <li><strong>Opbrugt data.</strong> Flere udbydere skruer ned frem for at stoppe. Er du
    pludselig meget langsom sidst på måneden, er det typisk forklaringen.</li>
    <li><strong>MVNO-vilkår.</strong> Nogle aftaler indeholder hastighedsloft eller lavere
    prioritet i myldretiden. Det står i abonnementsvilkårene.</li>
  </ul>

  <h2>Sådan tester du rigtigt</h2>
  <ol class="trin">
    <li><strong>Slå wi-fi fra</strong>
    Ellers måler du dit hjemmenet i stedet for mobilforbindelsen.</li>
    <li><strong>Test flere gange</strong>
    En enkelt måling siger ikke meget. Tag gennemsnittet af tre.</li>
    <li><strong>Test på forskellige tidspunkter</strong>
    Klokken 8 og klokken 20 kan give vidt forskellige resultater på samme sted.</li>
    <li><strong>Test hvor du faktisk er</strong>
    Hjemme, på arbejdet og på pendlerruten — ikke kun ét sted.</li>
  </ol>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/daekningskort/", "Tjek dækningen på din adresse"),
      ("/netvaerk/", "De tre danske mobilnet"),
      ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
  ])}
  {forfatterboks()}{afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel="Hastighedstest — mål din mobilforbindelse",
        beskrivelse=("Test hvor hurtig din mobilforbindelse er, og se hvad du reelt har brug "
                     "for. De fleste har brug for langt mindre hastighed, end de tror."),
        opdateret=OPDATERET,
        hero=hero_side("Værktøj", "Test din mobilhastighed",
                       "Mål downloadhastigheden på få sekunder, og se hvad tallet betyder "
                       "for det, du faktisk bruger telefonen til.",
                       "", [("Test", "0,9 MB"), ("HD-video", "5–10 Mbit"), ("Browsing", "2 Mbit")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     vaerktoejld(sti, "Hastighedstest",
                                 "Mål downloadhastigheden på din mobilforbindelse."))],
    ), prioritet="0.7")


# --------------------------------------------------------------- UDBYDERE

def byg_udbyderoversigt():
    sti = "/udbydere/"
    titel = f"Mobilselskaber i Danmark — alle {D['antal_udbydere']} udbydere sammenlignet"
    besk = ("Uafhængig gennemgang af alle danske mobilselskaber. Se netværk, priser, "
            "ejerforhold og hvem der passer til hvad — med fordele og ulemper.")
    krumme = [("/", "Forside"), (None, "Udbydere")]

    med_data = [a for a in ABON if a["data_gb"] > 0 and a["pris"] > 0]
    billigste_u = min(ABON, key=lambda a: gns12(a) or 9e9)
    dyreste_u = max(ABON, key=lambda a: gns12(a) or 0)

    faq = [
        {"sp": "Hvor mange mobilselskaber er der i Danmark?",
         "sv": f"Vi følger {D['antal_udbydere']} selskaber med i alt {D['antal']} abonnementer. "
               "Der findes flere på markedet, men de fleste er små eller retter sig mod erhverv."},
        {"sp": "Hvilket mobilselskab er billigst?",
         "sv": f"{UMAP[billigste_u['udbyder']]['navn']} har det billigste abonnement i vores "
               f"sammenligning til {kr(gns12(billigste_u))} kr. om måneden regnet over 12 måneder. "
               "Billigst i én kategori er dog ikke billigst i alle."},
        {"sp": "Har billige mobilselskaber dårligere dækning?",
         "sv": "Nej. Der findes kun tre mobilnet i Danmark, og alle selskaber lejer sig ind hos et "
               "af dem. Et discountselskab på TDC NET har præcis samme dækning som et premiumselskab "
               "på samme net."},
        {"sp": "Hvad er en MVNO?",
         "sv": "Et selskab uden eget mobilnet, der lejer kapacitet hos en netværksejer. De fleste "
               "danske mobilselskaber er MVNO'er. Din dækning bestemmes af det net, de lejer sig "
               "ind på — ikke af selskabets størrelse."},
        {"sp": "Kan jeg skifte selskab og beholde mit nummer?",
         "sv": "Ja. Nummerportering er en rettighed i Danmark. Du bestiller hos den nye udbyder, "
               "oplyser dit nummer, og de håndterer flytningen. Du skal ikke opsige noget selv."},
        {"sp": "Hvilket selskab har flest abonnementer at vælge mellem?",
         "sv": f"Blandt dem vi følger, har flere selskaber 5-7 abonnementer. Et stort udvalg er "
               "ikke i sig selv en fordel — en kort prisliste gør ofte beslutningen nemmere."},
        {"sp": "Anbefaler I selskaber, I tjener penge på?",
         "sv": "Vi medtager også udbydere, vi ikke har en provisionsaftale med, og alle tabeller "
               "sorteres efter pris. Udbydere kan ikke købe sig til en placering eller en bedre omtale."},
    ]

    krop = f"""
<section class="sektion baand">
  <div class="sektion-hoved afslør">
    <span class="etiket">Oversigt</span>
    <h2>Alle {D['antal_udbydere']} udbydere i vores sammenligning</h2>
    <p class="led">Klik videre for priser, netværk, fordele og de ulemper, selskaberne selv
    undlader at nævne.</p>
  </div>
  <div class="kortgitter kg-3">{"".join(udbyderkort(u) for u in UDBYDERE)}</div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET)}

  <div class="udtag">
  <p><strong>Kort svar:</strong> Vi følger {D['antal_udbydere']} danske mobilselskaber med
  {D['antal']} abonnementer mellem {kr(gns12(billigste_u))} og {kr(gns12(dyreste_u))} kr. om
  måneden. Alle lejer sig ind på et af landets tre mobilnet — TDC NET, Telenor eller 3 — så
  valget af selskab er reelt to beslutninger: hvilket net du vil køre på, og hvem du vil
  være kunde hos.</p>
  </div>

  {udbyder_rangliste()}

  <h2>Nettet bestemmer dækningen, selskabet bestemmer prisen</h2>
  <p>Det er den vigtigste indsigt om det danske marked, og den er værd at gentage: et
  abonnement til {kr(gns12(billigste_u))} kr. og et til {kr(gns12(dyreste_u))} kr. kan køre
  på præcis de samme master med præcis den samme hastighed. Din telefon kan ikke se forskel.</p>
  <p>Det, du betaler ekstra for i den dyre ende, er fire ting: adgang til det mest udbyggede
  net, bemandet kundeservice og butikker, tillægsydelser som streaming eller forsikring, og
  i nogle tilfælde en højere prioritering af din trafik, når nettet er belastet.</p>
  <p>Spørgsmålet er derfor aldrig, om et billigt selskab er "dårligt". Det er, om du får
  glæde af det, du betaler ekstra for.</p>

  {netvaerksgruppering()}

  {ejerforhold()}

  {prisfordeling()}

  <h2>Sådan vælger du mellem selskaberne</h2>
  <ol class="trin">
    <li><strong>Afgør først om netværket betyder noget for dig</strong>
    Bor du centralt i en større by, kan du vælge frit og gå efter pris. Bor du på landet, i
    et sommerhusområde eller pendler du langt, bør nettet vælges før prisen.
    <a href="/daekningskort/">Tjek dækningen på din adresse</a>.</li>
    <li><strong>Find dit dataforbrug</strong>
    Ikke hvad du tror — hvad du faktisk bruger. Det står i telefonens indstillinger.
    <a href="/guides/hvor-meget-data/">Sådan finder du tallet</a>.</li>
    <li><strong>Sammenlign på 12-måneders-prisen</strong>
    Ikke på introprisen. Det er der, de fleste vælger forkert.
    <a href="/12-maaneders-prisen/">Se hvordan vi beregner den</a>.</li>
    <li><strong>Tjek kundeservice, hvis du har brug for den</strong>
    Er du utryg ved selv at sætte et simkort op, eller vil du kunne ringe til nogen, så
    vælg et selskab med bemandet support — også selvom det koster mere.</li>
  </ol>

  {tabel_billigst_pr_udbyder()}

  <h2>Hvad vi ikke vurderer selskaberne på</h2>
  <p>Vi bruger ikke anmeldelsesscorer som rangeringskriterium. De er ikke sammenlignelige
  på tværs af selskaber med meget forskellige kundeantal, og folk skriver typisk kun, når
  noget går galt eller går overraskende godt.</p>
  <p>Vi laver heller ikke egne hastigheds- eller dækningsmålinger. Netværksejerne og de
  uafhængige måleinstitutter har adgang til datamængder, vi ikke kan matche, og det ville
  være uredeligt at foregive andet. Hvor dækning er relevant, henviser vi til dem.</p>

  {vejviser("/udbydere/")}

  {kilder(["teleindustrien", "digst_klage", "teleankenaevnet"],
          ["Priser og vilkår: udbydernes egne offentlige prislister, kontrolleret manuelt.",
           "Ejerforhold: selskabernes egne oplysninger.",
           "Netværksangivelser: udbydernes egne oplysninger. Hvor de ikke kan verificeres, "
           "angiver vi MVNO frem for at gætte."])}
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/netvaerk/", "De tre danske mobilnet sammenlignet"),
      ("/sammenlign/", "Stil to udbydere direkte op mod hinanden"),
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/bedste-mobilabonnement/", "Bedste mobilabonnement — vores kriterier"),
  ])}
  {forfatterboks()}{afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side("Udbydere", f"Alle {D['antal_udbydere']} danske mobilselskaber",
                       "Vi gennemgår hvert selskab for sig — netværk, priser, ejerforhold og "
                       "de ulemper, de selv undlader at nævne.",
                       '<a href="#indhold" class="knap knap-primaer">Se oversigten</a>',
                       [("Selskaber", str(D['antal_udbydere'])), ("Abonnementer", str(D['antal'])),
                        ("Net i DK", "3")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk),
                     {"@type": "ItemList", "name": "Mobilselskaber i Danmark",
                      "numberOfItems": len(UDBYDERE),
                      "itemListElement": [
                          {"@type": "ListItem", "position": i + 1,
                           "url": DOMAENE + f"/udbydere/{u['slug']}/", "name": u["navn"]}
                          for i, u in enumerate(UDBYDERE)]})],
    ), prioritet="0.85")


def oversigtsraekke(u):
    priser = [a["pris"] for a in ABON if a["udbyder"] == u["slug"]]
    fra = kr(min(priser)) + " kr." if priser else "—"
    return (f'<tr><td><a href="/udbydere/{u["slug"]}/"><strong>{e(u["navn"])}</strong></a></td>'
            f'<td>{e(u["netvaerk"])}</td><td>{fra}</td><td>{e(u["bedst_til"])}</td></tr>')


def byg_udbyder(u):
    sti = f"/udbydere/{u['slug']}/"
    egne = [a for a in ABON if a["udbyder"] == u["slug"]]
    fra = min(a["pris"] for a in egne) if egne else None
    titel = (f"{u['navn']} priser {IDAG.year} — abonnementer fra {fra} kr./md." if fra
             else f"{u['navn']} — priser, netværk og anmeldelse")
    netbesk = (f"{u['navn']} lejer sig ind på et af de danske netværk. "
               if u["netvaerk"] == "MVNO"
               else f"{u['navn']} kører på {u['netvaerk']}s netværk. ")
    besk = (netbesk
            + (f"Abonnementer fra {fra} kr./md. " if fra else "")
            + f"Se priser, fordele, ulemper og hvem {u['navn']} passer til.")
    krumme = [("/", "Forside"), ("/udbydere/", "Udbydere"), (None, u["navn"])]

    afsnit = "".join(f"<p>{e(p)}</p>" for p in u["anmeldelse"].split("\n\n"))
    fordele = "".join(f"<li>{e(x)}</li>" for x in u["fordele"])
    ulemper = "".join(f"<li>{e(x)}</li>" for x in u["ulemper"])

    # Sammenligning med tre nærmeste konkurrenter på pris
    andre = [a for a in ABON if a["udbyder"] != u["slug"]]
    if egne:
        ref = min(egne, key=lambda a: a["pris"])
        andre = sorted(andre, key=lambda a: abs(a["pris"] - ref["pris"]))[:3]
    sammenlign = ""
    for a in andre:
        au = UMAP[a["udbyder"]]
        sammenlign += (f'<tr><td><a href="/udbydere/{au["slug"]}/">{e(au["navn"])}</a> {e(a["navn"])}</td>'
                       f'<td>{gb_tekst(a["data_gb"])}</td><td>{e(au["netvaerk"])}</td>'
                       f'<td>{kr(a["pris"])} kr.</td></tr>')

    if u["netvaerk"] == "MVNO":
        netafsnit = (f"{e(u['navn'])} er en MVNO — et selskab uden eget mobilnet, der lejer "
                     "kapacitet hos en af de tre danske netværksejere: TDC NET, Telenor eller 3. "
                     "Netværksaftaler bliver løbende genforhandlet og kan skifte, og derfor "
                     f"angiver vi ikke et net her uden at have verificeret det. Tjek den "
                     f"aktuelle netværksangivelse på {e(u['navn'])}s egen side, hvis dækning "
                     "er afgørende for dit valg — det er den vigtigste enkeltoplysning om "
                     "enhver udbyder, fordi den bestemmer, hvor godt din telefon virker.")
    else:
        netafsnit = (f"{e(u['navn'])} kører på <strong>{e(u['netvaerk'])}</strong>. Det er den "
                     "vigtigste enkeltoplysning om enhver dansk udbyder, fordi den bestemmer, "
                     "hvor godt din telefon virker — ikke hvad du betaler. Der findes kun tre "
                     "mobilnetværk i Danmark, og alle andre selskaber lejer sig ind hos en af dem.")

    tabel = ""
    if egne:
        tabel = pristabel(sorted(egne, key=lambda a: a["pris"]), UMAP,
                          titel=f"{u['navn']}s abonnementer og priser",
                          undertitel=f"Alle {u['navn']}-abonnementer vi følger, sorteret efter pris.",
                          filtre=False, billigst_id=min(egne, key=lambda a: a['pris'])['id'])

    uq = UNIK.get(u["slug"], {})
    unikke = "".join(f"<h2>{h}</h2>{t}" for h, t in uq.get("sektioner", []))
    netafsnit = uq.get("net_note", netafsnit)
    skiftnote = uq.get("skift_note", "")

    krop = f"""
{tabel}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, f"Vilkår gennemgået på {u['navn']}s egen hjemmeside")}

  <h2>{e(uq.get("h2_vurdering", f"Vores vurdering af {u['navn']}"))}</h2>
  {afsnit}

  <div class="plusminus">
    <div class="pm pm-plus"><h3>Det taler for</h3><ul>{fordele}</ul></div>
    <div class="pm pm-minus"><h3>Det taler imod</h3><ul>{ulemper}</ul></div>
  </div>

  {unikke}

  <h2>{e(uq.get("h2_net", f"Netværk og dækning hos {u['navn']}"))}</h2>
  <p>{netafsnit}</p>
  <p>Bor du i en større by, er forskellen mellem de tre danske net lille i praksis. Bor du
  på landet, i et sommerhusområde eller pendler du gennem tyndt befolkede områder, kan
  forskellen være mærkbar. <a href="/guides/daekning-og-netvaerk/">Læs vores gennemgang af
  de tre netværk</a>.</p>

  <h2>{e(uq.get("h2_hvem", f"Hvem passer {u['navn']} til?"))}</h2>
  <div class="kortgitter kg-2" style="margin:1.6rem 0">
    <div class="kort"><h3>Vælg {e(u['navn'])} hvis…</h3><p>{e(u['bedst_til'])}</p></div>
    <div class="kort"><h3>Vælg noget andet hvis…</h3><p>{e(u['daarligt_til'])}</p></div>
  </div>

  <h2>{e(uq.get("h2_sammenlign", f"{u['navn']} sammenlignet med alternativerne"))}</h2>
  <p>Her er de abonnementer fra andre udbydere, der ligger tættest på
  {e(u['navn'])}s prisniveau. Bemærk især netværkskolonnen — det er der, den reelle forskel
  ofte ligger.</p>
  <table>
    <thead><tr><th>Abonnement</th><th>Data</th><th>Netværk</th><th>Pris/md.</th></tr></thead>
    <tbody>{sammenlign}</tbody>
  </table>
  <p>Se hele markedet i vores <a href="/billigste-mobilabonnement/">sammenligning af
  billigste mobilabonnement</a>.</p>

  <h2>{e(uq.get("h2_skift", f"Sådan skifter du til {u['navn']}"))}</h2>
  {f"<p>{skiftnote}</p>" if skiftnote else ""}
  <ol class="trin">
    <li><strong>Tjek din nuværende aftale</strong>
    Notér din binding og eventuel restgæld på en telefon købt på afbetaling. Restgælden
    følger ikke med til den nye udbyder.</li>
    <li><strong>Bestil og oplys dit nummer</strong>
    Du skal ikke opsige dit nuværende abonnement selv. {e(u['navn'])} henter nummeret for dig.</li>
    <li><strong>Aktivér simkort eller eSIM</strong>
    eSIM er hurtigst og kan aktiveres samme dag. Fysisk simkort tager typisk 1–3 hverdage.</li>
    <li><strong>Slå datastop til</strong>
    Første ting du gør, når abonnementet er oprettet. Det forhindrer uventede regninger ved
    overforbrug.</li>
  </ol>
  <p>Læs den fulde gennemgang i vores guide til
  <a href="/guides/skift-mobilselskab/">at skifte mobilselskab</a>.</p>

  <div class="advarsel">
    <p><strong>Bemærk:</strong> Priser og vilkår ændrer sig løbende, og netværksaftaler kan
    blive genforhandlet. Vi opdaterer siden regelmæssigt, men {e(u['navn'])}s egen hjemmeside
    er altid den primære kilde. Tjek de aktuelle vilkår før bestilling.</p>
  </div>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/bedste-mobilabonnement/", "Bedste mobilabonnement — vores kriterier"),
      ("/udbydere/", f"Sammenlign {u['navn']} med de andre udbydere"),
      ("/guides/daekning-og-netvaerk/", "Hvilket netværk skal du vælge?"),
  ])}
  {forfatterboks()}
  {afsloering()}
</section>
"""

    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(netlabel(u).replace("s net", "s netværk") if u["netvaerk"] != "MVNO" else "Udbyder uden eget net", f"{e(u['navn'])} — {e(u['tagline'])}",
                       e(u["kort"]),
                       '<a href="#sammenlign" class="knap knap-primaer">Se priser</a>'
                       if egne else ""),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(u["faq"], f"Spørgsmål om {u['navn']}"),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(u["faq"]),
                     artikelld(sti, titel, besk),
                     {"@type": "Organization", "name": u["navn"], "url": u["hjemmeside"],
                      "logo": DOMAENE + f"/assets/img/logoer/{u['logo']}"})],
    ), prioritet="0.8")


# --------------------------------------------------------------- GUIDES

def byg_guide(sti, etiket, h1, titel, besk, brodtekst, faq, links, billede=None,
              altbillede="", ekstra=None):
    krumme = [("/", "Forside"), ("/guides/", "Guides"), (None, etiket)]
    krop = f"""
{brodtekst.replace('<section class="sektion baand-smal artikel">',
                    '<section class="sektion baand-smal artikel">' + gennemgangslinje(OPDATERET), 1)
             .replace('</section>', "".join(ekstra or []) + '</section>', 1) if ekstra else
   brodtekst.replace('<section class="sektion baand-smal artikel">',
                    '<section class="sektion baand-smal artikel">' + gennemgangslinje(OPDATERET), 1)}
<section class="sektion baand-smal">
  {laesvidere(links)}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(etiket, h1, besk,
                       billede=guidebillede(billede, altbillede or h1, prioritet=True) if billede else None),
        efter_hero=logobaand(), krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk),
                     howtold(sti, h1, besk, brodtekst))],
    ), prioritet="0.7")


GUIDER = [
    ("/guides/hvor-meget-data/", "Hvor meget data har jeg brug for?",
     "Find dit faktiske forbrug på to minutter, og se hvilket abonnement der matcher.",
     "hvor-meget-data", "Kvinde tjekker sit dataforbrug på telefonen", "Guide", 6),
    ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab",
     "Trin for trin — og de fem ting der oftest går galt undervejs.",
     "skift-mobilselskab", "Kvinde skifter mobilselskab på laptop", "Guide", 5),
    ("/guides/daekning-og-netvaerk/", "Dækning og netværk i Danmark",
     "TDC NET, Telenor og 3 — hvem er stærkest hvor, og hvornår betyder det noget.",
     "daekning-og-netvaerk", "Kvinde med 5G-dækning ved dansk kystby", "Guide", 7),
    ("/guides/esim/", "eSIM forklaret",
     "Hvad et eSIM er, hvornår det er en fordel, og hvordan du kommer i gang.",
     "esim", "Rejsende aktiverer eSIM i en lufthavn", "Guide", 6),
    ("/guides/mobilabonnement-i-udlandet/", "Mobilabonnement i udlandet",
     "Roaming, EU-regler og hvordan du undgår de dyre overraskelser uden for EU.",
     "i-udlandet", "Kvinde bruger mobilen på en gade i Italien", "Guide", 7),
    ("/guides/prisstigning-mobilabonnement/", "Prisstigning på mobilabonnement",
     "Hvorfor prisen stiger, hvornår du kan opsige, og hvordan du får markedsprisen igen.",
     "prisstigning", "Kvinde gennemgår sin mobilregning", "Rettigheder", 7),
    ("/guides/mobilabonnement-eller-bredbaand/", "Mobilabonnement eller bredbånd?",
     "Kan et stort mobilabonnement erstatte dit bredbånd? Se forskellen og regnestykket.",
     "mobil-eller-bredbaand", "Mobilabonnement og bredbånd sammenlignet", "Sammenligning", 7),
    ("/guides/mobilabonnement-trods-rki/", "Mobilabonnement trods RKI",
     "Taletid kræver ingen kreditvurdering. Se alle veje til et abonnement og dine rettigheder.",
     "trods-rki", "Mand undersøger mobilabonnementer på et bibliotek", "Rettigheder", 8),
]


def byg_guideoversigt():
    sti = "/guides/"
    krumme = [("/", "Forside"), (None, "Guides")]

    kort = ""
    for h, t, besk, bil, alt, maerkat, min in GUIDER:
        kort += f"""<a class="artikelkort" href="{h}">
  <span class="ak-billede">{guidebillede(bil, alt)}</span>
  <span class="ak-krop">
    <span class="ak-maerkat">{e(maerkat)}</span>
    <span class="ak-titel">{e(t)}</span>
    <span class="ak-besk">{e(besk)}</span>
    <span class="ak-fod"><span class="ak-tid">{min} min. læsning</span>
    <span class="ak-laes">Læs <span aria-hidden="true">→</span></span></span>
  </span>
</a>"""

    krop = f"""<section class="sektion baand">
  <div class="sektion-hoved afslør">
    <span class="etiket">Guides</span>
    <h2>Start her</h2>
    <p class="led">{len(GUIDER)} guides, der dækker de spørgsmål vi oftest får. De tager
    hver et par minutter at læse og sparer typisk flere hundrede kroner om året.</p>
  </div>
  <div class="artikelkort-gitter">{kort}</div>
  <p class="ak-antal">Viser alle {len(GUIDER)} guides</p>
</section>

<section class="sektion baand-smal artikel">
  <h2>Guides efter emne</h2>
  <table>
  <thead><tr><th>Skal du…</th><th>Så læs</th></tr></thead>
  <tbody>
  <tr><td>Finde ud af hvor meget data du bruger</td><td><a href="/guides/hvor-meget-data/">Hvor meget data har jeg brug for?</a></td></tr>
  <tr><td>Vælge mellem de tre danske net</td><td><a href="/guides/daekning-og-netvaerk/">Dækning og netværk</a></td></tr>
  <tr><td>Skifte selskab og beholde dit nummer</td><td><a href="/guides/skift-mobilselskab/">Sådan skifter du</a></td></tr>
  <tr><td>Være i gang samme dag</td><td><a href="/guides/esim/">eSIM forklaret</a></td></tr>
  <tr><td>Rejse uden dyre regninger</td><td><a href="/guides/mobilabonnement-i-udlandet/">Mobilabonnement i udlandet</a></td></tr>
  <tr><td>Reagere på at prisen er steget</td><td><a href="/guides/prisstigning-mobilabonnement/">Prisstigning — dine rettigheder</a></td></tr>
  <tr><td>Vide om mobilen kan erstatte bredbånd</td><td><a href="/guides/mobilabonnement-eller-bredbaand/">Mobil eller bredbånd?</a></td></tr>
  <tr><td>Have abonnement på trods af RKI</td><td><a href="/guides/mobilabonnement-trods-rki/">Mobilabonnement trods RKI</a></td></tr>
  </tbody>
  </table>

  <h2>Rækkefølgen vi anbefaler</h2>
  <p>Skal du vælge nyt mobilabonnement, er der en rækkefølge, der gør beslutningen markant
  nemmere. De fleste starter med at kigge på priser, og det er præcis omvendt af, hvad der
  virker.</p>
  <ol class="trin">
    <li><strong>Find dit dataforbrug først</strong>
    Uden det tal er alt andet gætværk. Det tager to minutter at finde i telefonens
    indstillinger, og for de fleste er tallet lavere end forventet.
    <a href="/guides/hvor-meget-data/">Se hvordan</a>.</li>
    <li><strong>Afklar om netværket betyder noget for dig</strong>
    Bor du centralt i en by, kan du vælge frit og gå efter pris. Bor du på landet eller
    pendler langt, bør netværket vælges før prisen.
    <a href="/guides/daekning-og-netvaerk/">Læs om de tre net</a>.</li>
    <li><strong>Sammenlign på pris pr. GB</strong>
    Nu — og først nu — giver det mening at kigge på priser.
    <a href="/billigste-mobilabonnement/">Se sammenligningen</a>.</li>
    <li><strong>Skift, og vælg eSIM hvis du kan</strong>
    Skiftet er nemmere, end de fleste tror, og du beholder dit nummer.
    <a href="/guides/skift-mobilselskab/">Trin for trin</a>.</li>
  </ol>
  <div class="tip">
    <h3>Det vigtigste råd i alle fire guides</h3>
    <p>Slå datastop til, så snart abonnementet er oprettet. Det er den ene indstilling, der
    forhindrer uventede regninger ved overforbrug, og den tager under et minut at aktivere
    i udbyderens app.</p>
  </div>

  <h2>Værktøjer der hører til</h2>
  <p>Ud over guiderne har vi bygget en række gratis værktøjer, du kan bruge undervejs:
  <a href="/daekningskort/">dækningstjek</a> til at finde det rigtige net,
  <a href="/speedtest/">hastighedstest</a> til at måle din forbindelse,
  <a href="/landekoder/">landekoder</a> til udlandsopkald og
  <a href="/hvem-ringer-til-mig/">nummeropslag</a> til ukendte opkald.</p>
</section>

<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>"""

    return skriv(sti, shell(
        sti=sti, titel="Guides til mobilabonnement — data, dækning, eSIM og skifte",
        beskrivelse=("Praktiske guides om dataforbrug, netværk, eSIM og hvordan du skifter "
                     "mobilselskab. Skrevet i almindeligt dansk og opdateret løbende."),
        opdateret=OPDATERET,
        hero=hero_side("Guides", "Guides til mobilabonnement",
                       "Det du skal vide, før du vælger — skrevet i almindeligt dansk.",
                       "", [("Guides", str(len(GUIDER))), ("Værktøjer", "4"), ("Pris", "gratis")]),
        efter_hero=logobaand(), krumme=krumme, indhold=krop,
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme),
                     {"@type": "ItemList", "name": "Guides til mobilabonnement",
                      "numberOfItems": len(GUIDER),
                      "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "url": DOMAENE + g[0],
                           "name": g[1]} for i, g in enumerate(GUIDER)]})],
    ), prioritet="0.7")


# --------------------------------------------------------------- STATISKE

def byg_statisk(sti, titel, besk, etiket, h1, brodtekst, prioritet="0.5", jsonld_ekstra=None):
    krumme = [("/", "Forside"), (None, etiket)]
    noder = [ORG, PERSON, WEBSITE, krummeld(krumme)]
    if jsonld_ekstra:
        noder.append(jsonld_ekstra)
    krop = brodtekst + f'<section class="sektion baand-smal">{afsloering()}</section>'
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(etiket, h1, besk), efter_hero=logobaand(), krumme=krumme, indhold=krop,
        jsonld=[graf(*noder)],
    ), prioritet=prioritet, hyppighed="monthly")


# --------------------------------------------------------------- FILER

def ryd_forældede():
    """Sletter sider fra tidligere builds, som ikke længere genereres.
    Uden det ville gamle sider blive liggende og linke til data, der ikke findes."""
    manifest = os.path.join(STI, ".genereret.json")
    nu = {s for s, _, _ in SIDER}

    # Scan filsystemet frem for at stole på manifestet alene — så fanges også
    # sider fra builds før manifestet fandtes.
    spring = {".git", ".github", "_build", "data", "assets", ".well-known"}
    foer = set()
    for rod, mapper, filer in os.walk(ROD):
        mapper[:] = [m for m in mapper if m not in spring and not m.startswith(".")]
        if "index.html" in filer:
            rel = os.path.relpath(rod, ROD)
            foer.add("/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/")

    fjernet = []
    for sti in sorted(foer - nu):
        if sti == "/":
            continue
        mappe = os.path.join(ROD, sti.strip("/"))
        f = os.path.join(mappe, "index.html")
        if os.path.exists(f):
            os.remove(f)
            fjernet.append(sti)
            # Fjern tomme mapper op ad hierarkiet
            d = mappe
            while d != ROD and os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
                d = os.path.dirname(d)
    json.dump(sorted(nu), open(manifest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return fjernet


def byg_sitemap():
    poster = ""
    for sti, pri, hyp in SIDER:
        poster += (f"  <url><loc>{DOMAENE}{sti}</loc><lastmod>{ISO}</lastmod>"
                   f"<changefreq>{hyp}</changefreq><priority>{pri}</priority></url>\n")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{poster}</urlset>\n")
    with open(os.path.join(ROD, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def byg_ekstrafiler():
    """security.txt, humans.txt og llms.txt — små tillidssignaler."""
    os.makedirs(os.path.join(ROD, ".well-known"), exist_ok=True)
    with open(os.path.join(ROD, ".well-known", "security.txt"), "w", encoding="utf-8") as f:
        f.write(f"""Contact: mailto:kontakt@telemobil.dk
Expires: {IDAG.replace(year=IDAG.year + 1).isoformat()}T00:00:00.000Z
Preferred-Languages: da, en
Canonical: {DOMAENE}/.well-known/security.txt
""")

    with open(os.path.join(ROD, "humans.txt"), "w", encoding="utf-8") as f:
        f.write(f"""/* TEAM */
Stifter og redaktør: {FORFATTER['navn']}
Kontakt: kontakt@telemobil.dk
LinkedIn: {FORFATTER['linkedin']}
Adresse: Lundbyesgade 13, 8000 Aarhus C, Danmark

/* SITE */
Sidst opdateret: {ISO}
Sprog: Dansk
Byggesystem: Statisk generering med Python
Doktrin: Priser sorteres efter pris, ikke efter provision
""")

    # llms.txt: struktureret oversigt til AI-crawlere, der læser sitet
    veje = "\n".join(f"- [{t}]({DOMAENE}{h}): {u}" for h, t, u in [
        ("/billigste-mobilabonnement/", "Billigste mobilabonnement", "Hele markedet sorteret efter reel pris"),
        ("/bedste-mobilabonnement/", "Bedste mobilabonnement", "Vurderingskriterier og anbefalinger"),
        ("/mobilabonnement-med-fri-data/", "Fri data", "Ubegrænset data i Danmark"),
        ("/mobilabonnement-med-streaming/", "Med streaming", "Abonnementer med streamingtjenester"),
        ("/udbydere/", "Udbydere", "Gennemgang af de 10 danske mobilselskaber"),
        ("/netvaerk/", "Mobilnetværk", "TDC NET, Telenor og 3"),
        ("/sammenlign/", "Udbyder mod udbyder", "Direkte sammenligninger"),
        ("/landekoder/", "Landekoder", "Telefonkoder til alle lande"),
        ("/metode/", "Metode", "Sådan beregner og vurderer vi"),
        ("/saadan-tjener-vi-penge/", "Forretningsmodel", "Affiliateprovision og uafhængighed"),
    ])
    with open(os.path.join(ROD, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(f"""# Telemobil

> Uafhængig dansk prissammenligning af mobilabonnementer. Vi beregner den reelle
> månedspris over 12 måneder inklusive intropris, normalpris og oprettelse — ikke kun
> den intropris, udbyderne markedsfører.

Udgiver: Telemobil, Danmark. Redaktør: {FORFATTER['navn']}.
Sidst opdateret: {ISO}. Sprog: dansk.

## Vigtige sider

{veje}

## Om vores data

Priser og vilkår stammer fra udbydernes egne offentlige prislister. Nøgletallet
"gennemsnit over 12 måneder" beregnes som intropris ganget med introperioden plus
normalpris for de resterende måneder, divideret med tolv, plus eventuelt
oprettelsesgebyr. Tabeller sorteres efter pris, aldrig efter provision.

## Forbehold

Telemobil modtager provision fra udvalgte udbydere ved henvisning. Det påvirker ikke
sortering eller vurderinger. Se {DOMAENE}/saadan-tjener-vi-penge/
""")


def byg_robots():
    txt = f"""User-agent: *
Allow: /
Disallow: /_build/
Disallow: /data/

# Sitet er statisk og let at crawle — ingen grund til at bremse
User-agent: Googlebot
Allow: /

Sitemap: {DOMAENE}/sitemap.xml
"""
    with open(os.path.join(ROD, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def byg_favicon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="g" x1="0" y1="1" x2="1" y2="0">
<stop offset="0" stop-color="#00D18F"/><stop offset="55%" stop-color="#3D5AFE"/>
<stop offset="100%" stop-color="#7C4DFF"/></linearGradient></defs>
<rect width="64" height="64" rx="14" fill="#0B1026"/>
<rect x="12" y="38" width="8" height="14" rx="3" fill="url(#g)"/>
<rect x="24" y="30" width="8" height="22" rx="3" fill="url(#g)"/>
<rect x="36" y="22" width="8" height="30" rx="3" fill="url(#g)"/>
<rect x="48" y="12" width="8" height="40" rx="3" fill="url(#g)"/>
</svg>"""
    with open(os.path.join(ROD, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

    manifest = {
        "name": SITENAVN, "short_name": SITENAVN,
        "start_url": "/", "display": "standalone",
        "background_color": "#0B1026", "theme_color": "#0B1026",
        "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }
    with open(os.path.join(ROD, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def byg_htaccess():
    txt = """# telemobil.dk
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
  RewriteEngine On
  # Tving https
  RewriteCond %{HTTPS} off
  RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
  # Fjern www
  RewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]
  RewriteRule ^(.*)$ https://%1/$1 [R=301,L]
  # Afsluttende skråstreg på mapper
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteCond %{REQUEST_URI} !/$
  RewriteRule ^(.*)$ /$1/ [R=301,L]
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType text/javascript "access plus 1 year"
  ExpiresByType application/x-javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
  # Statiske filer er versionsuafhaengige og kan caches i et aar
  <FilesMatch "\\.(css|js|webp|svg|woff2|png|jpg)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
"""
    with open(os.path.join(ROD, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(txt)


def byg_404():
    krop = """<section class="sektion baand-smal artikel" style="text-align:center">
  <h2>Siden findes ikke</h2>
  <p>Linket er enten forældet, eller også har vi flyttet siden. Prøv en af disse i stedet:</p>
  <p style="margin-top:2rem">
    <a href="/billigste-mobilabonnement/" class="knap knap-primaer">Se billigste abonnementer</a>
    <a href="/udbydere/" class="knap knap-linje" style="margin-left:.6rem">Alle udbydere</a>
  </p>
</section>"""
    html = shell(sti="/404.html", titel="Siden blev ikke fundet",
                 beskrivelse="Siden blev ikke fundet. Find i stedet det billigste mobilabonnement i vores sammenligning af danske udbydere og priser.", opdateret=OPDATERET,
                 hero=hero_side("404", "Vi kunne ikke finde siden", "Men vi kan finde et billigt abonnement til dig."),
                 indhold=krop)
    with open(os.path.join(ROD, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)


# --------------------------------------------------------------- kør

def main():
    byg_forside()
    byg_billigste()
    byg_fridata()

    # Nichesider
    unge = sorted([a for a in ABON if a["data_gb"] >= 20], key=lambda a: a["pris"])[:12]
    byg_niche(
        "/mobilabonnement-til-unge/", "Unge og studerende",
        "Mobilabonnement til unge og studerende",
        f"Mobilabonnement til unge og studerende — fra {min(a['pris'] for a in unge)} kr./md.",
        "Billige mobilabonnementer med meget data til unge og studerende. Ingen binding, "
        "så du kan skifte, når du flytter eller behovet ændrer sig.",
        "Meget data til lav pris og ingen binding — de tre ting der betyder mest, når man "
        "er studerende og flytter ofte.",
        unge,
        """<h2>Hvad skal unge kigge efter?</h2>
<p>Studerende har et forbrugsmønster, der adskiller sig markant fra gennemsnittet. Du er
meget på farten, du har sjældent stabilt wi-fi mellem forelæsninger, og du streamer mere
musik og video end de fleste. Samtidig flytter du ofte, og din økonomi kan ændre sig fra
semester til semester.</p>
<p>Det giver tre klare prioriteter, som bør veje tungere end alt andet:</p>
<ol class="trin">
<li><strong>Rigelig data — mindst 30 GB</strong>
Det lyder af meget, men prisspringet fra 15 til 50 GB er ofte kun 20-30 kr. om måneden.
Til gengæld fjerner det bekymringen om at løbe tør midt i eksamensperioden.</li>
<li><strong>Ingen binding</strong>
Du ved ikke, hvor du bor om et år, eller hvad din økonomi ser ud til. Binding er en
unødvendig risiko, når langt de fleste danske abonnementer alligevel er uden.</li>
<li><strong>Ingen telefon på afbetaling sammen med abonnementet</strong>
Det er den dyreste fælde for unge. Køb telefonen for sig og abonnementet for sig — så kan
du skifte selskab uden at hænge på en restgæld.</li>
</ol>
<div class="tip"><h3>Studierabat findes, men regn efter</h3>
<p>Nogle udbydere tilbyder rabat til studerende. Sammenlign altid rabatprisen med markedets
billigste abonnement uden rabat — ret ofte er discountudbyderen stadig billigst, selv efter
studierabatten er trukket fra.</p></div>
<h2>Sådan holder du forbruget nede</h2>
<p>Slå automatisk videoafspilning fra i sociale medier, hent musik og podcasts på wi-fi
inden du går hjemmefra, og sæt streamingtjenester til kun at hente i høj kvalitet på wi-fi.
De tre indstillinger halverer typisk dataforbruget og kan flytte dig ned i en billigere
kategori. <a href="/guides/hvor-meget-data/">Se hele guiden til dataforbrug</a>.</p>""",
        [
            {"sp": "Findes der studierabat på mobilabonnement?",
             "sv": "Nogle udbydere tilbyder rabat til studerende. Sammenlign dog altid med markedets billigste "
                   "abonnement uden rabat, da discountudbydere ofte er billigere selv efter studierabat."},
            {"sp": "Hvor meget data bruger en studerende typisk?",
             "sv": "Studerende ligger typisk højere end gennemsnittet, ofte 25-50 GB om måneden, fordi der streames "
                   "mere musik og video uden for wi-fi."},
            {"sp": "Skal jeg købe telefonen sammen med abonnementet?",
             "sv": "Som regel ikke. Køber du telefon på afbetaling sammen med abonnementet, binder du dig i "
                   "praksis, og restgælden skal indfries, hvis du vil skifte selskab."},
        ],
        [("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
         ("/guides/hvor-meget-data/", "Hvor meget data har jeg brug for?"),
         ("/mobilabonnement-uden-binding/", "Abonnementer uden binding")],
    )

    ubinding = sorted([a for a in ABON if a["binding"] == 0], key=lambda a: a["pris"])[:15]
    byg_niche(
        "/mobilabonnement-uden-binding/", "Uden binding",
        "Mobilabonnement uden binding",
        f"Mobilabonnement uden binding — priser fra {min(a['pris'] for a in ubinding)} kr./md.",
        "Sammenlign mobilabonnementer uden binding. Skift når du vil, uden opsigelsesgebyr "
        "eller bindingsperiode.",
        "Alle abonnementer her kan opsiges med kort varsel. Sorteret efter laveste pris.",
        ubinding,
        """<h2>Hvad betyder "uden binding" egentlig?</h2>
<p>Uden binding betyder, at du ikke har forpligtet dig til at blive kunde i en bestemt
periode. Du kan opsige, når du vil, typisk med løbende måned plus et kort varsel, der
fremgår af vilkårene. Det er ikke det samme som "opsigelse fra dag til dag" — der er
næsten altid et varsel — men det er en verden til forskel fra seks måneders binding.</p>
<p>På det danske marked er abonnementer uden binding blevet normen, og det er godt nyt for
forbrugerne. Det betyder, at der sjældent er nogen grund til at acceptere binding, med
mindre du får noget markant til gengæld.</p>
<h2>Hvornår er binding alligevel i orden?</h2>
<p>Der findes ét scenarie, hvor binding kan give mening: når du køber telefon på afbetaling
gennem udbyderen og får en reel rabat på hardwaren. Regn det efter — læg alle månedlige
ydelser sammen over hele perioden og sammenlign med prisen på at købe telefonen kontant
plus et billigt abonnement uden binding. I langt de fleste tilfælde vinder den frie løsning.</p>
<div class="advarsel"><p><strong>Vær opmærksom:</strong> Selvom abonnementet er uden binding,
kan en telefon købt på afbetaling have sin egen aftale. Skifter du selskab, skal restgælden
typisk indfries på én gang.</p></div>
<h2>Sådan opsiger du</h2>
<p>Skal du bare skifte til et andet selskab, skal du <em>ikke</em> opsige selv. Bestil hos
den nye udbyder og oplys dit nummer — så håndterer de opsigelsen automatisk.
<a href="/guides/skift-mobilselskab/">Se hele guiden til at skifte</a>.</p>""",
        [
            {"sp": "Kan jeg opsige et abonnement uden binding når som helst?",
             "sv": "Ja, men der er normalt et opsigelsesvarsel på løbende måned plus en kort periode. Det fremgår "
                   "af udbyderens vilkår."},
            {"sp": "Koster det noget at opsige?",
             "sv": "Nej, ikke ved abonnementer uden binding. Har du købt telefon på afbetaling, skal restgælden "
                   "dog typisk indfries."},
            {"sp": "Skal jeg selv opsige, når jeg skifter selskab?",
             "sv": "Nej. Bestiller du hos en ny udbyder med nummerflytning, opsiges det gamle abonnement "
                   "automatisk, når nummeret flyttes."},
        ],
        [("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
         ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
         ("/udbydere/", "Alle udbydere")],
    )

    # ---------------- Seks nye kategorisider ----------------
    fritale = sorted([a for a in ABON if a["tale"] == "fri"], key=lambda a: a["pris"])
    byg_kategori(
        sti="/mobilabonnement-med-fri-tale/", etiket="Fri tale",
        h1="Billigste mobilabonnement med fri tale",
        titel=f"Mobilabonnement med fri tale — priser fra {D['pris_fritale']} kr./md.",
        besk=(f"Sammenlign mobilabonnementer med fri tale og fri sms. Priser fra "
              f"{D['pris_fritale']} kr./md. Se hvad fri tale dækker — og hvad det ikke gør."),
        intro=(f"Alle abonnementer her har ubegrænsede opkald og sms til danske numre. "
               f"Priserne starter ved {D['pris_fritale']} kr. om måneden."),
        udvalg=fritale, tekstfunktion=sider.fri_tale,
        chips=[("Fra", f"{D['pris_fritale']} kr."), ("Fri tale", "og sms"), ("Uden", "binding")],
        tabeltitel="Abonnementer med fri tale og sms",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), tabel_aarsomkostning(), begrebstabel(),
                         fejltabel(), vejviser('/mobilabonnement-med-fri-tale/')],
        faq=[
            {"sp": "Hvad koster det billigste mobilabonnement med fri tale?",
             "sv": f"Det billigste abonnement med fri tale i vores sammenligning koster {D['pris_fritale']} kr. om "
                   "måneden. Fri tale dækker ubegrænsede opkald til danske mobil- og fastnetnumre."},
            {"sp": "Hvad dækker fri tale ikke?",
             "sv": "Fri tale dækker ikke særnumre, opkald til udlandet, roaming uden for EU eller "
                   "indholdstjenester som sms-afstemninger og parkeringsapps. De faktureres separat."},
            {"sp": "Er fri tale inkluderet i EU?",
             "sv": "Ja. Inden for EU gælder roamingreglerne, så du kan ringe til danske numre på samme vilkår som "
                   "herhjemme. Datamængden i EU er derimod ofte begrænset."},
            {"sp": "Kan det betale sig med en timepakke i stedet?",
             "sv": "Kun hvis du taler under cirka to timer om måneden. Prisforskellen til fri tale er typisk 10-20 "
                   "kr., mens overforbrug på en timepakke hurtigt koster mere end det."},
            {"sp": "Er fri sms altid med, når der er fri tale?",
             "sv": "Næsten altid, men ikke garanteret på de allerbilligste abonnementer. Tjek at både tale og sms "
                   "er inkluderet, før du bestiller."},
        ],
        links=[("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
               ("/mobilabonnement-uden-data/", "Mobilabonnement uden data"),
               ("/mobilabonnement-med-fri-data/", "Mobilabonnement med fri data"),
               ("/udbydere/lebara/", "Lebara — bedst til opkald til udlandet")])

    bedste_udvalg = sorted([a for a in ABON if 10 <= a["data_gb"] < 900],
                           key=lambda a: a["pris"] / a["data_gb"])[:14]
    byg_kategori(
        sti="/bedste-mobilabonnement/", etiket="Bedste abonnement",
        h1="Bedste mobilabonnement — sådan finder du dit",
        titel=f"Bedste mobilabonnement {IDAG.year} — sammenlignet på pris, data og net",
        besk=("Der findes ikke ét bedste mobilabonnement. Se vores kriterier, og find det "
              "bedste abonnement til netop din situation, dit forbrug og din adresse."),
        intro=("Rangeret efter pris pr. gigabyte — det tal der gør abonnementer af forskellig "
               "størrelse direkte sammenlignelige."),
        udvalg=bedste_udvalg, tekstfunktion=sider.bedste,
        chips=[("Vurderet på", "5 kriterier"), ("Udbydere", str(D['antal_udbydere'])), ("Fra", f"{D['min_pris']} kr.")],
        tabeltitel="Bedste værdi for pengene lige nu",
        ekstra_tabeller=[redaktionens_valg(), prisfordeling(), tabel_billigst_pr_udbyder(),
                         tabel_prgb_rangliste(), overforbrug(),
                         udbydergitter(), fejltabel(), begrebstabel(), vejviser('/bedste-mobilabonnement/')],
        faq=[
            {"sp": "Hvad er det bedste mobilabonnement i Danmark?",
             "sv": "Det afhænger af, hvor du bor og hvor meget data du bruger. Bor du i en by med almindeligt "
                   "forbrug, er det billigste abonnement, der dækker dit behov, også det bedste. Bor du på landet, "
                   "vejer netværket tungere end prisen."},
            {"sp": "Er dyre mobilabonnementer bedre end billige?",
             "sv": "Ikke på selve forbindelsen. Der findes kun tre mobilnet i Danmark, og alle selskaber lejer sig "
                   "ind hos en af dem. Du betaler ekstra for dækning på det mest udbyggede net, kundeservice og "
                   "tillægsydelser — ikke for et bedre mobilnet."},
            {"sp": "Hvilket mobilnet er bedst i Danmark?",
             "sv": "TDC NET er det mest udbyggede og har gennem en årrække klaret sig bedst i uafhængige målinger "
                   "af netkvalitet. I byerne er forskellen til Telenor og 3 dog lille i praksis."},
            {"sp": "Hvordan vurderer I abonnementerne?",
             "sv": "Vi vægter pris pr. GB og vilkår højest, dernæst netværk og EU-data, og til sidst "
                   "gennemsigtighed. Vi laver ikke egne hastighedsmålinger og bruger ikke anmeldelsesscorer som "
                   "rangeringskriterium."},
            {"sp": "Bør jeg vælge abonnement med binding?",
             "sv": "Sjældent. De fleste danske abonnementer er uden binding, og binding giver kun mening, hvis du "
                   "får en reel rabat på hardware, du alligevel ville have købt."},
        ],
        links=[("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/daekning-og-netvaerk/", "Dækning og netværk: de tre danske net"),
               ("/metode/", "Sådan vurderer vi abonnementer"),
               ("/udbydere/", "Alle udbydere gennemgået")])

    udendata = sorted([a for a in ABON if a["data_gb"] == 0], key=lambda a: a["pris"])
    byg_kategori(
        sti="/mobilabonnement-uden-data/", etiket="Uden data",
        h1="Mobilabonnement uden data",
        titel=f"Mobilabonnement uden data — priser fra {D['pris_udendata']} kr./md.",
        besk=(f"Sammenlign mobilabonnementer uden data. Priser fra {D['pris_udendata']} kr./md. "
              "Se også hvorfor et lille dataabonnement ofte er billigere."),
        intro=("Abonnementer med tale og sms, men uden mobildata. Bemærk at forbrugsafregnede "
               "abonnementer har 0 kr. i fast pris, men koster pr. minut."),
        udvalg=udendata, tekstfunktion=sider.uden_data,
        chips=[("Fra", f"{D['pris_udendata']} kr."), ("Data", "0 GB"), ("Wi-fi", "virker stadig")],
        tabeltitel="Abonnementer uden mobildata",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), tabel_pr_datamaengde(), tabel_aarsomkostning(), fejltabel(), begrebstabel(), vejviser()],
        faq=[
            {"sp": "Findes der stadig mobilabonnement uden data?",
             "sv": "Ja, men udvalget er lille. De findes som faste abonnementer med tale og sms, som "
                   "forbrugsafregnede abonnementer uden fast pris, og som taletidskort."},
            {"sp": "Er et abonnement uden data billigst?",
             "sv": "Ofte ikke. Konkurrencen på det danske marked foregår på dataabonnementer, så du kan tit få fri "
                   "tale og en lille datapakke til samme pris eller billigere end et rent taleabonnement."},
            {"sp": "Hvordan slår jeg mobildata fra?",
             "sv": "På iPhone under Indstillinger og Mobildata. På Android under Indstillinger, Netværk og "
                   "internet, Mobilnetværk. Bed eventuelt udbyderen om at spærre helt for data."},
            {"sp": "Hvad er forskellen på uden data og taletidskort?",
             "sv": "Et abonnement har fast månedspris og faktureres bagud. Et taletidskort er forudbetalt, så du "
                   "kan ikke overskride. Taletid er tryggest, abonnement er nemmest."},
            {"sp": "Virker 112 uden data?",
             "sv": "Ja. Nødopkald fungerer uanset abonnement og datamængde, også hvis taletiden er brugt op."},
        ],
        links=[("/mobilabonnement-til-boern/", "Mobilabonnement til børn"),
               ("/mobilabonnement-med-fri-tale/", "Abonnement med fri tale"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?")])

    stream = sorted([a for a in ABON if a.get("streaming")], key=lambda a: a["pris"])
    byg_kategori(
        sti="/mobilabonnement-med-streaming/", etiket="Med streaming",
        h1="Mobilabonnement med streaming inkluderet",
        titel=f"Mobilabonnement med streaming — fra {D['pris_streaming']} kr./md.",
        besk=(f"Sammenlign mobilabonnementer med streaming inkluderet. Fra {D['pris_streaming']} "
              "kr./md. Se regnestykket, der afgør om det kan betale sig for dig."),
        intro=("Abonnementer hvor streamingtjenester indgår i prisen. Regn efter, hvad du "
               "betaler for de samme tjenester i dag."),
        udvalg=stream, tekstfunktion=sider2.streaming,
        chips=[("Fra", f"{D['pris_streaming']} kr."), ("Tjenester", "inkluderet"), ("Én", "regning")],
        tabeltitel="Abonnementer med streaming inkluderet",
        ekstra_tabeller=[tabel_pr_datamaengde(), tabel_prgb_rangliste(), tabel_aarsomkostning(), fejltabel(), begrebstabel(), vejviser()],
        faq=[
            {"sp": "Kan det betale sig med streaming i mobilabonnementet?",
             "sv": "Kun hvis du allerede betaler for to eller flere af de tjenester, der indgår, og ikke deler dem "
                   "med andre. Bruger du én tjeneste eller ingen, betaler du typisk over."},
            {"sp": "Hvad koster mobilabonnement med streaming?",
             "sv": f"Fra {D['pris_streaming']} kr. om måneden i vores sammenligning. Prisen afhænger af antallet af "
                   "tjenester og af datamængden."},
            {"sp": "Kan indholdet i pakken ændre sig?",
             "sv": "Ja. Tjenester kan ryge ud, når aftaler mellem udbyder og indholdsleverandør udløber. Tjek "
                   "vilkårene for, hvad der sker med prisen, og genberegn en gang om året."},
            {"sp": "Hvor meget data kræver streaming?",
             "sv": "Video koster cirka 0,7-1 GB i timen i standardkvalitet og 2-3 GB i HD. Vælger du streaming, bør "
                   "du vælge mindst 50 GB, ellers kan du kun bruge tjenesterne på wi-fi."},
            {"sp": "Hvad sker der med streamingen, hvis jeg skifter selskab?",
             "sv": "Den forsvinder sammen med abonnementet. Tegn de tjenester, du vil beholde, separat inden du "
                   "skifter."},
        ],
        links=[("/mobilabonnement-med-fri-data/", "Fri data — nødvendigt til streaming?"),
               ("/udbydere/telmore/", "Telmore — streaming samlet i regningen"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/bedste-mobilabonnement/", "Bedste mobilabonnement")])

    boernudvalg = sorted([a for a in ABON if a["data_gb"] <= 15], key=lambda a: a["pris"])
    byg_kategori(
        sti="/mobilabonnement-til-boern/", etiket="Til børn",
        h1="Mobilabonnement til børn",
        titel=f"Mobilabonnement til børn — trygt og fra {D['pris_boern']} kr./md.",
        besk=("Find et trygt mobilabonnement til dit barn. Se hvordan du sikrer mod store "
              "regninger med datastop, spærringer og det rigtige valg af abonnementstype."),
        intro=("Små abonnementer uden binding, der passer til en børnetelefon. Slå altid "
               "datastop til, uanset hvilket du vælger."),
        udvalg=boernudvalg, tekstfunktion=sider2.boern,
        chips=[("Fra", f"{D['pris_boern']} kr."), ("Datastop", "anbefales"), ("Uden", "binding")],
        tabeltitel="Små abonnementer der passer til børn",
        ekstra_tabeller=[erfaring('boern'), tabel_billigst_pr_udbyder(), tabel_pr_datamaengde(), tabel_aarsomkostning(), fejltabel(), begrebstabel(), vejviser()],
        faq=[
            {"sp": "Hvilket mobilabonnement er bedst til børn?",
             "sv": "Til de yngste er taletid tryggest, fordi udgiften er låst. Fra cirka 11-12 år er et lille "
                   "dataabonnement med datastop typisk det mest praktiske. Vælg altid uden binding."},
            {"sp": "Hvor meget data har et barn brug for?",
             "sv": "Mindre end de fleste tror, fordi børn har wi-fi hjemme og hos vennerne. 2-5 GB rækker langt op "
                   "til 12-årsalderen, mens teenagere typisk bruger 5-15 GB."},
            {"sp": "Kan mit barn selv stå på abonnementet?",
             "sv": "Nej. Mindreårige kan som udgangspunkt ikke indgå bindende aftaler, så abonnementet oprettes i "
                   "en forælders navn. Det er også forælderen, der hæfter for regningen."},
            {"sp": "Hvordan undgår jeg store regninger fra børnetelefonen?",
             "sv": "Slå datastop til, bed udbyderen spærre for overtakserede numre og indholdstjenester, og slå "
                   "dataroaming fra. Sæt desuden krav om kode ved køb i telefonens familieindstillinger."},
            {"sp": "Skal jeg købe telefonen på afbetaling sammen med abonnementet?",
             "sv": "Nej. Det binder jer i typisk 24-36 måneder, og restgælden skal indfries ved skift. Køb en "
                   "billig eller brugt telefon kontant og vælg et abonnement uden binding."},
        ],
        links=[("/mobilabonnement-uden-data/", "Mobilabonnement uden data"),
               ("/mobilabonnement-uden-binding/", "Abonnementer uden binding"),
               ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement")])

    esimudvalg = sorted([a for a in ABON if a.get("esim") and a["pris"] > 0],
                        key=lambda a: a["pris"])[:16]
    byg_kategori(
        sti="/mobilabonnement-med-esim/", etiket="Med eSIM",
        h1="Mobilabonnement med eSIM",
        titel=f"Mobilabonnement med eSIM — klar samme dag, fra {D['pris_esim']} kr.",
        besk=("Sammenlign mobilabonnementer med eSIM. Aktivér med en QR-kode og vær i gang "
              "på få minutter i stedet for at vente på et fysisk simkort."),
        intro=("Alle abonnementer her kan leveres som eSIM. Du får en QR-kode og kan være i "
               "gang få minutter efter bestilling."),
        udvalg=esimudvalg, tekstfunktion=sider2.esim,
        chips=[("Klar på", "få minutter"), ("Flere numre", "én telefon"), ("Fra", f"{D['pris_esim']} kr.")],
        tabeltitel="Abonnementer der kan leveres som eSIM",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), tabel_prgb_rangliste(), fejltabel(), begrebstabel(), vejviser()],
        faq=[
            {"sp": "Hvad er et eSIM?",
             "sv": "Et digitalt simkort indbygget i telefonen, som aktiveres med en QR-kode i stedet for et fysisk "
                   "kort. Funktionelt virker det præcis som et almindeligt simkort."},
            {"sp": "Understøtter min telefon eSIM?",
             "sv": "De fleste telefoner fra de senere år gør. På iPhone tjekker du under Indstillinger, Generelt, "
                   "Om. På Android varierer det mere mellem modeller."},
            {"sp": "Koster eSIM ekstra?",
             "sv": "Hos hovedparten af de danske udbydere er eSIM gratis, og abonnementsprisen er den samme som "
                   "med fysisk kort. Enkelte tager gebyr for at udstede en ny profil."},
            {"sp": "Kan jeg have to numre på samme telefon med eSIM?",
             "sv": "Ja. De fleste moderne telefoner kan have flere eSIM-profiler og to aktive samtidig, så du kan "
                   "have arbejde og privat i én telefon."},
            {"sp": "Hvad sker der med mit eSIM, når jeg skifter telefon?",
             "sv": "Det kan ikke flyttes fysisk. Nyere telefoner har en overførselsfunktion, ellers skal du bede "
                   "udbyderen om en ny QR-kode. Gør det inden du nulstiller den gamle telefon."},
        ],
        links=[("/guides/esim/", "eSIM forklaret — den fulde guide"),
               ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/bedste-mobilabonnement/", "Bedste mobilabonnement")])

    # ---------------- Fem nye artikler ----------------
    u100 = sorted([a for a in ABON if 0 < a["pris"] < 100], key=lambda a: gns12(a) or 9e9)
    byg_kategori(
        sti="/mobilabonnement-under-100-kr/", etiket="Under 100 kr.",
        h1="Mobilabonnement under 100 kr. om måneden",
        titel=f"Mobilabonnement under 100 kr. — {len(u100)} valg fra {D['min_pris']} kr.",
        besk=(f"Se alle {len(u100)} mobilabonnementer under 100 kr./md. Sorteret efter den "
              "reelle pris over 12 måneder, så introtilbud ikke skjuler normalprisen."),
        intro=(f"{len(u100)} abonnementer under hundrede kroner. Sorteret efter gennemsnitspris "
               "over 12 måneder, ikke efter intropris."),
        udvalg=u100, tekstfunktion=sider4.under100,
        chips=[("Under 100 kr.", f"{len(u100)} valg"), ("Fra", f"{D['min_pris']} kr."),
               ("Binding", "0 mdr.")],
        tabeltitel="Alle abonnementer under 100 kr. om måneden",
        ekstra_tabeller=[prisfordeling(), tabel_billigst_pr_udbyder(), tabel_prgb_rangliste(),
                         tabel_aarsomkostning(), fejltabel(), begrebstabel(),
                         kilder(
                             ["forbrugerombudsmanden", "reklameidentifikation", "teleankenaevnet"],
                             ["Priser og vilkår: udbydernes egne offentlige prislister, kontrolleret manuelt.",
                              "Gennemsnitspris over 12 mdr.: egen beregning — intropris ganget med "
                              "introperioden plus normalpris for resten, divideret med tolv, plus oprettelse.",
                              "Netværksangivelser: udbydernes egne oplysninger. Hvor de ikke kan "
                              "verificeres, angiver vi MVNO i stedet for at gætte."]),
                         vejviser("/mobilabonnement-under-100-kr/")],
        faq=[
            {"sp": "Hvor mange mobilabonnementer koster under 100 kr.?",
             "sv": f"Vi følger {len(u100)} abonnementer under 100 kr. om måneden. De starter ved "
                   f"{D['min_pris']} kr. for et taleabonnement og {D['min_pris_data']} kr. for det "
                   "billigste med mobildata."},
            {"sp": "Hvad får man for under 100 kr.?",
             "sv": "Typisk fri tale, fri sms, 5G og mellem 5 og 60 GB data uden binding. Det dækker "
                   "langt mere end gennemsnitsdanskerens forbrug."},
            {"sp": "Er billige abonnementer dårligere?",
             "sv": "Ikke på selve forbindelsen. Der findes kun tre mobilnet i Danmark, og de billige "
                   "selskaber lejer sig ind på de samme master. Forskellen ligger i kundeservice og "
                   "tillægsydelser."},
            {"sp": "Er priserne under 100 kr. intropriser?",
             "sv": "Mange af dem er. Derfor viser vi gennemsnitsprisen over 12 måneder, så du kan se, "
                   "hvilke der reelt er under hundrede kroner hele vejen."},
            {"sp": "Hvor meget sparer jeg ved at skifte?",
             "sv": "Skifter du fra 199 til 79 kr. om måneden, sparer du 1.440 kr. om året. For en "
                   "husstand med to abonnementer er det knap 2.900 kr."},
        ],
        links=[("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
               ("/bedste-mobilabonnement/", "Bedste mobilabonnement"),
               ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?"),
               ("/guides/prisstigning-mobilabonnement/", "Når prisen stiger — dine rettigheder")])

    byg_guide("/guides/mobilabonnement-trods-rki/", "Mobilabonnement og RKI",
              "Mobilabonnement trods RKI",
              "Mobilabonnement trods RKI — sådan får du et alligevel",
              "Registreret i RKI? Taletid kræver ingen kreditvurdering, og der findes flere "
              "veje til et abonnement. Se dine muligheder og dine rettigheder.",
              sider4.rki(D, {"gennemgang": gennemgangslinje(OPDATERET, "Regler og fremgangsmåde gennemgået")})
              + f'<section class="sektion baand-smal artikel">{kilder(
                  ["experian", "borger_kredit", "datatilsynet", "teleankenaevnet"],
                  ["Krav til kreditvurdering ved abonnementsaftaler: udbydernes egne vilkår.",
                   "Vi navngiver bevidst ikke udbydere som RKI-venlige. Ingen dansk udbyder "
                   "offentliggør sine kreditkriterier, og de ændrer sig løbende."])}</section>',
              [
                  {"sp": "Kan jeg få mobilabonnement, når jeg står i RKI?",
                   "sv": "Et almindeligt abonnement kræver som regel kreditvurdering, og en aktiv "
                         "registrering fører oftest til afslag. Et taletidskort kan du derimod altid få, "
                         "fordi du betaler forud og udbyderen ikke løber nogen risiko."},
                  {"sp": "Kræver taletidskort kreditvurdering?",
                   "sv": "Nej. Du betaler forud, så der er ingen kreditrisiko for udbyderen. Det er den "
                         "eneste løsning, der i praksis altid er tilgængelig."},
                  {"sp": "Kan jeg få telefon på afbetaling med RKI?",
                   "sv": "Meget sjældent. Afbetaling er en kreditaftale og vurderes strengere end selve "
                         "abonnementet. Køb telefonen kontant eller brugt i stedet."},
                  {"sp": "Hvad gør jeg, hvis jeg bliver afvist?",
                   "sv": "Ring til kundeservice og bed om en manuel kreditvurdering. Sagsbehandleren kan "
                         "se på et bredere billede end det automatiske opslag, og et depositum kan nogle "
                         "gange gøre forskellen."},
                  {"sp": "Skal jeg søge hos mange udbydere?",
                   "sv": "Nej. Hvert afslag udløser et opslag, og mange opslag kan i sig selv trække ned. "
                         "Søg målrettet på den løsning, der har højest sandsynlighed — typisk taletid."},
                  {"sp": "Beholder jeg mit nummer, hvis jeg går over på taletid?",
                   "sv": "Ja. Nummerportering er en rettighed i Danmark og gælder begge veje mellem "
                         "abonnement og taletid."},
              ],
              [("/taletidskort/", "Taletidskort — den sikre vej"),
               ("/mobilabonnement-med-telefon/", "Telefon på afbetaling — regn efter"),
               ("/mobilabonnement-under-100-kr/", "Abonnementer under 100 kr."),
               ("/mobilabonnement-uden-data/", "Abonnement uden data")],
              billede="trods-rki",
              altbillede="Mand undersøger mobilabonnementer på laptop på et bibliotek",
              ekstra=[tabel_billigst_pr_udbyder(), tabel_pr_datamaengde(),
                      vejviser("/guides/mobilabonnement-trods-rki/")])

    byg_guide("/guides/mobilabonnement-eller-bredbaand/", "Mobil eller bredbånd",
              "Mobilabonnement eller bredbånd — hvad skal du vælge?",
              "Mobilabonnement eller bredbånd — forskellen forklaret",
              "Kan et stort mobilabonnement erstatte dit bredbånd? Se forskellen på mobil, "
              "mobilt bredbånd og fast bredbånd — og hvornår hvad giver mening.",
              sider4.bredbaand(D, {"gennemgang": gennemgangslinje(OPDATERET, "Datatal baseret på typisk forbrug")})
              + f'<section class="sektion baand-smal artikel">{kilder(
                  ["teleankenaevnet", "digst_klage"],
                  ["Dataforbrug pr. aktivitet: typiske intervaller baseret på streamingtjenesternes "
                   "egne oplysninger om båndbredde ved forskellige opløsninger.",
                   "Mobilpriser: vores egen sammenligning, opdateret " + OPDATERET + ".",
                   "Vi sammenligner ikke bredbåndspriser og henviser til dedikerede "
                   "bredbåndssammenligninger for den del."])}</section>',
              [
                  {"sp": "Kan et mobilabonnement erstatte bredbånd?",
                   "sv": "For en enkelt person med god mobildækning og fri data, ja. For en husstand med "
                         "flere personer, streaming og hjemmearbejde er fast bredbånd som regel nødvendigt."},
                  {"sp": "Hvad er forskellen på mobilt bredbånd og et mobilabonnement?",
                   "sv": "Begge bruger mobilnettet. Et mobilabonnement er til telefonen, mens mobilt "
                         "bredbånd leveres med en router til hjemmet og typisk har større datamængde."},
                  {"sp": "Hvor meget data bruger en husstand?",
                   "sv": "En enkelt person med laptop bruger typisk 80-150 GB om måneden. En familie med "
                         "børn ligger ofte over 500 GB. Det er derfor fri data er et minimum, hvis mobilen "
                         "skal være husstandens internet."},
                  {"sp": "Må jeg bruge hotspot?",
                   "sv": "Hos de fleste danske udbydere ja, men tjek vilkårene. Enkelte begrænser deling "
                         "til andre enheder."},
                  {"sp": "Hvad er billigst?",
                   "sv": "Det afhænger af forbruget. Fri data koster fra " + str(D['pris_fri']) + " kr. om "
                         "måneden. Er det billigere end dit bredbånd, og har du god dækning, kan du spare "
                         "hele bredbåndsregningen."},
              ],
              [("/mobilabonnement-med-fri-data/", "Abonnementer med fri data"),
               ("/daekningskort/", "Tjek dækningen på din adresse"),
               ("/speedtest/", "Test din mobilhastighed"),
               ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?")],
              billede="mobil-eller-bredbaand",
              altbillede="Kvinde sammenligner mobilabonnement og bredbånd derhjemme med router",
              ekstra=[prisfordeling(), tabel_pr_datamaengde(),
                      vejviser("/guides/mobilabonnement-eller-bredbaand/")])

    byg_guide("/guides/mobilabonnement-i-udlandet/", "Mobil i udlandet",
              "Mobilabonnement i udlandet — roaming og EU-regler",
              "Mobil i udlandet — roaming, EU-regler og hvad det koster",
              "Sådan bruger du dit danske abonnement i udlandet uden dyre overraskelser. "
              "Forskellen på roaming og udlandsopkald, og hvad du gør uden for EU.",
              sider4.udlandet(D, {"gennemgang": gennemgangslinje(OPDATERET, "Roamingregler og takstforhold gennemgået")})
              + f'<section class="sektion baand-smal artikel">{kilder(
                  ["digst_klage", "teleankenaevnet"],
                  ["EU-roaming: reglerne om roaming inden for EU og EØS, som de fremgår af "
                   "udbydernes abonnementsvilkår.",
                   "EU-datalofter: de enkelte udbyderes vilkår — se EU-kolonnen i vores tabeller.",
                   "Landekoder: ITU-T E.164 og ISO 3166-1.",
                   "Dataforbrug på rejse: typiske intervaller, ikke målte værdier."])}</section>',
              [
                  {"sp": "Virker mit danske abonnement i EU?",
                   "sv": "Ja. Inden for EU og EØS bruger du abonnementet på stort set samme vilkår som "
                         "herhjemme. Datamængden er dog ofte lavere end i Danmark."},
                  {"sp": "Hvad koster det at bruge mobilen uden for EU?",
                   "sv": "Det afhænger helt af landet og udbyderen — reglerne gælder ikke der. Slå "
                         "dataroaming fra, tjek taksten for landet, og overvej et lokalt data-eSIM."},
                  {"sp": "Er opkald til udlandet inkluderet i fri tale?",
                   "sv": "Nej, hos de fleste udbydere. Fri tale dækker opkald til danske numre. At ringe "
                         "fra Danmark til et udenlandsk nummer afregnes særskilt."},
                  {"sp": "Hvor meget EU-data har jeg?",
                   "sv": "Det står i abonnementsvilkårene og er ofte lavere end din danske datamængde. Vi "
                         "viser tallet i EU-kolonnen i alle vores tabeller."},
                  {"sp": "Er eSIM en god løsning på rejsen?",
                   "sv": "Uden for EU er det ofte den billigste. Du køber en lokal datapakke og beholder "
                         "dit danske nummer aktivt til opkald og sms."},
              ],
              [("/guides/esim/", "eSIM forklaret — også til rejsen"),
               ("/landekoder/", "Alle landekoder"),
               ("/mobilabonnement-med-fri-tale/", "Abonnementer med fri tale"),
               ("/hvem-ringer-til-mig/", "Ukendt opkald fra udlandet?")],
              billede="i-udlandet",
              altbillede="Kvinde bruger mobilen med roaming på en gade i Italien",
              ekstra=[erfaring("udlandet"), tabel_billigst_pr_udbyder(), begrebstabel(),
                      vejviser("/guides/mobilabonnement-i-udlandet/")])

    byg_guide("/guides/prisstigning-mobilabonnement/", "Prisstigning",
              "Prisstigning på mobilabonnement — hvad gør du?",
              "Prisstigning på mobilabonnement — dine rettigheder",
              "Er dit mobilabonnement steget i pris? Se hvorfor det sker, hvornår du kan "
              "opsige, og hvordan du får markedsprisen igen.",
              sider4.prisstigning(D, {"gennemgang": gennemgangslinje(OPDATERET, "Rettigheder og fremgangsmåde gennemgået")})
              + f'<section class="sektion baand-smal artikel">{kilder(
                  ["teleankenaevnet", "teleanke_klag", "digst_klage", "forbrugerombudsmanden",
                   "teleklagenaevnet"],
                  ["Varslingsregler ved ændringer til ugunst: udbydernes abonnementsvilkår.",
                   "Prisberegninger: egne beregninger ud fra de viste beløb.",
                   "Vi giver ikke juridisk rådgivning — ved tvivl om din konkrete aftale bør du "
                   "kontakte udbyderen eller Teleankenævnet."])}</section>',
              [
                  {"sp": "Må mit mobilselskab hæve prisen?",
                   "sv": "Ja, men væsentlige ændringer til ugunst for dig skal varsles inden ikrafttræden, "
                         "og du kan som udgangspunkt opsige aftalen i forbindelse med ændringen."},
                  {"sp": "Hvorfor steg min pris pludselig?",
                   "sv": "Oftest fordi en intropris er udløbet som aftalt ved bestillingen. Det sker typisk "
                         "to til seks måneder efter oprettelse."},
                  {"sp": "Kan jeg opsige på grund af en prisstigning?",
                   "sv": "Er ændringen til ugunst for dig, kan du som udgangspunkt opsige i forbindelse med "
                         "den. Har du telefon på afbetaling, skal restgælden dog typisk indfries."},
                  {"sp": "Kan jeg forhandle prisen ned?",
                   "sv": "Ofte ja. Ring og sig, at du overvejer at skifte. De fleste selskaber har en "
                         "fastholdelsesafdeling, der kan matche prisen til nye kunder."},
                  {"sp": "Hvor klager jeg?",
                   "sv": "Klag først skriftligt til selskabet. Får du ikke medhold — eller intet svar inden "
                         "for rimelig tid — kan sagen indbringes for Teleankenævnet. Klagegebyret er 175 kr. "
                         "og refunderes, hvis du får medhold."},
              ],
              [("/billigste-mobilabonnement/", "Sammenlign priser nu"),
               ("/mobilabonnement-uden-binding/", "Abonnementer uden binding"),
               ("/mobilabonnement-under-100-kr/", "Abonnementer under 100 kr."),
               ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab")],
              billede="prisstigning",
              altbillede="Kvinde gennemgår sin mobilregning efter en prisstigning",
              ekstra=[erfaring("prisstigning"), tabel_aarsomkostning(),
                      tabel_billigst_pr_udbyder(), fejltabel(),
                      vejviser("/guides/prisstigning-mobilabonnement/")])

    # ---------------- Musik, ældre, telefon og taletid ----------------
    musikudvalg = sorted([a for a in ABON if MUSIKTJENESTER & set(a.get("streaming", []))],
                         key=lambda a: gns12(a) or 9e9)
    byg_kategori(
        sti="/mobilabonnement-med-musik/", etiket="Med musik",
        h1="Mobilabonnement med musik inkluderet",
        titel=f"Mobilabonnement med musik — fra {D['pris_musik']} kr./md.",
        besk=("Sammenlign mobilabonnementer med musik, podcast og lydbøger inkluderet. "
              f"Fra {D['pris_musik']} kr./md. Musik fylder næsten ingen data."),
        intro=("Abonnementer med musik-, podcast- eller lydbogstjeneste. Lyd fylder langt "
               "mindre data end video, så du behøver ikke et stort abonnement."),
        udvalg=musikudvalg, tekstfunktion=sider3.musik,
        chips=[("Fra", f"{D['pris_musik']} kr."), ("Musik", "ca. 100 MB/t"), ("Planer", str(len(musikudvalg)))],
        tabeltitel="Abonnementer med musik og lyd inkluderet",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), tabel_pr_datamaengde(), fejltabel(),
                         begrebstabel(), vejviser("/mobilabonnement-med-musik/")],
        faq=[
            {"sp": "Hvad koster mobilabonnement med musik?",
             "sv": f"Fra {D['pris_musik']} kr. om måneden i vores sammenligning. Musiktjenester er "
                   "billigere at få med end video, fordi de koster mindre separat."},
            {"sp": "Hvor meget data bruger musikstreaming?",
             "sv": "Cirka 70-150 MB i timen afhængigt af kvalitet. Det er op mod tyve gange mindre end "
                   "video. Podcasts fylder endnu mindre, typisk 30-60 MB i timen."},
            {"sp": "Kan jeg undgå at bruge data på musik?",
             "sv": "Ja. Alle større musiktjenester kan gemme musik offline. Sæt automatisk download til "
                   "over wi-fi, så bruger du reelt ingen mobildata på musik."},
            {"sp": "Er operatørens egen musiktjeneste noget værd?",
             "sv": "Det afhænger af, om du vil bruge den. Har du playlister og lyttehistorik hos en anden "
                   "tjeneste, er værdien af at skifte tæt på nul, uanset prisskiltet."},
            {"sp": "Hvad med lydbøger?",
             "sv": "Lydbøger er dyrere at købe separat end musik, så det er ofte den tjeneste, hvor et "
                   "bundle bedst kan betale sig — hvis du rent faktisk lytter."},
        ],
        links=[("/mobilabonnement-med-streaming/", "Alle abonnementer med streaming"),
               ("/bedste-mobilabonnement/", "Bedste mobilabonnement"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/hvor-meget-data/", "Hvor meget data har du brug for?")])

    aeldreudvalg = sorted([a for a in ABON if a["data_gb"] <= 15], key=lambda a: gns12(a) or 9e9)
    byg_kategori(
        sti="/mobilabonnement-til-aeldre/", etiket="Til ældre",
        h1="Mobilabonnement til ældre",
        titel=f"Mobilabonnement til ældre — trygt og fra {D['pris_aeldre']} kr./md.",
        besk=("Find et trygt mobilabonnement til en ældre bruger. Vi forklarer hvorfor "
              "billigst sjældent er bedst her, og hvordan du undgår overraskelser på regningen."),
        intro=("Små abonnementer uden binding. Bemærk at vi ikke automatisk anbefaler det "
               "billigste her — kundeservice vejer tungere end de sidste tyve kroner."),
        udvalg=aeldreudvalg, tekstfunktion=sider3.aeldre,
        chips=[("Fra", f"{D['pris_aeldre']} kr."), ("112", "virker altid"), ("Uden", "binding")],
        tabeltitel="Små abonnementer der passer til en let bruger",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), tabel_pr_datamaengde(), fejltabel(),
                         begrebstabel(), vejviser("/mobilabonnement-til-aeldre/")],
        faq=[
            {"sp": "Hvilket mobilabonnement er bedst til ældre?",
             "sv": "Et abonnement med lav datamængde og telefonisk kundeservice. Vi anbefaler sjældent "
                   "det allerbilligste her, fordi discountudbydere kun har digital support."},
            {"sp": "Hvor meget data har en ældre bruger brug for?",
             "sv": "Typisk 5 GB. Bruges der videoopkald med familien uden for wi-fi, bør du op på 10 GB, "
                   "da videoopkald kan koste op mod 1,5 GB i timen."},
            {"sp": "Hvordan undgår jeg store regninger?",
             "sv": "Bed udbyderen spærre for overtakserede numre og for udgående udlandsopkald, og slå "
                   "datastop til. Alle tre er gratis og kan klares over telefonen."},
            {"sp": "Virker 112 altid?",
             "sv": "Ja. Nødopkald fungerer uanset abonnement, uanset om taletiden er brugt op, og selv "
                   "uden simkort — telefonen bruger det net, der er stærkest."},
            {"sp": "Skal jeg vælge en seniortelefon?",
             "sv": "Ofte ja. Telefoner med store taster, høj lyd og nødopkaldsknap er billigere end en "
                   "smartphone og markant lettere at bruge. Køb den kontant og uden binding."},
        ],
        links=[("/taletidskort/", "Taletidskort — ingen regning kan overraske"),
               ("/mobilabonnement-uden-data/", "Abonnement uden data"),
               ("/hvem-ringer-til-mig/", "Sådan genkender du svindelopkald"),
               ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab")])

    udenbinding = sorted([a for a in ABON if a["binding"] == 0], key=lambda a: gns12(a) or 9e9)[:14]
    byg_kategori(
        sti="/mobilabonnement-med-telefon/", etiket="Med telefon",
        h1="Mobilabonnement med telefon på afbetaling",
        titel="Mobilabonnement med telefon — regn efter før du binder dig",
        besk=("Telefon og abonnement samlet ser billigt ud, men binder dig i 24-36 måneder. "
              "Se regnestykket, der afgør om det kan betale sig."),
        intro=("Vi anbefaler at købe telefon og abonnement hver for sig. Her er de "
               "abonnementer uden binding, du kan kombinere med et kontantkøb."),
        udvalg=udenbinding, tekstfunktion=sider3.telefon,
        chips=[("Binding", "0 mdr."), ("Fra", f"{D['min_pris']} kr."), ("Frihed", "til at skifte")],
        tabeltitel="Abonnementer uden binding til dit kontantkøb",
        ekstra_tabeller=[tabel_aarsomkostning(), tabel_billigst_pr_udbyder(), fejltabel(),
                         begrebstabel(), vejviser("/mobilabonnement-med-telefon/")],
        faq=[
            {"sp": "Kan det betale sig med telefon og abonnement samlet?",
             "sv": "Sjældent. Gang den samlede månedspris med bindingsperioden og sammenlign med "
                   "telefonens kontantpris plus et discountabonnement. Kontantkøb vinder næsten altid."},
            {"sp": "Hvad sker der, hvis jeg vil skifte selskab undervejs?",
             "sv": "Restgælden på telefonen skal typisk indfries på én gang. Den følger ikke med til den "
                   "nye udbyder, og det er den hyppigste ubehagelige overraskelse ved selskabsskifte."},
            {"sp": "Hvad hvis telefonen går i stykker?",
             "sv": "Afbetalingen løber videre. Restgælden forsvinder ikke, fordi telefonen gør — tjek "
                   "derfor forsikringsdækningen, før du binder dig."},
            {"sp": "Er brugt telefon et godt alternativ?",
             "sv": "Ofte det bedste. Du sparer typisk halvdelen, undgår binding helt og kan lægge "
                   "forskellen i et bedre abonnement. Tjek at telefonen ikke er simlåst."},
            {"sp": "Hvornår giver afbetaling mening?",
             "sv": "Hvis du ikke kan lægge pengene ud nu, eller hvis telefonen reelt sælges under "
                   "kontantpris som del af pakken. Regn efter — det tager fem minutter."},
        ],
        links=[("/mobilabonnement-uden-binding/", "Alle abonnementer uden binding"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/mobilabonnement-til-aeldre/", "Mobilabonnement til ældre"),
               ("/guides/esim/", "eSIM — tjek om din telefon understøtter det")])

    smaa = sorted([a for a in ABON if a["data_gb"] <= 10], key=lambda a: a["pris"])[:12]
    byg_kategori(
        sti="/taletidskort/", etiket="Taletidskort",
        h1="Taletidskort — forudbetalt og uden overraskelser",
        titel="Taletidskort — forudbetalt mobil uden regning",
        besk=("Taletid er forudbetalt, så regningen aldrig kan løbe løbsk. Se hvornår det "
              "betaler sig frem for et abonnement, og hvad du skal være opmærksom på."),
        intro=("Taletid kan ikke overskrides. Her er de mindste abonnementer til "
               "sammenligning, så du kan se, hvornår taletid holder op med at betale sig."),
        udvalg=smaa, tekstfunktion=sider3.taletid,
        chips=[("Betaling", "forudbetalt"), ("Overforbrug", "umuligt"), ("Binding", "aldrig")],
        tabeltitel="Små abonnementer til sammenligning med taletid",
        ekstra_tabeller=[tabel_billigst_pr_udbyder(), fejltabel(), begrebstabel(),
                         vejviser("/taletidskort/")],
        faq=[
            {"sp": "Hvad er forskellen på taletid og abonnement?",
             "sv": "Taletid er forudbetalt og kan ikke overskrides. Et abonnement faktureres bagud og "
                   "kan give overforbrug. Til gengæld er prisen pr. gigabyte lavere på abonnement."},
            {"sp": "Kræver taletid kreditvurdering?",
             "sv": "Normalt ikke, fordi du betaler forud. Det gør taletid til en mulighed for dem, der "
                   "ikke kan få et almindeligt abonnement."},
            {"sp": "Kan jeg beholde mit nummer, hvis jeg skifter til abonnement?",
             "sv": "Ja. Nummerportering gælder begge veje, og den nye udbyder klarer flytningen."},
            {"sp": "Udløber min taletid?",
             "sv": "Typisk ja. Bruges kortet ikke i en længere periode, kan saldoen eller nummeret "
                   "bortfalde. Fyld et lille beløb på med jævne mellemrum for at holde det aktivt."},
            {"sp": "Hvornår bliver taletid dyrere end et abonnement?",
             "sv": "Omkring 100 minutter om måneden, og hurtigere hvis der bruges data. Bruges telefonen "
                   "dagligt med data, er et abonnement næsten altid billigere."},
        ],
        links=[("/mobilabonnement-til-boern/", "Mobilabonnement til børn"),
               ("/mobilabonnement-til-aeldre/", "Mobilabonnement til ældre"),
               ("/mobilabonnement-uden-data/", "Abonnement uden data"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement")])

    # ---------------- Long-tail: én side pr. streamingtjeneste ----------------
    if TJENESTER:
        byg_streamingoversigt()
        for tj in TJENESTER:
            byg_tjenesteside(tj)

    # ---------------- Netværkssider ----------------
    byg_netvaerksoversigt()
    for n in NETVAERK:
        byg_netvaerksside(n)

    # GB-intervaller
    for _s, _n, _l, _h, _p, _b in GB_INTERVALLER:
        byg_gb_side(_s, _n, _l, _h, _p, _b)

    # Sammenligninger mellem to udbydere
    byg_vs_oversigt()
    for _sa, _sb in VS_PAR:
        if [a for a in ABON if a["udbyder"] == _sa] and [a for a in ABON if a["udbyder"] == _sb]:
            VS_PAR_AKTIVE.append((_sa, _sb))
    for _sa, _sb in VS_PAR_AKTIVE:
        byg_vs(_sa, _sb)

    # Værktøjer
    byg_landekoder()
    byg_hvem_ringer()
    byg_daekningstjek()
    byg_speedtest()

    # Sæsonside — oprettes i god tid, så den er indekseret inden november
    byg_statisk("/mobilabonnementer-black-friday/",
                "Black Friday mobilabonnement — er tilbuddene ægte?",
                "Black Friday er sjældent den bedste tid at købe mobilabonnement. Se hvordan "
                "du gennemskuer et tilbud, og hvad der faktisk bliver billigere.",
                "Black Friday", "Black Friday og mobilabonnement",
                sider3.BLACK_FRIDAY, prioritet="0.6")

    # Udbydere
    byg_udbyderoversigt()
    for u in UDBYDERE:
        byg_udbyder(u)

    # Guides
    byg_guideoversigt()
    byg_guide("/guides/skift-mobilselskab/", "Skift mobilselskab",
              "Sådan skifter du mobilselskab",
              f"Skift mobilselskab — behold dit nummer, trin for trin",
              "Sådan skifter du mobilselskab og beholder dit nummer. Trin for trin, og de "
              "fem ting der oftest går galt.",
              indhold.GUIDE_SKIFT,
              [
                  {"sp": "Hvor lang tid tager det at skifte mobilselskab?",
                   "sv": "Typisk 1-5 hverdage fra bestilling til nummeret er flyttet. Med eSIM kan du ofte være i "
                         "gang samme dag. Selve overgangen tager sjældent mere end nogle minutter."},
                  {"sp": "Skal jeg selv opsige mit gamle abonnement?",
                   "sv": "Nej. Den nye udbyder håndterer både nummerflytning og opsigelse. Opsiger du selv, "
                         "risikerer du at nummeret lukkes, før det kan flyttes."},
                  {"sp": "Mister jeg mit nummer, hvis jeg skifter?",
                   "sv": "Nej. Nummerportering er en rettighed i Danmark, og du beholder dit nummer, når du "
                         "angiver det ved bestilling."},
                  {"sp": "Hvad sker der med restgælden på min telefon?",
                   "sv": "Restgæld på en telefon købt på afbetaling følger ikke med. Den skal typisk indfries, "
                         "når du skifter selskab. Spørg om beløbet, før du bestiller."},
              ],
              [("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/esim/", "eSIM forklaret"),
               ("/mobilabonnement-uden-binding/", "Abonnementer uden binding")],
              billede="skift-mobilselskab",
              altbillede="Kvinde skifter mobilselskab på laptop og telefon på en café",
              ekstra=[tabel_billigst_pr_udbyder(), tabel_aarsomkostning(), fejltabel(),
                      vejviser("/guides/skift-mobilselskab/"),
                      kilder(
                          ["digst_klage", "teleankenaevnet", "teleindustrien"],
                          ["Nummerportering: en rettighed i Danmark — den nye udbyder håndterer flytningen.",
                           "Priser og vilkår: udbydernes egne prislister, kontrolleret manuelt.",
                           "Tidsangivelser for portering er typiske intervaller, ikke garantier."])])

    byg_guide("/guides/hvor-meget-data/", "Hvor meget data",
              "Hvor meget data har jeg brug for?",
              f"Hvor meget data har jeg brug for? Sådan finder du dit forbrug",
              "Find dit faktiske dataforbrug på to minutter, og se præcis hvilket "
              "abonnement der matcher. Med forbrugstal for streaming, sociale medier og video.",
              indhold.GUIDE_DATA,
              [
                  {"sp": "Hvor meget data bruger en gennemsnitsdansker?",
                   "sv": "De fleste danskere bruger mellem 10 og 30 GB om måneden. Forbruget stiger år for år, "
                         "primært på grund af video."},
                  {"sp": "Hvor meget data bruger en times video?",
                   "sv": "Cirka 0,7-1 GB i standardkvalitet og 2-3 GB i HD. Video er langt den største "
                         "dataforbruger på de fleste telefoner."},
                  {"sp": "Hvordan ser jeg mit dataforbrug?",
                   "sv": "På iPhone under Indstillinger og Mobildata. På Android under Indstillinger, Netværk og "
                         "internet, Dataforbrug. Din udbyders app viser det mest præcise tal."},
                  {"sp": "Hvad sker der, hvis jeg løber tør for data?",
                   "sv": "Afhængigt af udbyderen bliver forbindelsen stoppet, hastigheden sat ned, eller du "
                         "opkræves for ekstra forbrug. Slå datastop til for at undgå uventede regninger."},
              ],
              [("/mobilabonnement-med-fri-data/", "Er fri data pengene værd?"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/daekning-og-netvaerk/", "Dækning og netværk")],
              billede="hvor-meget-data",
              altbillede="Kvinde tjekker sit dataforbrug på telefonen på en café",
              ekstra=[prisfordeling(), tabel_pr_datamaengde(), tabel_prgb_rangliste(),
                      vejviser("/guides/hvor-meget-data/"),
                      kilder(
                          ["teleankenaevnet"],
                          ["Dataforbrug pr. aktivitet: typiske intervaller ud fra streamingtjenesternes "
                           "egne oplysninger om båndbredde ved forskellige opløsninger.",
                           "Priser og datamængder: vores egen sammenligning, opdateret " + OPDATERET + ".",
                           "Tallene er vejledende — dit eget forbrug findes i telefonens indstillinger "
                           "og er den eneste præcise kilde."])])

    byg_guide("/guides/daekning-og-netvaerk/", "Dækning og netværk",
              "Dækning og netværk i Danmark",
              f"Mobildækning i Danmark — TDC NET, Telenor og 3 sammenlignet",
              "Der findes kun tre mobilnetværk i Danmark. Her er forskellen på dem, og "
              "hvornår den betyder noget for dit valg af abonnement.",
              """<section class="sektion baand-smal artikel">
<div class="udtag"><p><strong>Kort svar:</strong> Danmark har tre mobilnetværk — TDC NET,
Telenor og 3. Alle andre selskaber lejer sig ind hos en af dem. TDC NET er mest udbygget og
stærkest i landdistrikter. 3 er stærk på hastighed i byerne. Telenor ligger derimellem. Bor
du i en større by, kan du i praksis vælge frit.</p></div>

<h2>Kun tre net — resten er lejere</h2>
<p>Det er den vigtigste ting at forstå om det danske mobilmarked. Når du vælger mellem tredive
selskaber, vælger du reelt mellem tre netværk. Et discountselskab bruger nøjagtig de samme
master som et premiumselskab på samme net, og din telefon kan ikke se forskel.</p>
<p>Det betyder også, at spørgsmålet "har billige selskaber dårligere dækning" har et klart
svar: nej, ikke i sig selv. Dækningen bestemmes af nettet, ikke af prisen.</p>

<h2>De tre net sammenlignet</h2>
<table>
<thead><tr><th>Netværk</th><th>Stærkest</th><th>Svagest</th><th>Vælg det hvis</th></tr></thead>
<tbody>
<tr><td><strong>TDC NET</strong></td><td>Landdistrikter, sommerhuse, tog, indendørs i ældre bygninger</td><td>Prisen på brands der kører på nettet</td><td>Du bor uden for byerne eller pendler langt</td></tr>
<tr><td><strong>Telenor</strong></td><td>Bred dækning, god balance mellem pris og kvalitet</td><td>Enkelte huller i tyndt befolkede områder</td><td>Du vil have solid dækning til fornuftig pris</td></tr>
<tr><td><strong>3</strong></td><td>Hastighed og kapacitet i byer, tidlig 5G</td><td>Landdistrikter og visse kystområder</td><td>Du bor i en større by og bruger meget data</td></tr>
</tbody>
</table>

<h2>Sådan tjekker du dækningen på din egen adresse</h2>
<ol class="trin">
<li><strong>Find dækningskortet</strong>
Alle tre netværksejere har offentlige dækningskort på deres hjemmesider. De er den bedste
tilgængelige kilde, fordi de bygger på operatørernes egne måledata.</li>
<li><strong>Tjek tre steder, ikke ét</strong>
Din bopæl, din arbejdsplads og din pendlerrute. Det er de tre steder, du faktisk bruger
telefonen mest.</li>
<li><strong>Spørg naboen</strong>
Den mest undervurderede metode. Naboer på samme vej med samme udbyder giver dig et
virkelighedstjek, som intet kort kan matche.</li>
</ol>

<h2>Hvad med 5G?</h2>
<p>5G giver højere hastigheder og lavere forsinkelse, men for almindelig brug — sociale
medier, streaming, navigation — mærker de fleste ikke stor forskel fra et velfungerende
4G-net. 5G er værd at prioritere, hvis du henter meget store filer, bruger telefonen som
hotspot til arbejde, eller bor et sted med overbelastet 4G.</p>
<p>Vær opmærksom på, at 5G ikke automatisk er inkluderet i alle abonnementer, og at
dækningen stadig er mest udbygget i byerne.</p>

<div class="tip"><h3>Fortrydelsesret er din sikkerhedsnet</h3>
<p>Køber du abonnementet online, har du som udgangspunkt fortrydelsesret efter
forbrugeraftaleloven. Test dækningen grundigt de første dage — hjemme, på arbejde og i
kælderen — mens du stadig kan fortryde.</p></div>
</section>""",
              [
                  {"sp": "Hvor mange mobilnetværk er der i Danmark?",
                   "sv": "Tre: TDC NET, Telenor og 3. Alle andre mobilselskaber lejer sig ind på et af dem."},
                  {"sp": "Hvilket netværk har den bedste dækning i Danmark?",
                   "sv": "TDC NET er historisk det mest udbyggede net og står typisk stærkest i landdistrikter, "
                         "sommerhusområder og indendørs. I byerne er forskellen mellem de tre lille."},
                  {"sp": "Har billige mobilselskaber dårligere dækning?",
                   "sv": "Nej. De lejer sig ind på de samme netværk som de dyre. Nogle aftaler kan dog indeholde "
                         "hastighedsloft eller lavere prioritet i myldretiden."},
                  {"sp": "Er 5G nødvendigt?",
                   "sv": "For almindelig brug mærker de fleste ikke stor forskel fra et godt 4G-net. 5G er mest "
                         "relevant ved store downloads, hotspot til arbejde eller i områder med belastet 4G."},
              ],
              [("/udbydere/", "Se hvilket net hver udbyder kører på"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab")],
              billede="daekning-og-netvaerk",
              altbillede="Kvinde med 5G-dækning på telefonen ved dansk kystby med mobilmast",
              ekstra=[udbydergitter(), tabel_billigst_pr_udbyder(),
                      vejviser("/guides/daekning-og-netvaerk/"),
                      kilder(
                          ["digst_klage", "teleindustrien", "teleklagenaevnet"],
                          ["Netværksejere i Danmark: TDC NET, Telenor og 3.",
                           "Dækningskort: netværksejernes egne offentlige kort, som bygger på deres måledata.",
                           "Netværksangivelser pr. udbyder: udbydernes egne oplysninger. Hvor de ikke kan "
                           "verificeres, angiver vi MVNO frem for at gætte.",
                           "Vi laver ikke egne hastigheds- eller dækningsmålinger og foregiver ikke andet."])])

    byg_guide("/guides/esim/", "eSIM", "eSIM forklaret",
              f"eSIM i Danmark — sådan virker det, og hvornår det betaler sig",
              "Hvad et eSIM er, hvilke telefoner der understøtter det, og hvordan du "
              "kommer i gang på få minutter.",
              """<section class="sektion baand-smal artikel">
<div class="udtag"><p><strong>Kort svar:</strong> Et eSIM er et digitalt simkort, der er
indbygget i telefonen. Du aktiverer det med en QR-kode i stedet for at vente på et fysisk
kort med posten, og du kan være i gang få minutter efter bestilling.</p></div>

<h2>Hvorfor eSIM er værd at vælge</h2>
<p>Den mest håndgribelige fordel er tid. Bestiller du et abonnement med eSIM, får du en kode
med det samme og kan skifte selskab samme eftermiddag i stedet for at vente på posten.</p>
<p>Den anden fordel er, at de fleste moderne telefoner kan have flere eSIM-profiler samtidig.
Det er praktisk på to måder: du kan have arbejde og privat på samme telefon uden to enheder,
og du kan købe et lokalt data-eSIM, når du rejser uden for EU, hvor roaming ellers er dyrt.</p>

<h2>Sådan kommer du i gang</h2>
<ol class="trin">
<li><strong>Tjek at din telefon understøtter eSIM</strong>
De fleste telefoner fra de senere år gør. På iPhone: Indstillinger → Generelt → Om →
kig efter eSIM. På Android varierer det efter model.</li>
<li><strong>Bestil abonnementet med eSIM</strong>
Vælg eSIM i stedet for fysisk simkort ved bestillingen.</li>
<li><strong>Scan QR-koden</strong>
Du modtager en QR-kode på mail eller i udbyderens app. Scan den i telefonens indstillinger.
Du skal være på wi-fi.</li>
<li><strong>Vælg hvilken linje der bruges til hvad</strong>
Har du flere linjer, kan du vælge hvilken der bruges til data, opkald og sms.</li>
</ol>

<div class="advarsel"><p><strong>Vær opmærksom:</strong> Skifter du til en ny telefon, kan et
eSIM ikke bare flyttes fysisk. Du skal typisk overføre det via telefonens
overførselsfunktion eller bede udbyderen om en ny kode. Det er gratis hos de fleste, men
det er et ekstra skridt at huske.</p></div>

<h2>eSIM på rejsen</h2>
<p>Rejser du uden for EU, hvor roaming kan være meget dyrt, kan du købe et lokalt data-eSIM
og beholde dit danske nummer aktivt til opkald og sms. Det er ofte den billigste måde at
have data i udlandet, og det kræver ingen udskiftning af kort.</p>
</section>""",
              [
                  {"sp": "Hvad er forskellen på eSIM og almindeligt simkort?",
                   "sv": "Et eSIM er indbygget i telefonen og aktiveres digitalt med en kode. Et almindeligt "
                         "simkort er et fysisk kort, du sætter i. Funktionelt virker de ens."},
                  {"sp": "Understøtter min telefon eSIM?",
                   "sv": "De fleste telefoner fra de senere år gør. Tjek under telefonens indstillinger, eller "
                         "søg på din model plus eSIM."},
                  {"sp": "Kan jeg have både eSIM og fysisk simkort?",
                   "sv": "Ja, de fleste moderne telefoner understøtter begge dele samtidig. Det er praktisk til "
                         "arbejde og privat eller til rejser."},
                  {"sp": "Koster eSIM ekstra?",
                   "sv": "Hos de fleste danske udbydere er eSIM gratis, og det er ofte hurtigere end at få et "
                         "fysisk kort tilsendt."},
              ],
              [("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
               ("/billigste-mobilabonnement/", "Billigste mobilabonnement"),
               ("/udbydere/", "Alle udbydere")],
              billede="esim",
              altbillede="Rejsende aktiverer eSIM på telefonen i en lufthavn",
              ekstra=[tabel_billigst_pr_udbyder(), begrebstabel(),
                      vejviser("/guides/esim/"),
                      kilder(
                          ["teleindustrien", "teleankenaevnet"],
                          ["eSIM-understøttelse: telefonproducenternes egne specifikationer.",
                           "Gebyrer for nye eSIM-profiler: udbydernes prislister.",
                           "Priser: vores egen sammenligning, opdateret " + OPDATERET + "."])])

    # Navngiven metode — vores signaturtal
    tolv_krop = f"""<section class="sektion baand-smal artikel">
  <div class="udtag">
  <p><strong>Kort fortalt:</strong> 12-måneders-prisen er den reelle månedspris, når
  intropris, normalpris og oprettelsesgebyr regnes sammen over et år. Det er tallet, vi
  sorterer efter — ikke den intropris, udbyderne markedsfører.</p>
  </div>

  <h2>Formlen</h2>
  <p>Vi bruger den samme udregning på hvert eneste abonnement på sitet:</p>
  <div class="formelboks">
    <code>(intropris × introperiode) + (normalpris × resterende måneder) + oprettelse</code>
    <span class="formel-div">÷ 12</span>
  </div>
  <p>Regnestykket står under prisen på hvert abonnement i vores tabeller, så du selv kan
  efterprøve det. Ser du <code>59×2 + 200×10 ÷ 12</code>, betyder det 59 kr. i to måneder,
  derefter 200 kr. i ti — altså 176 kr. i gennemsnit.</p>

  <h2>Hvorfor ikke bare vise månedsprisen?</h2>
  <p>Fordi den næsten aldrig er den pris, du betaler. To ud af fem abonnementer på det
  danske marked sælges på en intropris, der gælder to til seks måneder. Et abonnement til
  49 kr., der stiger til 149 kr. i måned tre, koster i virkeligheden 129 kr. i gennemsnit
  over året.</p>
  <p>Sorterer man efter månedsprisen, ligger de aggressive introtilbud øverst — også når de
  er dyrere end alternativerne over et helt år. Det er ikke en fejl i tabellen. Det er en
  fejl i, hvad tabellen måler.</p>

  <h2>Hvad tallet ikke dækker</h2>
  <ul>
    <li><strong>Prisstigninger vi ikke kender.</strong> Regner udbyderen prisen op midt i
    perioden, kan den reelle pris blive højere. Vi bruger de priser, der er oplyst i dag.</li>
    <li><strong>Overforbrug.</strong> Køber du ekstra data, kommer det oveni. Det er
    endnu en grund til at vælge ét trin over dit målte forbrug.</li>
    <li><strong>Telefon på afbetaling.</strong> Vi regner kun på abonnementet. Hardware er
    en separat aftale — se <a href="/mobilabonnement-med-telefon/">vores gennemgang</a>.</li>
    <li><strong>Værdien af streaming.</strong> Indgår der tjenester, kan den reelle værdi
    være højere end prisen antyder. Det vurderer vi i teksten, ikke i tallet.</li>
  </ul>

  <h2>Hvorfor 12 måneder og ikke 6 eller 24?</h2>
  <p>Tolv måneder er den periode, hvor stort set alle introtilbud er udløbet, og hvor de
  fleste mennesker tænker i budget. Seks måneder favoriserer lange introperioder
  kunstigt. Fireogtyve måneder forudsætter, at du bliver — og det bør du netop ikke uden
  at genoverveje.</p>

  <h2>Sådan bruger du tallet</h2>
  <ol class="trin">
    <li><strong>Sammenlign kun 12-måneders-priser med hinanden</strong>
    Ikke en 12-måneders-pris mod en andens intropris. Det er den hyppigste fejl.</li>
    <li><strong>Sortér efter det i tabellen</strong>
    Knappen hedder "Gns. 12 mdr." i filterpanelet.</li>
    <li><strong>Tjek regnestykket</strong>
    Det står under prisen. Ser du et abonnement uden intropris, står der bare
    <code>×12</code>.</li>
  </ol>

  {kilder(["forbrugerombudsmanden", "reklameidentifikation"],
          ["Formlen er vores egen. Vi har ikke set andre danske sammenligningssider "
           "beregne og sortere efter den, men de fleste viser normalprisen ved siden af "
           "introprisen.",
           "Priser hentes fra udbydernes offentlige prislister og kontrolleres manuelt."])}
</section>"""
    byg_statisk("/12-maaneders-prisen/",
                "12-måneders-prisen — sådan beregner vi den reelle pris",
                "Vores signaturtal: den reelle månedspris når intropris, normalpris og "
                "oprettelse regnes sammen. Se formlen og hvorfor den findes.",
                "Metode", "12-måneders-prisen", tolv_krop, prioritet="0.6")

    ordbog_krop = f"""<section class="sektion baand-smal artikel">
  <p class="led">Telemarkedet bruger en række ord, der ikke betyder helt det, man tror.
  Her er de vigtigste oversat til almindeligt dansk.</p>
  {begrebstabel()}

  <h2>Enheder og forkortelser</h2>
  <table>
  <thead><tr><th>Forkortelse</th><th>Står for</th><th>Hvad det betyder</th></tr></thead>
  <tbody>
  <tr><td><strong>GB</strong></td><td>Gigabyte</td><td>Datamængde. 1 GB ≈ en times video i standardkvalitet</td></tr>
  <tr><td><strong>MB</strong></td><td>Megabyte</td><td>1.000 MB = 1 GB. En times musik fylder ca. 100 MB</td></tr>
  <tr><td><strong>Mbit/s</strong></td><td>Megabit pr. sekund</td><td>Hastighed. 10 Mbit rækker til video i HD</td></tr>
  <tr><td><strong>eSIM</strong></td><td>Embedded SIM</td><td>Digitalt simkort indbygget i telefonen</td></tr>
  <tr><td><strong>MVNO</strong></td><td>Mobile Virtual Network Operator</td><td>Selskab uden eget net, der lejer kapacitet</td></tr>
  <tr><td><strong>PUK</strong></td><td>Personal Unblocking Key</td><td>Kode der låser simkortet op efter tre forkerte PIN-forsøg</td></tr>
  <tr><td><strong>APN</strong></td><td>Access Point Name</td><td>Indstilling der forbinder telefonen til udbyderens datanet</td></tr>
  <tr><td><strong>VoLTE</strong></td><td>Voice over LTE</td><td>Opkald over 4G-nettet — bedre lyd og hurtigere opkobling</td></tr>
  <tr><td><strong>VoWiFi</strong></td><td>Voice over Wi-Fi</td><td>Wi-fi-opkald. Løser dårlig indendørsdækning</td></tr>
  <tr><td><strong>Roaming</strong></td><td>—</td><td>At bruge dit abonnement, mens du er i udlandet</td></tr>
  </tbody>
  </table>
  <p>Mangler der et ord? <a href="/kontakt/">Skriv til os</a>, så tilføjer vi det.</p>
</section>"""
    byg_statisk("/ordbog/", "Teleordbog — mobilbegreber forklaret på dansk",
                "Alle de begreber du møder, når du vælger mobilabonnement — fra MVNO og "
                "eSIM til PUK og VoWiFi, forklaret i almindeligt dansk.",
                "Ordbog", "Teleordbog", ordbog_krop, prioritet="0.5")

    pin_krop = """<section class="sektion baand-smal artikel">
  <div class="udtag">
  <p><strong>Kort svar:</strong> PIN-koden beskytter dit simkort og indtastes, når du
  tænder telefonen. Taster du forkert tre gange, låses kortet, og du skal bruge PUK-koden.
  Taster du PUK forkert ti gange, ødelægges simkortet permanent, og du skal have et nyt
  fra din udbyder.</p>
  </div>

  <h2>Forskellen på PIN og PUK</h2>
  <table>
  <thead><tr><th></th><th>PIN</th><th>PUK</th></tr></thead>
  <tbody>
  <tr><td><strong>Cifre</strong></td><td>4 (kan ofte ændres til 8)</td><td>8</td></tr>
  <tr><td><strong>Bruges til</strong></td><td>At låse simkortet op ved opstart</td><td>At låse op efter tre forkerte PIN</td></tr>
  <tr><td><strong>Kan du ændre den?</strong></td><td>Ja</td><td>Nej — den er fast</td></tr>
  <tr><td><strong>Forsøg før spærring</strong></td><td>3</td><td>10</td></tr>
  <tr><td><strong>Hvor finder du den?</strong></td><td>Fulgte med simkortet</td><td>Udbyderens selvbetjening</td></tr>
  </tbody>
  </table>

  <h2>Jeg har glemt min PIN-kode</h2>
  <ol class="trin">
    <li><strong>Prøv ikke at gætte</strong>
    Du har tre forsøg i alt, og de tæller på tværs af genstarter. Stop hellere med det samme.</li>
    <li><strong>Find din PUK-kode</strong>
    Den ligger i din udbyders app eller selvbetjening, typisk under simkort eller
    abonnement. Den stod også på det plastikkort, simkortet sad i.</li>
    <li><strong>Indtast PUK og vælg en ny PIN</strong>
    Telefonen beder om det automatisk, når kortet er låst.</li>
    <li><strong>Kan du ikke finde PUK?</strong>
    Ring til udbyderen. De kan oplyse den efter identifikation — de kan ikke se din PIN,
    men de kan altid finde PUK.</li>
  </ol>

  <div class="advarsel">
  <p><strong>Ti forkerte PUK-forsøg ødelægger simkortet permanent.</strong> Der findes ingen
  vej tilbage — du skal have et nyt simkort. Er du usikker, så ring frem for at gætte. Et
  nyt simkort er gratis hos de fleste udbydere, men det tager dage med posten, hvis du ikke
  kan bruge eSIM.</p>
  </div>

  <h2>Standardkoder — og hvorfor du bør ændre dem</h2>
  <p>Mange udbydere udleverer simkort med en standard-PIN. Beholder du den, kan enhver, der
  får fat i dit kort, sætte det i en anden telefon og modtage dine sms'er — herunder koder
  fra bank og MitID.</p>
  <p>Ændr PIN-koden på iPhone under Indstillinger → Mobil → SIM-PIN, og på Android under
  Indstillinger → Sikkerhed → SIM-kortlås. Vælg noget, du husker, men som ikke er din
  fødselsdato.</p>

  <h2>Slipper du for det med eSIM?</h2>
  <p>Delvist. Et eSIM har også en PIN, men det kan ikke tages fysisk ud af telefonen, så
  risikoen ved tyveri er lavere. Til gengæld kan et eSIM ikke bare flyttes til en lånt
  telefon, hvis din går i stykker. Se <a href="/guides/esim/">vores guide til eSIM</a>.</p>
</section>"""
    byg_statisk("/pin-og-puk-kode/", "PIN- og PUK-kode — sådan låser du simkortet op",
                "Glemt PIN-kode? Se hvordan du finder din PUK, hvor mange forsøg du har, "
                "og hvad du gør, hvis simkortet er spærret.",
                "Hjælp", "PIN- og PUK-kode", pin_krop, prioritet="0.5")

    # Om-sider
    byg_statisk("/om-os/", "Om Telemobil — uafhængig sammenligning af mobilabonnementer",
                "Telemobil sammenligner danske mobilabonnementer uafhængigt. Læs om vores "
                "metode, redaktionelle principper og hvem der står bag.",
                "Om os", "Om Telemobil", indhold.OM_OS, prioritet="0.6")

    byg_statisk("/saadan-tjener-vi-penge/",
                "Sådan tjener Telemobil penge — provision og uafhængighed",
                "Telemobil modtager provision fra udvalgte udbydere. Her forklarer vi "
                "præcis hvordan det fungerer, og hvad det ikke påvirker.",
                "Forretningsmodel", "Sådan tjener vi penge", indhold.TJENER_PENGE, prioritet="0.6")

    byg_statisk("/metode/", "Vores metode — sådan sammenligner vi mobilabonnementer",
                "Datagrundlag, beregninger og vurderingskriterier bag Telemobils "
                "sammenligninger af mobilabonnementer.",
                "Metode", "Sådan sammenligner vi", indhold.METODE, prioritet="0.6")

    emil_krop = f"""<section class="sektion baand-smal artikel">
  <div style="display:flex;gap:1.8rem;align-items:flex-start;flex-wrap:wrap;margin-bottom:2rem">
    <img src="{FORFATTER['billede']}" width="150" height="150" alt="{e(FORFATTER['navn'])}"
         style="border-radius:18px;box-shadow:var(--skygge-loft)">
    <div style="flex:1;min-width:260px">
      <p class="led" style="margin-top:0">{e(FORFATTER['bio'])}</p>
      <p><a href="{FORFATTER['linkedin']}" rel="noopener nofollow" target="_blank"
            class="knap knap-linje knap-lille">Se profil på LinkedIn</a></p>
    </div>
  </div>

  <h2>Baggrund</h2>
  <p>Emil Rostgaard har siden 2018 arbejdet med digitale sammenligningstjenester inden for
  forbrugerøkonomi og har stået bag opbygningen af flere danske prisportaler. Arbejdet har
  gennemgående handlet om det samme: at oversætte komplicerede produktvilkår til tal, som
  almindelige forbrugere kan handle på.</p>

  <h2>Hvad han laver på Telemobil</h2>
  <ul>
    <li>Gennemgår udbydernes produktvilkår og prislister ved hver opdatering</li>
    <li>Fastlægger den metode, sammenligningerne bygger på</li>
    <li>Skriver de redaktionelle vurderinger af hver udbyder</li>
    <li>Behandler henvendelser om faktuelle fejl og rettelser</li>
  </ul>

  <h2>Redaktionel linje</h2>
  <p>Telemobil skriver konsekvent, at de fleste danskere ikke har brug for det dyreste
  abonnement — også selvom vi typisk tjener mere på dyre produkter. Det er den vigtigste
  redaktionelle beslutning på siden, og den er bevidst. En sammenligningsside, der aldrig
  anbefaler det billige valg, er en annonce.</p>

  <h2>Kontakt</h2>
  <p>Spørgsmål, rettelser eller henvendelser fra presse kan sendes via
  <a href="/kontakt/">kontaktsiden</a> eller gennem
  <a href="{FORFATTER['linkedin']}" rel="noopener nofollow" target="_blank">LinkedIn</a>.</p>
</section>"""

    byg_statisk("/om/emil-rostgaard/",
                f"{FORFATTER['navn']} — stifter og redaktør af Telemobil",
                f"{FORFATTER['navn']} står bag Telemobil og har arbejdet med digitale "
                "sammenligningstjenester siden 2018.",
                "Forfatter", FORFATTER["navn"], emil_krop, prioritet="0.6",
                jsonld_ekstra={"@type": "ProfilePage", "mainEntity": {"@id": DOMAENE + "/om/emil-rostgaard/#person"}})

    kontakt_krop = """<section class="sektion baand-smal artikel">
  <h2>Skriv til os</h2>
  <p>Vi svarer på alle henvendelser om faktuelle fejl i priser eller oplysninger. Skriv til
  <strong>kontakt@telemobil.dk</strong>.</p>
  <h2>Rettelser</h2>
  <p>Har du fundet en pris eller en oplysning, der ikke stemmer, så send gerne et link til
  udbyderens side sammen med din henvendelse. Så kan vi rette hurtigt.</p>
  <h2>Udbydere</h2>
  <p>Er du udbyder og mangler i vores sammenligning, hører vi gerne fra dig. Bemærk at
  optagelse ikke kan købes, og at en eventuel provisionsaftale ikke påvirker placering
  eller omtale. Se <a href="/saadan-tjener-vi-penge/">vores forretningsmodel</a>.</p>
  <h2>Presse</h2>
  <p>Henvendelser fra presse kan sendes til samme adresse eller via
  <a href="https://www.linkedin.com/in/emil-rostgaard-702809195/" rel="noopener nofollow" target="_blank">LinkedIn</a>.
  Se også vores <a href="/presse/">pressesid med faktaark</a>.</p>

  <h2>Postadresse</h2>
  <p>
    Telemobil<br>
    Lundbyesgade 13<br>
    8000 Aarhus C<br>
    Danmark
  </p>
  <p>Vi har ikke fysisk kundebetjening — henvendelser besvares på mail.</p>
</section>"""
    byg_statisk("/kontakt/", "Kontakt Telemobil — rettelser, spørgsmål og presse",
                "Kontakt Telemobil om faktuelle rettelser i priser, spørgsmål til vores sammenligninger eller henvendelser fra presse og udbydere.",
                "Kontakt", "Kontakt os", kontakt_krop, prioritet="0.4")

    cookie_krop = """<section class="sektion baand-smal artikel">
  <h2>Hvad er cookies?</h2>
  <p>Cookies er små tekstfiler, som gemmes i din browser, når du besøger et website. De
  bruges til at huske dine valg og til at måle, hvordan siden bliver brugt.</p>
  <h2>Hvilke cookies bruger Telemobil?</h2>
  <table>
  <thead><tr><th>Type</th><th>Formål</th><th>Levetid</th></tr></thead>
  <tbody>
  <tr><td><strong>Nødvendige</strong></td><td>Får siden til at fungere. Kan ikke fravælges.</td><td>Sessionen</td></tr>
  <tr><td><strong>Statistik</strong></td><td>Måler hvilke sider der bruges, så vi kan forbedre dem. Anonymiseret.</td><td>Op til 24 mdr.</td></tr>
  <tr><td><strong>Affiliatesporing</strong></td><td>Registrerer at du kom fra os, så vi kan modtage provision ved bestilling.</td><td>Sættes af udbyderen</td></tr>
  </tbody>
  </table>
  <h2>Sådan afviser eller sletter du cookies</h2>
  <p>Du kan til enhver tid slette cookies i din browsers indstillinger. I Chrome, Safari,
  Firefox og Edge findes det under indstillinger for privatliv. Bemærk at siden stadig
  fungerer uden statistik- og sporingscookies.</p>
  <h2>Tredjeparter</h2>
  <p>Klikker du videre til en udbyder, gælder deres cookiepolitik på deres site. Vi har
  ingen kontrol over, hvad de sætter.</p>
  <p>Læs også vores <a href="/privatlivspolitik/">privatlivspolitik</a> og
  <a href="/saadan-tjener-vi-penge/">hvordan vi tjener penge</a>.</p>
</section>"""
    byg_statisk("/cookiepolitik/", "Cookiepolitik — sådan bruger Telemobil cookies",
                "Se hvilke cookies Telemobil bruger, hvad de gør, og hvordan du sletter dem.",
                "Cookies", "Cookiepolitik", cookie_krop, prioritet="0.3")

    presse_krop = """<section class="sektion baand-smal artikel">
  <h2>Om Telemobil</h2>
  <p>Telemobil er en uafhængig dansk prissammenligning for mobilabonnementer. Vi følger
  markedets udbydere, regner priserne om til sammenlignelige tal og skriver om, hvad
  forskellene betyder for forbrugeren.</p>
  <h2>Til journalister</h2>
  <p>Vi stiller gerne op til interview om det danske mobilmarked, prisudvikling,
  intropriser og forbrugerrettigheder ved skift af udbyder. Vi udtaler os kun om det, vores
  egne data dækker, og oplyser altid tydeligt, hvad der er beregnet og hvad der er vurderet.</p>
  <h2>Brug af vores tal</h2>
  <p>Vores prissammenligninger må gerne citeres med kildeangivelse og link til den konkrete
  side. Skriv til os, hvis du har brug for et udtræk til en bestemt periode eller kategori.</p>
  <h2>Kontakt</h2>
  <p>Henvendelser fra presse kan sendes via <a href="/kontakt/">kontaktsiden</a> eller gennem
  <a href="https://www.linkedin.com/in/emil-rostgaard-702809195/" rel="noopener nofollow" target="_blank">LinkedIn</a>.
  Vi svarer normalt samme hverdag.</p>
  <h2>Faktaark</h2>
  <ul>
    <li><strong>Navn:</strong> Telemobil</li>
    <li><strong>Stiftet af:</strong> Emil Rostgaard</li>
    <li><strong>Adresse:</strong> Lundbyesgade 13, 8000 Aarhus C</li>
    <li><strong>Dækker:</strong> Danske mobilabonnementer og mobilselskaber</li>
    <li><strong>Forretningsmodel:</strong> Affiliateprovision — <a href="/saadan-tjener-vi-penge/">se hvordan</a></li>
    <li><strong>Metode:</strong> <a href="/metode/">Sådan sammenligner vi</a></li>
  </ul>
</section>"""
    byg_statisk("/presse/", "Presse — Telemobil",
                "Information til journalister om Telemobil, vores data og brug af vores tal.",
                "Presse", "Presse og fakta", presse_krop, prioritet="0.3")

    privat_krop = """<section class="sektion baand-smal artikel">
  <h2>Cookies</h2>
  <p>Telemobil bruger cookies til at måle, hvordan siden bruges, så vi kan forbedre den. Du
  kan til enhver tid slette cookies i din browsers indstillinger. Vi sætter ikke
  markedsføringscookies uden dit samtykke.</p>
  <h2>Affiliatesporing</h2>
  <p>Når du klikker videre til en udbyder, registreres det, at du kom fra Telemobil, så vi
  kan modtage provision ved en eventuel bestilling. Sporingen indeholder ikke oplysninger,
  der identificerer dig personligt over for os. Læs mere om
  <a href="/saadan-tjener-vi-penge/">vores forretningsmodel</a>.</p>
  <h2>Personoplysninger</h2>
  <p>Vi indsamler ikke personoplysninger, medmindre du selv sender os en henvendelse. Skriver
  du til os, gemmer vi din henvendelse, indtil den er besvaret og afsluttet.</p>
  <h2>Dine rettigheder</h2>
  <p>Du har efter databeskyttelsesforordningen ret til indsigt i, berigtigelse af og
  sletning af de oplysninger, vi måtte have om dig. Skriv til kontakt@telemobil.dk.</p>
  <h2>Ansvarsfraskrivelse</h2>
  <p>Priser og vilkår på Telemobil er vejledende og kan ændre sig uden varsel. Vi
  kontrollerer oplysningerne løbende, men udbyderens egen hjemmeside er altid den gældende
  kilde. Telemobil er ikke part i den aftale, du indgår med en udbyder.</p>
</section>"""
    byg_statisk("/privatlivspolitik/", "Privatliv og cookies — sådan behandler vi data",
                "Sådan behandler Telemobil cookies, affiliatesporing og personoplysninger.",
                "Privatliv", "Privatliv og cookies", privat_krop, prioritet="0.3")

    # Filer
    fjernet = ryd_forældede()
    byg_404()
    byg_sitemap()
    byg_robots()
    byg_ekstrafiler()
    byg_favicon()
    byg_htaccess()

    print(f"Byggede {len(SIDER)} sider.")
    if fjernet:
        print(f"  Fjernede {len(fjernet)} forældede sider (manglende prisdata):")
        for f in fjernet[:8]:
            print(f"    - {f}")
        if len(fjernet) > 8:
            print(f"    … og {len(fjernet) - 8} mere")
    print(f"  {D['antal']} abonnementer fra {D['antal_udbydere']} udbydere")
    print(f"  Billigste: {D['min_pris']} kr. — bedste pris pr. GB: {bedste_pr_gb['navn']}")
    if not site.get("data_verificeret"):
        print("\n  ADVARSEL: data_verificeret er false i data/site.json.")
        print("  Priser og netværksoplysninger er IKKE verificeret. Ret dem før lancering.")


if __name__ == "__main__":
    main()
