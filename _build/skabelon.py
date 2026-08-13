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

MENU = [
    ("/billigste-mobilabonnement/", "Billigste abonnement"),
    ("/mobilabonnement-med-fri-data/", "Fri data"),
    ("/udbydere/", "Udbydere"),
    ("/guides/", "Guides"),
    ("/om-os/", "Om os"),
]


def e(t):
    """Escaper tekst til HTML."""
    return html.escape(str(t), quote=True)


def kr(v):
    """Formaterer et kronebeløb dansk."""
    return f"{v:,.0f}".replace(",", ".")


def gb_tekst(gb):
    return "Fri data" if gb >= 900 else f"{gb} GB"


def netlabel(u):
    """Kort netværksetiket til tabeller. MVNO = udbyder uden eget net."""
    n = u.get("netvaerk", "")
    return "MVNO" if n in ("", "MVNO", "Se udbyder") else f"{e(n)}s net"


# ---------------------------------------------------------------- HTML-shell

def shell(*, sti, titel, beskrivelse, indhold, jsonld=None, krumme=None,
          hero=None, opdateret="", ekstra_hoved=""):
    """Bygger en komplet HTML-side."""
    kanonisk = DOMAENE + sti
    blokke = ""
    for blok in (jsonld or []):
        blokke += ('<script type="application/ld+json">'
                   + json.dumps(blok, ensure_ascii=False, separators=(",", ":"))
                   + "</script>\n")

    navpunkter = ""
    for href, tekst in MENU:
        aktiv = ' aria-current="page"' if sti == href or (href != "/" and sti.startswith(href)) else ""
        navpunkter += f'<a href="{href}"{aktiv}>{e(tekst)}</a>'
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
      Tele<em>mobil</em>
    </a>
    <button class="burger" aria-label="Åbn menu" aria-expanded="false" aria-controls="hovedmenu">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="hovedmenu" aria-label="Hovedmenu">{navpunkter}</nav>
  </div>
</header>

{hero or ''}
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
          Tele<em>mobil</em>
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
          <li><a href="/mobilabonnement-med-fri-data/">Fri data</a></li>
          <li><a href="/mobilabonnement-til-unge/">Til unge og studerende</a></li>
          <li><a href="/mobilabonnement-uden-binding/">Uden binding</a></li>
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
          <li><a href="/privatlivspolitik/">Privatliv og cookies</a></li>
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

def prisrække(a, u, billigst_pr_gb=False):
    """Én række i sammenligningstabellen."""
    logo = f"/assets/img/logoer/{u['logo']}"
    pr_gb = a["pris"] / a["data_gb"] if a["data_gb"] < 900 else 0
    pr_gb_tekst = (f"{pr_gb:.2f}".replace(".", ",") + " kr.") if pr_gb else "—"
    styrke = 4 if a["data_gb"] >= 900 else (3 if a["data_gb"] >= 50 else (2 if a["data_gb"] >= 15 else 1))
    bjaelker = "".join(f'<i class="{"t" if i < styrke else ""}"></i>' for i in range(4))

    maerker = ""
    if a.get("badge"):
        maerker = f'<span class="maerke maerke-sol">{e(a["badge"])}</span>'
    if billigst_pr_gb:
        maerker = '<span class="maerke maerke-puls">Bedste pris pr. GB</span>' + maerker

    foer = f'<s>{kr(a["foer_pris"])}</s>' if a.get("foer_pris") else ""
    klasse = ' class="fremhaev"' if billigst_pr_gb else ""

    return f"""<tr{klasse} data-gb="{a['data_gb']}" data-pris="{a['pris']}" data-prgb="{pr_gb:.4f}" data-udbyder="{e(u['navn'])}">
  <td>
    <div class="t-udbyder">
      <img src="{logo}" alt="{e(u['navn'])} logo" loading="lazy" height="22">
      <span><b>{e(a['navn'])}</b><small>{netlabel(u)}</small></span>
    </div>
    {maerker}
  </td>
  <td class="t-data">{gb_tekst(a['data_gb'])}<div class="bjaelke" aria-hidden="true">{bjaelker}</div></td>
  <td>{'Fri' if a['tale'] == 'fri' else e(a['tale'])}</td>
  <td class="t-pr-gb">{pr_gb_tekst}</td>
  <td>{'Nej' if a['binding'] == 0 else str(a['binding']) + ' mdr.'}</td>
  <td class="t-pris">{foer}{kr(a['pris'])} kr.</td>
  <td><a class="knap knap-primaer knap-lille" href="{a['link']}" rel="sponsored nofollow noopener" target="_blank"
        data-udgaaende="{e(u['slug'])}" data-abonnement="{e(a['id'])}">Se tilbud</a></td>
</tr>"""


def pristabel(abonnementer, udbydere_map, *, titel, undertitel, filtre=True,
              billigst_id=None, id_attr="sammenlign"):
    raekker = ""
    for a in abonnementer:
        u = udbydere_map[a["udbyder"]]
        raekker += prisrække(a, u, billigst_pr_gb=(a["id"] == billigst_id))

    filterhtml = ""
    if filtre:
        filterhtml = """<div class="filtre">
  <span class="maerkat">Filtrér</span>
  <button class="chip" data-filter="alle" aria-pressed="true">Alle</button>
  <button class="chip" data-filter="lille" aria-pressed="false">Op til 15 GB</button>
  <button class="chip" data-filter="mellem" aria-pressed="false">15–50 GB</button>
  <button class="chip" data-filter="stor" aria-pressed="false">Over 50 GB</button>
  <button class="chip" data-filter="fri" aria-pressed="false">Fri data</button>
</div>"""

    return f"""<section class="sektion baand" id="{id_attr}">
  <div class="sektion-hoved afslør">
    <span class="etiket">Sammenligning</span>
    <h2>{e(titel)}</h2>
    <p class="led">{undertitel}</p>
  </div>
  {filterhtml}
  <div class="tabelramme afslør">
    <div class="tabelrul">
      <table class="pris">
        <caption>Klik på en kolonneoverskrift for at sortere. <span data-antal-vist>{len(abonnementer)}</span> abonnementer vist.</caption>
        <thead>
          <tr>
            <th scope="col" class="sorter" data-noegle="udbyder">Abonnement</th>
            <th scope="col" class="sorter" data-noegle="gb">Data</th>
            <th scope="col">Tale</th>
            <th scope="col" class="sorter" data-noegle="prgb">Pris pr. GB</th>
            <th scope="col">Binding</th>
            <th scope="col" class="sorter" data-noegle="pris" data-retning="op">Pris pr. md.</th>
            <th scope="col"><span class="visuelt-skjult">Link</span></th>
          </tr>
        </thead>
        <tbody>{raekker}</tbody>
      </table>
    </div>
    <div class="tabelfod">
      <span>Sorteret efter laveste månedspris. Priser er vejledende og kan ændre sig uden varsel.</span>
      <span>Kilde: udbydernes egne prislister</span>
    </div>
  </div>
  {afsloering(kort=True)}
</section>"""
