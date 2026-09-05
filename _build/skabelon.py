import re
# -*- coding: utf-8 -*-
"""Skabelonlag for telemobil.dk — HTML-shell, navigation og genbrugelige komponenter."""

import json
import html

DOMAENE = "https://telemobil.dk"
SITENAVN = "Telemobil"

# Sættes af build.py fra data/site.json. Står tomt, viser footeren ingenting
# frem for en tom linje.
FIRMA = {"navn": None, "cvr": None, "cvr_url": None}

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

# Menuen viser kun de sider, folk faktisk leder efter. Resten står i footeren.
# En liste på 22 punkter kan ikke skimmes — den bliver til en mur, man lukker igen.
SAMMENLIGN_MENU = [
    ("/billigste-mobilabonnement/", "Billigste abonnement", "Hele markedet sorteret efter pris"),
    ("/bedste-mobilabonnement/", "Bedste abonnement", "Bedst samlet værdi"),
    ("/kampagner/", "Kampagner og tilbud", "Intropriser og gaver lige nu"),
    ("/mobilabonnement-med-fri-data/", "Fri data", "Ubegrænset data i Danmark"),
    ("/mobilabonnement-med-fri-tale/", "Fri tale", "Ubegrænsede opkald og sms"),
    ("/mobilabonnement-uden-binding/", "Uden binding", "Opsig når du vil"),
    ("/mobilabonnement-med-streaming/", "Med streaming", "Streamingtjenester i prisen"),
    ("/mobilabonnement-med-musik/", "Med musik", "Musik, podcast og lydbøger"),
    ("/mobilabonnement-med-esim/", "Med eSIM", "Klar samme dag"),
    ("/mobilabonnement-til-boern/", "Til børn", "Trygt og uden overraskelser"),
    ("/mobilabonnement-under-100-kr/", "Under 100 kr.", "Alle billige abonnementer"),
]

# Alt det øvrige — findes i footeren og i krydslinks, ikke i topmenuen.
SAMMENLIGN_OEVRIGE = [
    ("/prisudvikling/", "Prisudvikling", "Stiger eller falder priserne?"),
    ("/mobilabonnement-med-telefon/", "Med telefon", "Regn efter før du binder dig"),
    ("/mobilabonnement-uden-data/", "Uden data", "Kun tale og sms"),
    ("/mobilabonnement-til-unge/", "Til unge", "Meget data, ingen binding"),
    ("/mobilabonnement-til-aeldre/", "Til ældre", "Tryghed frem for laveste pris"),
    ("/taletidskort/", "Taletidskort", "Forudbetalt uden regning"),
    ("/mobilabonnement-1-10-gb/", "1–10 GB", "Til let brug"),
    ("/mobilabonnement-10-30-gb/", "10–30 GB", "Danmarks mest almindelige"),
    ("/mobilabonnement-30-50-gb/", "30–50 GB", "Til pendleren"),
    ("/mobilabonnement-50-gb/", "50 GB og op", "Til storforbrugeren"),
    ("/mobilabonnement-100-gb/", "100 GB og op", "Mobilen som internet"),
]

# Flad liste — sitemap og krydslinks vil have dem alle.
SAMMENLIGN = SAMMENLIGN_MENU + SAMMENLIGN_OEVRIGE

VAERKTOEJER = [
    ("/daekningskort/", "Dækningstjek", "Se hvilket net der dækker hos dig"),
    ("/sammenlign/", "Udbyder mod udbyder", "To selskaber side om side"),
    ("/hvem-ringer-til-mig/", "Hvem ringer til mig?", "Slå et ukendt nummer op"),
    ("/speedtest/", "Hastighedstest", "Mål din forbindelse"),
    ("/12-maaneders-prisen/", "12-måneders-prisen", "Sådan regner vi"),
]

VAERKTOEJER_OEVRIGE = [
    ("/mobilabonnement-med-streaming/tjenester/", "Streaming pr. tjeneste", "Netflix, HBO Max, Disney+ …"),
    ("/netvaerk/", "Mobilnetværk", "TDC NET, Telenor og 3"),
    ("/landekoder/", "Landekoder", "Alle telefonkoder med søgning"),
    ("/hvad-koster-et-mobilabonnement/", "Hvad koster det?", "Gennemsnit og statistik"),
    ("/ordbog/", "Teleordbog", "Alle begreber forklaret"),
    ("/pin-og-puk-kode/", "PIN- og PUK-kode", "Simkortet er spærret?"),
]

MENU = [
    ("/billigste-mobilabonnement/", "Billigste abonnement"),
    ("/bedste-mobilabonnement/", "Bedste abonnement"),
    ("/guides/", "Guides"),
    ("/om-os/", "Om os"),
]


# Bredbåndssektionen har sine egne undersider. Sættes af build.py.
BREDBAAND_MENU = [
    ("/bredbaand/", "Alle bredbåndsabonnementer"),
    ("/bredbaand/fiberbredbaand/", "Fiber"),
    ("/bredbaand/5g-bredbaand/", "5G-bredbånd"),
    ("/bredbaand/coax-bredbaand/", "Coax"),
    ("/guides/mobilt-bredbaand/", "Guide: mobilt bredbånd"),
]

NAV_UDBYDERE = []
HURTIGPRIS = ""
OPDATERET_GLOBAL = ""

# Uden en versionsnøgle ville browsere holde fast i den gamle CSS og JS i et år,
# fordi .htaccess sætter Cache-Control: immutable. Nøglen skifter, når filen gør.
def _filversion(relativ_sti):
    import hashlib
    import os as _os
    rod = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    f = _os.path.join(rod, relativ_sti.lstrip("/"))
    try:
        with open(f, "rb") as fh:
            return hashlib.sha1(fh.read()).hexdigest()[:8]
    except OSError:
        return "0"


CSS_INLINE = ""
CSS_V = _filversion("assets/css/telemobil.css")
JS_V = _filversion("assets/js/telemobil.js")


def e(t):
    """Escaper tekst til HTML."""
    return html.escape(str(t), quote=True)


def kr(v):
    """Formaterer et kronebeløb dansk."""
    return f"{v:,.0f}".replace(",", ".")


def gb_tekst(gb):
    if gb >= 9999:
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

MAANEDER_ISO = {"januar": "01", "februar": "02", "marts": "03", "april": "04", "maj": "05",
                "juni": "06", "juli": "07", "august": "08", "september": "09",
                "oktober": "10", "november": "11", "december": "12"}


def opdateret_til_iso(tekst):
    """Konverterer '13. august 2026' til ISO-format til meta-tags."""
    m = re.match(r"(\d{1,2})\. (\w+) (\d{4})", tekst or "")
    if not m:
        return ""
    dag, maaned, aar = m.groups()
    return f"{aar}-{MAANEDER_ISO.get(maaned, '01')}-{int(dag):02d}"


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
          hero=None, efter_hero="", opdateret="", ekstra_hoved="", toc=True):
    indhold, _toc = indholdsfortegnelse(indhold)
    toc = _toc if toc else ""
    if toc:
        indhold = indhold.replace('<section class="sektion baand-smal artikel">',
                                  f'<section class="sektion baand-smal">{toc}</section>'
                                  '<section class="sektion baand-smal artikel">', 1)
    minutter = laesetid(indhold)
    opdateret_iso = opdateret_til_iso(opdateret)
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
        f'<a href="{h}"{aktiv(h)}><span class="mp-navn">{e(t)}</span></a>'
        for h, t, _b in SAMMENLIGN_MENU
    )

    vaerktoej_punkter = "".join(
        f'<a href="{h}"{aktiv(h)}><span class="mp-navn">{e(t)}</span></a>'
        for h, t, _b in VAERKTOEJER
    )
    bredbaand_punkter = "".join(
        f'<a href="{h}"{aktiv(h)}><span class="mp-navn">{e(t)}</span></a>'
        for h, t in BREDBAAND_MENU
    )
    udbyder_punkter = "".join(
        f'<a href="/udbydere/{u["slug"]}/"{aktiv("/udbydere/" + u["slug"] + "/")}>'
        # Tom alt er korrekt: navnet står i teksten ved siden af, og en
        # skærmlæser skal ikke læse det to gange.
        f'<img src="/assets/img/logoer/{u["logo"]}" alt="" aria-hidden="true" loading="lazy"'
        f' width="{round(u.get("logo_w", 240) * 18 / u.get("logo_h", 96))}" height="18" decoding="async">'
        f'<span>{e(u["navn"])}</span></a>'
        for u in NAV_UDBYDERE
    )

    navpunkter = f'''
<div class="nav-gruppe">
  <button type="button" class="nav-knap" aria-expanded="false" aria-controls="menu-sammenlign">
    Sammenlign <span class="pil-ned" aria-hidden="true"></span>
  </button>
  <div class="nav-menu nav-menu-enkel" id="menu-sammenlign">{sammenlign_punkter}</div>
</div>
<div class="nav-gruppe">
  <button type="button" class="nav-knap" aria-expanded="false" aria-controls="menu-vaerktoej">
    Værktøjer <span class="pil-ned" aria-hidden="true"></span>
  </button>
  <div class="nav-menu nav-menu-enkel" id="menu-vaerktoej">{vaerktoej_punkter}</div>
</div>
<div class="nav-gruppe">
  <button type="button" class="nav-knap" aria-expanded="false" aria-controls="menu-bredbaand">
    Bredbånd <span class="pil-ned" aria-hidden="true"></span>
  </button>
  <div class="nav-menu nav-menu-enkel" id="menu-bredbaand">{bredbaand_punkter}</div>
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
    navpunkter += '<a href="/billigste-mobilabonnement/" class="nav-cta" data-hurtigpris>Se priser</a>'

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
<link rel="alternate" hreflang="da-DK" href="{kanonisk}">
<link rel="alternate" hreflang="x-default" href="{kanonisk}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="author" content="{e(FORFATTER['navn'])}">
<meta name="twitter:label1" content="Estimeret læsetid">
<meta name="twitter:data1" content="{minutter} minutter">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="geo.region" content="DK">
<meta name="language" content="Danish">
<meta name="publisher" content="Telemobil">
<meta property="article:publisher" content="{DOMAENE}/">
<meta property="article:modified_time" content="{opdateret_iso}">
<meta name="rating" content="general">
<meta name="geo.placename" content="Aarhus, Danmark">
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
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" media="print" onload="this.media='all';this.onload=null"
      href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap"></noscript>
<script>document.documentElement.className+=" js";</script>
<style>{CSS_INLINE}</style>
{ekstra_hoved}
{blokke}</head>
<body>
<a class="spring" href="#indhold">Spring til indhold</a>

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
{HURTIGPRIS}
<script src="/assets/js/telemobil.js?v={JS_V}" defer></script>
</body>
</html>
"""


def cvrlinje():
    """CVR i footeren, med link til det officielle register.

    Et registreret selskab bag sitet er et af de få tillidssignaler, en læser
    selv kan efterprøve. Vi linker til Virk frem for en aggregator, fordi det
    er kilden."""
    if not FIRMA.get("cvr"):
        return ""
    navn = e(FIRMA.get("navn") or "")
    if FIRMA.get("cvr_url"):
        nr = (f'<a href="{e(FIRMA["cvr_url"])}" rel="noopener nofollow" target="_blank">'
              f'CVR {e(FIRMA["cvr"])}</a>')
    else:
        nr = f'CVR {e(FIRMA["cvr"])}'
    return f'<br>{navn} · {nr}' if navn else f'<br>{nr}'


def fod(opdateret):
    """Kompakt footer. Kategorierne ligger i menuen — her er kun det nødvendige."""
    return f"""<footer class="fod">
  <div class="baand">
    <div class="fod-gitter">
      <div class="fod-om">
        <a href="/" class="logo">
          <span class="logo-maerke" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
          <span class="logo-tekst">Tele<em>mobil</em></span>
        </a>
        <p>Uafhængig dansk sammenligning af mobilabonnementer. Vi beregner
        <a href="/12-maaneders-prisen/">12-måneders-prisen</a> — den reelle pris, når
        intropris, normalpris og oprettelse regnes sammen.</p>
        <p class="fod-adresse">
          Telemobil<br>
          Lundbyesgade 13<br>
          8000 Aarhus C<br>
          <a href="mailto:kontakt@telemobil.dk">kontakt@telemobil.dk</a>
          {cvrlinje()}
        </p>
      </div>

      <div>
        <div class="fodtitel">Flere sammenligninger</div>
        <ul>
          <li><a href="/udbydere/">Alle udbydere</a></li>
          <li><a href="/mobilabonnement-med-telefon/">Med telefon</a></li>
          <li><a href="/mobilabonnement-uden-data/">Uden data</a></li>
          <li><a href="/mobilabonnement-til-unge/">Til unge</a></li>
          <li><a href="/mobilabonnement-til-aeldre/">Til ældre</a></li>
          <li><a href="/taletidskort/">Taletidskort</a></li>
          <li><a href="/prisudvikling/">Prisudvikling</a></li>
        </ul>
      </div>

      <div>
        <div class="fodtitel">Bredbånd</div>
        <ul>
          <li><a href="/bredbaand/">Alle bredbåndsabonnementer</a></li>
          <li><a href="/bredbaand/fiberbredbaand/">Fiber</a></li>
          <li><a href="/bredbaand/5g-bredbaand/">5G-bredbånd</a></li>
          <li><a href="/bredbaand/coax-bredbaand/">Coax</a></li>
          <li><a href="/guides/mobilt-bredbaand/">Mobilt bredbånd — guide</a></li>
        </ul>
      </div>

      <div>
        <div class="fodtitel">Efter datamængde</div>
        <ul>
          <li><a href="/mobilabonnement-1-10-gb/">1–10 GB</a></li>
          <li><a href="/mobilabonnement-10-30-gb/">10–30 GB</a></li>
          <li><a href="/mobilabonnement-30-50-gb/">30–50 GB</a></li>
          <li><a href="/mobilabonnement-50-gb/">50 GB og op</a></li>
          <li><a href="/mobilabonnement-100-gb/">100 GB og op</a></li>
          <li><a href="/hvad-koster-et-mobilabonnement/">Hvad koster det?</a></li>
        </ul>
      </div>

      <div>
        <div class="fodtitel">Værktøjer</div>
        <ul>
          <li><a href="/netvaerk/">Mobilnetværk</a></li>
          <li><a href="/mobilabonnement-med-streaming/tjenester/">Streaming pr. tjeneste</a></li>
          <li><a href="/landekoder/">Landekoder</a></li>
          <li><a href="/ordbog/">Teleordbog</a></li>
          <li><a href="/pin-og-puk-kode/">PIN- og PUK-kode</a></li>
        </ul>
      </div>

      <div>
        <div class="fodtitel">Værktøjer og guides</div>
        <ul>
          <li><a href="/guides/">Alle guides</a></li>
          <li><a href="/daekningskort/">Dækningstjek</a></li>
          <li><a href="/speedtest/">Hastighedstest</a></li>
          <li><a href="/landekoder/">Landekoder</a></li>
          <li><a href="/hvem-ringer-til-mig/">Hvem ringer til mig?</a></li>
          <li><a href="/ordbog/">Teleordbog</a></li>
        </ul>
      </div>

      <div>
        <div class="fodtitel">Om Telemobil</div>
        <ul>
          <li><a href="/om-os/">Om os</a></li>
          <li><a href="/om/emil-rostgaard/">{e(FORFATTER['navn'])}</a></li>
          <li><a href="/metode/">Vores metode</a></li>
          <li><a href="/saadan-tjener-vi-penge/">Sådan tjener vi penge</a></li>
          <li><a href="/kontakt/">Kontakt</a></li>
          <li><a href="/presse/">Presse</a></li>
        </ul>
      </div>
    </div>

    <div class="fod-bund">
      <span>© {opdateret[-4:] or '2026'} Telemobil · Priser er vejledende og kan ændre sig.</span>
      <span class="fod-jura">
        <a href="/privatlivspolitik/">Privatliv</a>
        <a href="/cookiepolitik/">Cookies</a>
        <a href="#" data-cookievalg>Cookieindstillinger</a>
        <a href="/saadan-tjener-vi-penge/">Annonceoplysning</a>
      </span>
    </div>
    <p class="fod-provision">Telemobil modtager provision fra udvalgte udbydere, når du
    bestiller via vores links. Det påvirker ikke sorteringen i vores tabeller, som altid
    er efter pris.</p>
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
      <a href="{f['linkedin']}" rel="me noopener nofollow" target="_blank">LinkedIn</a>
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
    endelig = [a for a in med_data if a["data_gb"] < 9999]
    frie = [a for a in betalte if a["data_gb"] >= 9999]

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


def _netgruppe(u):
    """Rå netværksnøgle til filtrering."""
    n = (u.get("netvaerk") or "").strip()
    if n in ("", "MVNO", "Se udbyder"):
        return "MVNO"
    return n


def stjerner(u, *, kompakt=False):
    """Anmeldelsesscore som fem stjerner, hvor den delvise stjerne fyldes med CSS.

    Vi bruger ikke halvstjerne-tegn — de findes ikke i alle skrifttyper og
    falder tilbage til noget tilfældigt. I stedet lægges fem fyldte stjerner
    oven på fem tomme og klippes til den rigtige bredde.

    Trustpilot må gerne nævnes ved navn som kilde. Det, man ikke må, er at
    bruge deres logo eller grønne stjerne — derfor vores egne."""
    tp = (u.get("trustpilot") or {})
    score, antal, hentet = tp.get("score"), tp.get("antal"), tp.get("hentet")
    if not score:
        return ""
    pct = max(0, min(100, round(score / 5 * 100)))
    tal = f"{score:.1f}".replace(".", ",")
    graf = (f'<span class="tp-stjerner" role="img" aria-label="{tal} af 5 stjerner">'
            f'<span class="tp-tom">★★★★★</span>'
            f'<span class="tp-fyld" style="width:{pct}%">★★★★★</span></span>')
    if kompakt:
        titel = (f"Trustpilot {tal} af 5"
                 + (f" · {kr(antal)} anmeldelser" if antal else "")
                 + (f" · hentet {hentet}" if hentet else ""))
        return (f'<span class="tp tp-lille" title="{e(titel)}">{graf}'
                f'<span class="tp-under"><b>{tal}</b> <i>på Trustpilot</i></span></span>')
    an = f" baseret på {kr(antal)} anmeldelser" if antal else ""
    da = f" Hentet {e(hentet)}." if hentet else ""
    return (f'<p class="tp tp-stor">{graf}'
            f'<span><strong>{tal} af 5</strong> på Trustpilot{an}.{da}</span></p>')


def prisrække(a, u, billigst_pr_gb=False, gnsnit_aar=None, dyn=None):
    """Ét abonnement som kompakt rækkekort med foldbare detaljer."""
    logo = f"/assets/img/logoer/{u['logo']}"
    forbrug = a.get("forbrugsafregnet")
    intro = a.get("intro_pris") is not None and a.get("intro_mdr")
    vist_pris = a["intro_pris"] if intro else a["pris"]

    pr_gb = a["pris"] / a["data_gb"] if 0 < a["data_gb"] < 9999 else 0
    pr_gb_tekst = (f"{pr_gb:.2f}".replace(".", ",") + " kr.") if pr_gb else "—"
    g = gns12(a)
    aar = (g * 12) if g is not None else 0

    if intro:
        m = min(a["intro_mdr"], 12)
        formel = f'{a["intro_pris"]}×{m} + {a["pris"]}×{12 - m}'
    else:
        formel = f'{a["pris"]}×12'
    if a.get("oprettelse"):
        formel += f' + {a["oprettelse"]}'
    formel += " ÷ 12"

    # ---- Faneblad over kortet: ét budskab, ikke fem -----------------------
    dyn_liste = (dyn or {}).get(a["id"], [])
    if a.get("badge"):
        flagtekst, flagklasse = e(a["badge"]), "sol"
    elif intro:
        flagtekst = f'{kr(a["intro_pris"])} kr./md. de første {a["intro_mdr"]} mdr.'
        flagklasse = "nat"
    elif dyn_liste:
        flagtekst, flagklasse = e(dyn_liste[0][0]), dyn_liste[0][1]
    else:
        flagtekst, flagklasse = "", ""
    flag = (f'<span class="pk-flag pk-flag-{flagklasse}">{flagtekst}</span>'
            if flagtekst else "")

    # ---- Fire nøgletal — det folk faktisk scanner efter ------------------
    stats = [
        (gb_tekst(a["data_gb"]), "data i Danmark"),
        ("Fri" if a["tale"] == "fri" else e(a["tale"]), "tale"),
        ("Ingen" if a["binding"] == 0 else f'{a["binding"]} mdr.', "binding"),
        (f'{kr(a.get("oprettelse", 0))} kr.', "oprettelse"),
    ]
    statbokse = "".join(f'<div class="pk-stat"><b>{v}</b><span>{t}</span></div>'
                        for v, t in stats)

    # ---- Højst tre plusser, så rækken ikke svulmer op -------------------
    plus = []
    if a["data_gb"] >= 9999:
        plus.append("Fri data")
    elif a["data_gb"] > 0:
        plus.append(f'{a["data_gb"]} GB data')
    plus.append("Ingen binding" if a["binding"] == 0 else f'{a["binding"]} mdr. binding')
    if a.get("femg") and a["data_gb"] > 0:
        plus.append("5G")
    if a.get("esim"):
        plus.append("eSIM")
    if a.get("streaming"):
        n = len(a["streaming"])
        plus.append(f'{n} streamingtjeneste{"r" if n > 1 else ""}')
    if a.get("eu_gb", 0) >= 9999:
        plus.append("Fri EU-data")
    chips = "".join(f'<span class="pk-chip">{e(t)}</span>' for t in plus[:3])

    # ---- Advarsler hører i detaljepanelet, ikke i rækken ----------------
    advarsler = []
    if a["data_gb"] > 0 and not a.get("eu_gb"):
        advarsler.append("Ingen EU-data inkluderet — data i udlandet koster ekstra.")
    if a.get("sms") and a["sms"] != "fri":
        advarsler.append(f'Sms er begrænset til {e(a["sms"])}.')
    if a.get("oprettelse"):
        advarsler.append(f'Oprettelse på {kr(a["oprettelse"])} kr. betales én gang.')
    advarhtml = ("<ul class=\"pk-advar\">"
                 + "".join(f"<li>{t}</li>" for t in advarsler) + "</ul>") if advarsler else ""

    eu_tekst = ("—" if a["data_gb"] == 0 else "Fri" if a.get("eu_gb", 0) >= 9999
                else "Ingen" if not a.get("eu_gb") else f'{a["eu_gb"]} GB')
    fakta = [
        ("Netværk", netlabel(u)),
        ("EU-data", eu_tekst),
        ("Pris pr. GB", pr_gb_tekst),
        ("Sms", "Fri" if a.get("sms") == "fri" else e(a.get("sms") or "—")),
        ("Samlet på 12 mdr.", f'{kr(aar)} kr.' if aar else "—"),
        ("Gns. pr. md. over 12 mdr.", f'{kr(g)} kr.' if g is not None else "—"),
    ]
    if a.get("streaming"):
        fakta.append(("Streaming", e(", ".join(a["streaming"]))))
    faktahtml = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in fakta)

    # ---- Prisblok --------------------------------------------------------
    if forbrug:
        prisblok = ('<div class="pk-tal"><b>0</b><span>kr.</span></div>'
                    '<div class="pk-under">+ takst pr. minut og sms</div>')
    elif intro:
        prisblok = (f'<div class="pk-tal"><b>{kr(a["intro_pris"])}</b><span>kr.</span></div>'
                    f'<div class="pk-under">Herefter {kr(a["pris"])} kr./md.</div>')
    else:
        prisblok = (f'<div class="pk-tal"><b>{kr(a["pris"])}</b><span>kr.</span></div>'
                    f'<div class="pk-under">{kr(aar)} kr. samlet på 12 mdr.</div>')

    spar = ""
    if gnsnit_aar and not forbrug and aar and aar < gnsnit_aar:
        spar = f'<div class="pk-spar">{kr((gnsnit_aar - aar) / 12)} kr./md. under snittet</div>'

    # ---- Filterflag ------------------------------------------------------
    ekstra = []
    if a.get("femg") and a["data_gb"] > 0:
        ekstra.append("5g")
    if a.get("esim"):
        ekstra.append("esim")
    if a.get("tale") == "fri":
        ekstra.append("fritale")
    if a.get("eu_gb", 0) > 0:
        ekstra.append("eudata")
    if a.get("streaming"):
        ekstra.append("streaming")

    tag = ("Taletid" if a["data_gb"] == 0
           else "5G internet" if a.get("femg") else "4G internet")
    panel_id = f'd-{e(a["id"])}'
    klasse = " fremhaev" if billigst_pr_gb else ""
    logo_w = round(u.get("logo_w", 240) * 40 / u.get("logo_h", 96))

    return f"""<article class="plan{klasse}" data-gb="{a['data_gb']}" data-pris="{vist_pris}"
  data-normalpris="{a['pris']}" data-prgb="{pr_gb:.4f}" data-aar="{aar:.0f}"
  data-binding="{a['binding']}" data-net="{e(_netgruppe(u))}" data-slug="{e(u['slug'])}"
  data-tilbud="{1 if intro else 0}" data-ekstra="{' '.join(ekstra)}"
  data-tp="{(u.get('trustpilot') or {}).get('score') or 0}"
  data-udbyder="{e(u['navn'])}">
  {flag}
  <div class="pk-raekke">
    <div class="pk-ident">
      <img src="{logo}" alt="{e(u['navn'])} logo" loading="lazy"
        width="{logo_w}" height="40" decoding="async">
      <span class="pk-tag">{tag}</span>
      {stjerner(u, kompakt=True)}
    </div>
    <div class="pk-midt">
      <h3 class="pk-navn">{e(u['navn'])} – {e(a['navn'])}</h3>
      <div class="pk-stats">{statbokse}</div>
      <div class="pk-chips">{chips}</div>
    </div>
    <div class="pk-pris">
      {prisblok}
      {spar}
      <button type="button" class="pk-detaljer" aria-expanded="false"
        aria-controls="{panel_id}">Se detaljer</button>
      <a class="knap knap-primaer pk-cta" href="{a['link']}" rel="sponsored nofollow noopener"
        target="_blank" data-udgaaende="{e(u['slug'])}" data-abonnement="{e(a['id'])}"
        aria-label="Se tilbud på {e(a['navn'])} hos {e(u['navn'])}">Se tilbud</a>
    </div>
  </div>
  <div class="pk-panel" id="{panel_id}" hidden>
    <dl class="pk-fakta">{faktahtml}</dl>
    {advarhtml}
    <div class="pk-panelfod">
      <span class="pk-formel" title="Sådan er gennemsnittet beregnet">{formel}</span>
      <a href="/udbydere/{u['slug']}/">Læs vores gennemgang af {e(u['navn'])} →</a>
    </div>
  </div>
</article>"""


def _drop(navn, noegle, valg, ikon=""):
    """Én filterknap med foldemenu og flervalg."""
    punkter = "".join(
        f'<label><input type="checkbox" data-f="{noegle}" value="{e(v)}">'
        f'<span>{e(t)}</span></label>' for v, t in valg)
    return f"""<div class="fb-grp" data-gruppe="{noegle}">
      <button type="button" class="fb-knap" aria-expanded="false">{ikon}{e(navn)}<i class="fb-pil" aria-hidden="true"></i></button>
      <div class="fb-menu" hidden>{punkter}
        <button type="button" class="fb-ryd" data-ryd="{noegle}">Ryd</button>
      </div>
    </div>"""


def filterbar(abonnementer, udbydere_map, forvalg=None):
    """Kompakt filterlinje med foldemenuer — samme højde som én knap."""
    selskaber, net = {}, {}
    for a in abonnementer:
        u = udbydere_map[a["udbyder"]]
        selskaber[u["slug"]] = u["navn"]
        net[_netgruppe(u)] = netlabel(u)

    data_valg = [("lille", "Op til 15 GB"), ("mellem", "15–50 GB"),
                 ("stor", "50–100 GB"), ("xl", "Over 100 GB"), ("fri", "Fri data")]
    pris_valg = [("u50", "Under 50 kr."), ("50-99", "50–99 kr."),
                 ("100-149", "100–149 kr."), ("150-199", "150–199 kr."),
                 ("o200", "200 kr. og op")]
    bind_valg = [("0", "Ingen binding"), ("1-6", "Op til 6 mdr."), ("o6", "Over 6 mdr.")]
    ekstra_valg = [("5g", "5G"), ("esim", "eSIM"), ("fritale", "Fri tale"),
                   ("eudata", "EU-data"), ("streaming", "Streaming")]
    selskab_valg = sorted(selskaber.items(), key=lambda x: x[1].lower())
    net_valg = sorted(net.items(), key=lambda x: x[1].lower())

    fv = f' data-forvalg="{e(json.dumps(forvalg))}"' if forvalg else ""
    return f"""<div class="filterbar"{fv} role="group" aria-label="Filtrér abonnementer">
  <div class="fb-venstre">
    {_drop("Data", "data", data_valg)}
    {_drop("Pris", "pris", pris_valg)}
    {_drop("Binding", "binding", bind_valg)}
    {_drop("Selskab", "slug", selskab_valg)}
    {_drop("Netværk", "net", net_valg)}
    {_drop("Ekstra", "ekstra", ekstra_valg)}
    <div class="fb-grp fb-sortgrp">
      <label class="visuelt-skjult" for="fb-sorter">Sortér efter</label>
      <select id="fb-sorter" class="fb-sorter" data-sorter>
        <option value="pris">Pris: lav til høj</option>
        <option value="aar">Gns. 12 mdr.: lav til høj</option>
        <option value="prgb">Pris pr. GB: lav til høj</option>
        <option value="gb">Mest data først</option>
        <option value="tp">Bedst bedømt først</option>
      </select>
    </div>
    <button type="button" class="fb-toggle" data-kun-tilbud aria-pressed="false">
      <span aria-hidden="true">★</span> Tilbud</button>
    <button type="button" class="fb-nulstil" data-nulstil hidden>Nulstil</button>
  </div>
  <span class="fb-antal"><span data-antal-vist>{len(abonnementer)}</span></span>
</div>"""


def pristabel(abonnementer, udbydere_map, *, titel, undertitel, filtre=True,
              billigst_id=None, id_attr="sammenlign", vis=10, opdateret=None,
              forvalg=None):
    if opdateret is None:
        opdateret = OPDATERET_GLOBAL
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

    filterhtml = filterbar(abonnementer, udbydere_map, forvalg) if filtre else ""

    return f"""<section class="sektion baand" id="{id_attr}">
  <div class="sektion-hoved afslør">
    <div class="sh-tekst">
      <span class="etiket">Sammenligning</span>
      <h2>{e(titel)}</h2>
      <p class="led">{undertitel}</p>
    </div>
    <p class="opdateret-stribe">
      <span class="op-prik" aria-hidden="true"></span>
      <span><strong>Opdateret {e(opdateret)}</strong> · {len(abonnementer)} abonnementer
      hentet automatisk fra udbydernes datafeed</span>
    </p>
  </div>
  {filterhtml}
  <div class="listeramme afslør">
    <div class="planliste">{kort}</div>
    <p class="pk-tom" data-tom hidden>Ingen abonnementer matcher filtrene.
      <button type="button" class="knap knap-linje knap-lille" data-nulstil>Nulstil filtre</button></p>
    {visflere}
    <div class="listefod">
      <span>Klik <strong>Se detaljer</strong> for EU-data, pris pr. GB og den reelle
      12-måneders pris, hvor intropris, normalpris og oprettelse regnes sammen.</span>
      <span>Kilde: udbydernes egne prislister</span>
    </div>
  </div>
  {afsloering(kort=True)}
</section>"""
