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
    shell, e, kr, gb_tekst, netlabel, DOMAENE, SITENAVN, FORFATTER,
    afsloering, forfatterboks, gennemgangslinje, faqblok, laesvidere,
    ctabaand, pristabel,
)
import indhold  # noqa: E402

MAANEDER = ["januar", "februar", "marts", "april", "maj", "juni", "juli",
            "august", "september", "oktober", "november", "december"]

sider = []  # (sti, prioritet, hyppighed)


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
        sider.append((sti, prioritet, hyppighed))
    return filsti


def indlaes(navn):
    with open(os.path.join(ROD, "data", navn), encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------- data

site = indlaes("site.json")
ud_data = indlaes("udbydere.json")
ab_data = indlaes("abonnementer.json")

UDBYDERE = ud_data["udbydere"]
UMAP = {u["slug"]: u for u in UDBYDERE}
ABON = sorted(ab_data["abonnementer"], key=lambda a: a["pris"])
for a in ABON:
    if a["udbyder"] not in UMAP:
        raise SystemExit(f"Ukendt udbyder i abonnementer.json: {a['udbyder']}")

IDAG = date.today()
OPDATERET = dansk_dato(IDAG)
ISO = IDAG.isoformat()

# Afledte nøgletal — bruges i tekst, så tal og tabeller aldrig kan komme i utakt
med_gb = [a for a in ABON if a["data_gb"] < 900]
fri = [a for a in ABON if a["data_gb"] >= 900]
billigst = ABON[0]
bedste_pr_gb = min(med_gb, key=lambda a: a["pris"] / a["data_gb"])

D = {
    "min_pris": billigst["pris"],
    "pris_lille": min(a["pris"] for a in ABON if a["data_gb"] <= 10),
    "pris_mellem": min(a["pris"] for a in ABON if 15 <= a["data_gb"] <= 30),
    "pris_stor": min(a["pris"] for a in ABON if 50 <= a["data_gb"] < 900),
    "pris_fri": min(a["pris"] for a in fri) if fri else 199,
    "antal": len(ABON),
    "antal_udbydere": len(UDBYDERE),
    "maks_besparelse": max(a["pris"] for a in ABON) - billigst["pris"],
}


# --------------------------------------------------------------- JSON-LD

ORG = {
    "@type": "Organization",
    "@id": DOMAENE + "/#organisation",
    "name": SITENAVN,
    "url": DOMAENE + "/",
    "description": "Uafhængig dansk sammenligning af mobilabonnementer.",
    "areaServed": {"@type": "Country", "name": "Danmark"},
    "founder": {"@id": DOMAENE + "/om/emil-rostgaard/#person"},
    "sameAs": [FORFATTER["linkedin"]],
}

PERSON = {
    "@type": "Person",
    "@id": DOMAENE + "/om/emil-rostgaard/#person",
    "name": FORFATTER["navn"],
    "url": DOMAENE + "/om/emil-rostgaard/",
    "jobTitle": FORFATTER["rolle"],
    "image": DOMAENE + FORFATTER["billede"],
    "sameAs": [FORFATTER["linkedin"]],
    "knowsAbout": ["Mobilabonnementer", "Telemarkedet i Danmark",
                   "Forbrugerøkonomi", "Prissammenligning"],
    "worksFor": {"@id": DOMAENE + "/#organisation"},
}

WEBSITE = {
    "@type": "WebSite",
    "@id": DOMAENE + "/#website",
    "url": DOMAENE + "/",
    "name": SITENAVN,
    "inLanguage": "da-DK",
    "publisher": {"@id": DOMAENE + "/#organisation"},
}


def graf(*noder):
    return {"@context": "https://schema.org", "@graph": list(noder)}


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


def artikelld(sti, titel, beskrivelse):
    return {
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
    }


def listeld(abonnementer, navn):
    poster = []
    for i, a in enumerate(abonnementer[:20], 1):
        u = UMAP[a["udbyder"]]
        poster.append({
            "@type": "ListItem", "position": i,
            "item": {
                "@type": "Product",
                "name": f"{u['navn']} — {a['navn']}",
                "brand": {"@type": "Brand", "name": u["navn"]},
                "category": "Mobilabonnement",
                "offers": {
                    "@type": "Offer",
                    "price": a["pris"],
                    "priceCurrency": "DKK",
                    "availability": "https://schema.org/InStock",
                    "url": DOMAENE + f"/udbydere/{u['slug']}/",
                },
            },
        })
    return {"@type": "ItemList", "name": navn, "numberOfItems": len(poster),
            "itemListElement": poster}


# --------------------------------------------------------------- komponenter

def logobaand(titel="Vi sammenligner priser fra"):
    logoer = "".join(
        f'<img src="/assets/img/logoer/{u["logo"]}" alt="{e(u["navn"])}" loading="lazy" height="30">'
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
        <h1>Find det <em>billigste mobilabonnement</em> i Danmark</h1>
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


def hero_side(etiket, h1, tekst, knapper=""):
    return f"""<section class="hero" style="padding:2.6rem 0 2.2rem">
  <div class="hero-net" aria-hidden="true"></div>
  <div class="baand">
    <div style="max-width:760px">
      <span class="etiket">{e(etiket)}</span>
      <h1>{h1}</h1>
      <p class="led">{tekst}</p>
      {f'<div class="hero-knapper" style="margin-top:1.3rem">{knapper}</div>' if knapper else ''}
    </div>
  </div>
</section>"""


def hurtigvalg():
    """Fire kort over tabellen — de mest søgte indgange."""
    billigste_fri = min(fri, key=lambda a: a["pris"]) if fri else ABON[0]
    daekning = next((a for a in ABON if a["udbyder"] == "yousee"), ABON[-1])
    udland = next((a for a in ABON if a["udbyder"] == "lebara"), ABON[0])

    valg = [
        ("Billigst i alt", billigst, "Laveste månedspris på markedet"),
        ("Bedst pris pr. GB", bedste_pr_gb, "Flest gigabyte for pengene"),
        ("Bedst dækning", daekning, "TDC NET — landets mest udbyggede"),
        ("Bedst til udlandet", udland, "Skarpe priser på udlandsopkald"),
    ]

    kort = ""
    for kat, a, detalje in valg:
        u = UMAP[a["udbyder"]]
        kort += f"""<a class="valgkort" href="/udbydere/{u['slug']}/">
  <div class="kat">{e(kat)}</div>
  <img class="logo-lille" src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])}" loading="lazy" height="20">
  <div class="navn">{e(a['navn'])}</div>
  <div class="detalje">{e(detalje)} · {gb_tekst(a['data_gb'])}</div>
  <div class="pris">{kr(a['pris'])}<span> kr./md.</span></div>
  <div class="pil">Se abonnementet →</div>
</a>"""

    return f'<div class="baand"><div class="hurtigvalg">{kort}</div></div>'


# --------------------------------------------------------------- FORSIDE

def byg_forside():
    sti = "/"
    titel = f"Billigste mobilabonnement {IDAG.year} — sammenlign priser | Telemobil"
    besk = (f"Sammenlign mobilabonnementer fra {D['antal_udbydere']} danske udbydere. "
            f"Priser fra {D['min_pris']} kr./md. Opdateret {OPDATERET}. Uafhængig og gratis.")

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

<section class="sektion sektion-nat">
  <div class="baand">
    <div class="sektion-hoved midt afslør">
      <span class="etiket">Kategorier</span>
      <h2>Find abonnementet efter dit behov</h2>
      <p class="led">Vi har lavet dedikerede sammenligninger til de mest almindelige situationer.</p>
    </div>
    <div class="kortgitter kg-4 afslør">
      <a class="kort kort-nat" href="/billigste-mobilabonnement/" style="text-decoration:none;color:inherit">
        <div class="ikon">💰</div><h3>Billigste abonnement</h3>
        <p>Hele markedet sorteret efter pris, med gennemgang af de skjulte omkostninger.</p></a>
      <a class="kort kort-nat" href="/mobilabonnement-med-fri-data/" style="text-decoration:none;color:inherit">
        <div class="ikon">∞</div><h3>Fri data</h3>
        <p>Hvad fri data koster — og hvorfor de fleste ikke har brug for det.</p></a>
      <a class="kort kort-nat" href="/mobilabonnement-til-unge/" style="text-decoration:none;color:inherit">
        <div class="ikon">🎓</div><h3>Unge og studerende</h3>
        <p>Meget data, lav pris og ingen binding, så du kan skifte når du flytter.</p></a>
      <a class="kort kort-nat" href="/mobilabonnement-uden-binding/" style="text-decoration:none;color:inherit">
        <div class="ikon">🔓</div><h3>Uden binding</h3>
        <p>Abonnementer du kan opsige med kort varsel, hvis behovet ændrer sig.</p></a>
    </div>
  </div>
</section>

{logobaand()}

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

{ctabaand("Klar til at spare på mobilregningen?",
          f"Den største forskel mellem det billigste og det dyreste abonnement i vores sammenligning er {kr(D['maks_besparelse'])} kr. om måneden. Det er {kr(D['maks_besparelse'] * 12)} kr. om året for et produkt, der kører på de samme master.")}

<section class="sektion baand-smal">
  {forfatterboks()}
  {afsloering()}
</section>
"""

    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_forside(), krumme=krumme,
        indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     listeld(ABON, "Mobilabonnementer i Danmark"))],
    ), prioritet="1.0", hyppighed="daily")


def udbyderkort(u):
    priser = [a["pris"] for a in ABON if a["udbyder"] == u["slug"]]
    fra = min(priser) if priser else None
    return f"""<a class="udbyderkort" href="/udbydere/{u['slug']}/">
  <img src="/assets/img/logoer/{u['logo']}" alt="{e(u['navn'])} logo" loading="lazy" height="30">
  <h3>{e(u['navn'])}</h3>
  <p>{e(u['kort'])}</p>
  <div class="fra">{'fra ' + kr(fra) + ' kr./md.' if fra else ''} <em>· {netlabel(u)}</em></div>
</a>"""


# --------------------------------------------------------------- BILLIGSTE

def byg_billigste():
    sti = "/billigste-mobilabonnement/"
    titel = f"Billigste mobilabonnement — fra {D['min_pris']} kr./md. {IDAG.year} | Telemobil"
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

<section class="sektion baand-smal">{gennemgangslinje(OPDATERET)}</section>

{indhold.billigste_brodtekst(D)}

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
        krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk),
                     listeld(ABON, "Billigste mobilabonnementer"))],
    ), prioritet="0.9", hyppighed="daily")


# --------------------------------------------------------------- FRI DATA

def byg_fridata():
    sti = "/mobilabonnement-med-fri-data/"
    titel = f"Mobilabonnement med fri data — fra {D['pris_fri']} kr./md. | Telemobil"
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

<section class="sektion baand-smal">{gennemgangslinje(OPDATERET)}</section>

{indhold.fridata_brodtekst(D)}

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
        krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk), listeld(udvalg, "Abonnementer med fri data"))],
    ), prioritet="0.9")


# --------------------------------------------------------------- NICHESIDER

def byg_niche(sti, etiket, h1, titel, besk, intro, udvalg, brodtekst, faq, links):
    krumme = [("/", "Forside"), (None, etiket)]
    krop = f"""
{pristabel(udvalg, UMAP, titel=f"Bedste valg — {etiket.lower()}", undertitel=intro,
           billigst_id=udvalg[0]['id'] if udvalg else None)}
<section class="sektion baand-smal">{gennemgangslinje(OPDATERET)}</section>
<section class="sektion baand-smal artikel">{brodtekst}</section>
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
        krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk), listeld(udvalg, etiket))],
    ), prioritet="0.8")


# --------------------------------------------------------------- UDBYDERE

def byg_udbyderoversigt():
    sti = "/udbydere/"
    titel = f"Mobilselskaber i Danmark — alle udbydere | Telemobil"
    besk = ("Uafhængig gennemgang af de danske mobilselskaber. Se netværk, priser, fordele "
            "og ulemper for hver udbyder.")
    krumme = [("/", "Forside"), (None, "Udbydere")]

    krop = f"""
<section class="sektion baand">
  <div class="sektion-hoved afslør">
    <span class="etiket">Oversigt</span>
    <h2>Alle udbydere i vores sammenligning</h2>
    <p class="led">Klik videre for priser, netværk, fordele og ulemper hos den enkelte udbyder.</p>
  </div>
  <div class="kortgitter kg-3">{"".join(udbyderkort(u) for u in UDBYDERE)}</div>
</section>

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET)}
  <h2>Sådan hænger det danske mobilmarked sammen</h2>
  <p>Der findes kun tre mobilnetværk i Danmark: TDC NET, Telenor og 3. Alle andre selskaber
  lejer sig ind hos en af de tre. Det betyder, at valget af udbyder i praksis er to
  beslutninger på én gang: hvilket <em>net</em> du vil køre på, og hvilket <em>selskab</em>
  du vil have som kunde hos.</p>
  <p>Nettet bestemmer din dækning og hastighed. Selskabet bestemmer din pris, din
  kundeservice og hvilke tillægsydelser du får. Et discountselskab på TDC NET giver dig
  altså samme dækning som et premiumselskab på samme net — til en anden pris og med en
  anden serviceoplevelse.</p>
  <table>
    <thead><tr><th>Udbyder</th><th>Netværk</th><th>Priser fra</th><th>Bedst til</th></tr></thead>
    <tbody>{"".join(oversigtsraekke(u) for u in UDBYDERE)}</tbody>
  </table>
  <div class="tip">
    <h3>Vores generelle råd</h3>
    <p>Bor du i en større by, kan du i praksis vælge frit mellem de tre net og bør vælge
    efter pris. Bor du på landet, i et sommerhusområde eller pendler gennem områder med
    svingende dækning, bør du vælge net før pris — og der står TDC NET historisk stærkest.</p>
  </div>
</section>

<section class="sektion baand-smal">
  {laesvidere([
      ("/billigste-mobilabonnement/", "Billigste mobilabonnement — hele markedet"),
      ("/guides/daekning-og-netvaerk/", "Dækning og netværk forklaret"),
      ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
  ])}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side("Udbydere", "Alle danske mobilselskaber",
                       "Vi gennemgår hver udbyder for sig — netværk, priser, fordele og "
                       "de ulemper, de selv undlader at nævne."),
        krumme=krumme, indhold=krop,
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme))],
    ), prioritet="0.8")


def oversigtsraekke(u):
    priser = [a["pris"] for a in ABON if a["udbyder"] == u["slug"]]
    fra = kr(min(priser)) + " kr." if priser else "—"
    return (f'<tr><td><a href="/udbydere/{u["slug"]}/"><strong>{e(u["navn"])}</strong></a></td>'
            f'<td>{e(u["netvaerk"])}</td><td>{fra}</td><td>{e(u["bedst_til"])}</td></tr>')


def byg_udbyder(u):
    sti = f"/udbydere/{u['slug']}/"
    egne = [a for a in ABON if a["udbyder"] == u["slug"]]
    fra = min(a["pris"] for a in egne) if egne else None
    titel = f"{u['navn']} anmeldelse {IDAG.year} — priser og netværk | Telemobil"
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

    krop = f"""
{tabel}

<section class="sektion baand-smal artikel">
  {gennemgangslinje(OPDATERET, f"Vilkår gennemgået på {u['navn']}s egen hjemmeside")}

  <h2>Vores vurdering af {e(u['navn'])}</h2>
  {afsnit}

  <div class="plusminus">
    <div class="pm pm-plus"><h3>Det taler for</h3><ul>{fordele}</ul></div>
    <div class="pm pm-minus"><h3>Det taler imod</h3><ul>{ulemper}</ul></div>
  </div>

  <h2>Netværk og dækning hos {e(u['navn'])}</h2>
  <p>{netafsnit}</p>
  <p>Bor du i en større by, er forskellen mellem de tre net lille i praksis. Bor du på
  landet, i et sommerhusområde eller pendler gennem tyndt befolkede områder, kan forskellen
  være mærkbar. Tjek altid dækningskortet på din egen adresse, før du bestiller.
  <a href="/guides/daekning-og-netvaerk/">Læs vores gennemgang af de tre netværk</a>.</p>

  <h2>Hvem passer {e(u['navn'])} til?</h2>
  <div class="kortgitter kg-2" style="margin:1.6rem 0">
    <div class="kort"><h3>Vælg {e(u['navn'])} hvis…</h3><p>{e(u['bedst_til'])}</p></div>
    <div class="kort"><h3>Vælg noget andet hvis…</h3><p>{e(u['daarligt_til'])}</p></div>
  </div>

  <h2>{e(u['navn'])} sammenlignet med alternativerne</h2>
  <p>Her er de abonnementer fra andre udbydere, der ligger tættest på
  {e(u['navn'])}s prisniveau. Bemærk især netværkskolonnen — det er der, den reelle forskel
  ofte ligger.</p>
  <table>
    <thead><tr><th>Abonnement</th><th>Data</th><th>Netværk</th><th>Pris/md.</th></tr></thead>
    <tbody>{sammenlign}</tbody>
  </table>
  <p>Se hele markedet i vores <a href="/billigste-mobilabonnement/">sammenligning af
  billigste mobilabonnement</a>.</p>

  <h2>Sådan skifter du til {e(u['navn'])}</h2>
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
      ("/udbydere/", f"Sammenlign {u['navn']} med de andre udbydere"),
      ("/guides/daekning-og-netvaerk/", "Hvilket netværk skal du vælge?"),
      ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab"),
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
        krumme=krumme, indhold=krop + faqblok(u["faq"], f"Spørgsmål om {u['navn']}"),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(u["faq"]),
                     artikelld(sti, titel, besk),
                     {"@type": "Organization", "name": u["navn"], "url": u["hjemmeside"],
                      "logo": DOMAENE + f"/assets/img/logoer/{u['logo']}"})],
    ), prioritet="0.8")


# --------------------------------------------------------------- GUIDES

def byg_guide(sti, etiket, h1, titel, besk, brodtekst, faq, links):
    krumme = [("/", "Forside"), ("/guides/", "Guides"), (None, etiket)]
    krop = f"""
<section class="sektion baand-smal">{gennemgangslinje(OPDATERET)}</section>
{brodtekst}
<section class="sektion baand-smal">
  {laesvidere(links)}
  {forfatterboks()}
  {afsloering()}
</section>
"""
    return skriv(sti, shell(
        sti=sti, titel=titel, beskrivelse=besk, opdateret=OPDATERET,
        hero=hero_side(etiket, h1, besk),
        krumme=krumme, indhold=krop + faqblok(faq),
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme), faqld(faq),
                     artikelld(sti, titel, besk))],
    ), prioritet="0.7")


def byg_guideoversigt():
    sti = "/guides/"
    krumme = [("/", "Forside"), (None, "Guides")]
    guides = [
        ("/guides/hvor-meget-data/", "Hvor meget data har jeg brug for?",
         "Find dit faktiske forbrug på to minutter, og se hvilket abonnement der matcher."),
        ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab",
         "Trin for trin — og de fem ting der oftest går galt undervejs."),
        ("/guides/daekning-og-netvaerk/", "Dækning og netværk i Danmark",
         "TDC NET, Telenor og 3 — hvem er stærkest hvor, og hvornår betyder det noget."),
        ("/guides/esim/", "eSIM forklaret",
         "Hvad et eSIM er, hvornår det er en fordel, og hvordan du kommer i gang."),
    ]
    kort = "".join(
        f'<a class="kort" href="{h}" style="text-decoration:none;color:inherit">'
        f'<h3>{e(t)}</h3><p>{e(b)}</p></a>' for h, t, b in guides)
    krop = f"""<section class="sektion baand">
  <div class="sektion-hoved afslør">
    <span class="etiket">Guides</span>
    <h2>Start her</h2>
    <p class="led">Fire guides, der dækker de spørgsmål vi oftest får. De tager hver et par
    minutter at læse og sparer typisk flere hundrede kroner om året.</p>
  </div>
  <div class="kortgitter kg-2">{kort}</div>
</section>

<section class="sektion baand-smal artikel">
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
</section>

<section class="sektion baand-smal">{forfatterboks()}{afsloering()}</section>"""
    return skriv(sti, shell(
        sti=sti, titel="Guides til mobilabonnement — Telemobil",
        beskrivelse="Praktiske guides om dataforbrug, netværk, eSIM og hvordan du skifter mobilselskab.",
        opdateret=OPDATERET,
        hero=hero_side("Guides", "Guides til mobilabonnement",
                       "Det du skal vide, før du vælger — skrevet i almindeligt dansk."),
        krumme=krumme, indhold=krop,
        jsonld=[graf(ORG, PERSON, WEBSITE, krummeld(krumme))],
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
        hero=hero_side(etiket, h1, besk), krumme=krumme, indhold=krop,
        jsonld=[graf(*noder)],
    ), prioritet=prioritet, hyppighed="monthly")


# --------------------------------------------------------------- FILER

def byg_sitemap():
    poster = ""
    for sti, pri, hyp in sider:
        poster += (f"  <url><loc>{DOMAENE}{sti}</loc><lastmod>{ISO}</lastmod>"
                   f"<changefreq>{hyp}</changefreq><priority>{pri}</priority></url>\n")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{poster}</urlset>\n")
    with open(os.path.join(ROD, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def byg_robots():
    txt = f"""User-agent: *
Allow: /
Disallow: /_build/

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
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
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
    html = shell(sti="/404.html", titel="Siden blev ikke fundet | Telemobil",
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
        f"Mobilabonnement til unge — fra {min(a['pris'] for a in unge)} kr. | Telemobil",
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
        f"Mobilabonnement uden binding — fra {min(a['pris'] for a in ubinding)} kr. | Telemobil",
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

    # Udbydere
    byg_udbyderoversigt()
    for u in UDBYDERE:
        byg_udbyder(u)

    # Guides
    byg_guideoversigt()
    byg_guide("/guides/skift-mobilselskab/", "Skift mobilselskab",
              "Sådan skifter du mobilselskab",
              f"Skift mobilselskab — behold dit nummer | Telemobil",
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
               ("/mobilabonnement-uden-binding/", "Abonnementer uden binding")])

    byg_guide("/guides/hvor-meget-data/", "Hvor meget data",
              "Hvor meget data har jeg brug for?",
              f"Hvor meget data har jeg brug for? Guide | Telemobil",
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
               ("/guides/daekning-og-netvaerk/", "Dækning og netværk")])

    byg_guide("/guides/daekning-og-netvaerk/", "Dækning og netværk",
              "Dækning og netværk i Danmark",
              f"Mobildækning i Danmark — TDC NET, Telenor og 3 | Telemobil",
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
               ("/guides/skift-mobilselskab/", "Sådan skifter du mobilselskab")])

    byg_guide("/guides/esim/", "eSIM", "eSIM forklaret",
              f"eSIM i Danmark — sådan virker det | Telemobil",
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
               ("/udbydere/", "Alle udbydere")])

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
                f"{FORFATTER['navn']} — stifter og redaktør | Telemobil",
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
  <a href="https://www.linkedin.com/in/emil-rostgaard-702809195/" rel="noopener nofollow" target="_blank">LinkedIn</a>.</p>
</section>"""
    byg_statisk("/kontakt/", "Kontakt Telemobil",
                "Kontakt Telemobil om faktuelle rettelser i priser, spørgsmål til vores sammenligninger eller henvendelser fra presse og udbydere.",
                "Kontakt", "Kontakt os", kontakt_krop, prioritet="0.4")

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
    byg_statisk("/privatlivspolitik/", "Privatliv og cookies | Telemobil",
                "Sådan behandler Telemobil cookies, affiliatesporing og personoplysninger.",
                "Privatliv", "Privatliv og cookies", privat_krop, prioritet="0.3")

    # Filer
    byg_404()
    byg_sitemap()
    byg_robots()
    byg_favicon()
    byg_htaccess()

    print(f"Byggede {len(sider)} sider.")
    print(f"  {D['antal']} abonnementer fra {D['antal_udbydere']} udbydere")
    print(f"  Billigste: {D['min_pris']} kr. — bedste pris pr. GB: {bedste_pr_gb['navn']}")
    if not site.get("data_verificeret"):
        print("\n  ADVARSEL: data_verificeret er false i data/site.json.")
        print("  Priser og netværksoplysninger er IKKE verificeret. Ret dem før lancering.")


if __name__ == "__main__":
    main()
