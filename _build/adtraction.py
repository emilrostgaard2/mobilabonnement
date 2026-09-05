#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Henter mobilabonnementer fra Adtractions data feed og skriver dem til
data/abonnementer.json i det format, build.py forventer.

Kør før build:
    python3 _build/adtraction.py
    python3 _build/build.py

Eller undersøg feedets struktur uden at skrive noget:
    python3 _build/adtraction.py --inspect

Miljøvariabler (sæt dem som GitHub Secrets, ikke i koden):
    ADTRACTION_CHANNEL_ID   din kanal-id
    ADTRACTION_MARKED       landekode, standard "dk"
    ADTRACTION_FEED         feednavn, standard "mobile"
"""

import json
import os
import re
import sys
import urllib.request
from datetime import date

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KANAL = os.environ.get("ADTRACTION_CHANNEL_ID", "")
MARKED = os.environ.get("ADTRACTION_MARKED", "dk")
FEED = os.environ.get("ADTRACTION_FEED", "mobile")
URL = f"https://api.adtraction.com/v3/public/data/{MARKED}/{FEED}?channelId={KANAL}"

# Kortlægning fra Adtractions annoncørnavne til vores udbyder-slugs.
# Venstre side skal matche feedets navn i små bogstaver uden " DK".
UDBYDER_KORT = {
    "cbb mobil": "cbb-mobil", "cbb": "cbb-mobil",
    "yousee": "yousee",
    "telmore": "telmore",
    "oister": "oister", "oister dk": "oister",
    "lebara": "lebara",
    "greentel": "greentel",
    "duka": "duka",
    "lyca mobile": "lyca-mobile", "lycamobile": "lyca-mobile",
    "eesy": "eesy",
    "flexii": "flexii",
}


def hent(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "telemobil.dk feed-import",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------- oversæt

def tal(v, standard=0):
    if v is None:
        return standard
    if isinstance(v, bool):
        return standard
    if isinstance(v, (int, float)):
        return int(round(v))
    m = re.search(r"[\d.,]+", str(v).replace(".", "").replace(",", "."))
    return int(round(float(m.group()))) if m else standard


def slug(navn):
    """Oversætter 'Flexii DK' til vores udbyder-slug."""
    s = re.sub(r"\s+dk$", "", (navn or "").lower().strip())
    if s in UDBYDER_KORT:
        return UDBYDER_KORT[s]
    for k, v in UDBYDER_KORT.items():
        if k in s:
            return v
    return None


def introperiode(post):
    """Udleder introprisens længde. Feedet har den kun i promotionText.

    Udbyderne formulerer sig vidt forskelligt: "første 3 mdr", "i 6 måneder",
    "første ÅR", "første md.". Genkender vi ikke formuleringen, kasseres
    tilbuddet, og siden viser normalprisen — altså går vi glip af kampagnen.
    Derfor dækker vi alle de former, feedet faktisk indeholder."""
    t = post.get("promotionText") or ""

    # "første ÅR", "resten af året", "frem til 31.3.2027" → tolv måneder
    if re.search(r"(første|hele)\s*(1\s*)?år\b", t, re.I):
        return 12
    if re.search(r"resten af året", t, re.I):
        return 12
    if re.search(r"frem til\s+\d", t, re.I):
        return 12

    # "første md.", "første måned" uden tal → én måned
    if re.search(r"første\s+(md\.?|måned)\b", t, re.I):
        return 1

    m = re.search(r"første\s+(\d+)\s*(mdr|måned)", t, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"i\s+(\d+)\s*(mdr|måned)", t, re.I)
    if m:
        return int(m.group(1))
    # "20 % rabat i 6 måneder" fanges ovenfor; "Prisrabat i 3 måneder" ligeså
    m = re.search(r"(\d+)\s*(mdr|måneder)", t, re.I)
    if m:
        return int(m.group(1))
    return 0


def inkluderet(post):
    """Hvad der følger med ud over tale og data.

    Feedet siger kun ja/nej — ikke hvilke tjenester. Vi skriver derfor det,
    feedet faktisk oplyser, og opfinder ikke navne som Netflix eller HBO.
    Bemærk at nøglen "audioBooks " har et mellemrum til sidst i feedet."""
    ud = []
    if post.get("streaming"):
        # usp1 er typisk "3 valgfrie streamingtjenester" — mere præcist end et flag
        u = (post.get("usp1") or "").strip()
        ud.append(u if "streaming" in u.lower() else "Streaming inkluderet")
    if post.get("music"):
        ud.append("Musik")
    if post.get("audioBooks") or post.get("audioBooks "):
        ud.append("Lydbøger")
    return ud


# Markering for ubegrænset data. Skal ligge over enhver reel datamængde —
# Duka sælger fx et abonnement med 1000 GB, og det er IKKE fri data.
UBEGRAENSET = 9999


def datamaengde(post, felt, ubegraenset_felt):
    if post.get(ubegraenset_felt):
        return UBEGRAENSET
    v = post.get(felt)
    return tal(v, 0) if v is not None else 0


def taletid(post):
    if post.get("unlimitedHoursDK"):
        return "fri"
    t = post.get("hoursIncludedDK")
    if t:
        return f"{tal(t)} timer"
    return "fri"


def navngiv(post, data_dk):
    """Feedet har ikke produktnavne — vi bygger et beskrivende et."""
    u = post.get("unitName") or "Abonnement"
    if data_dk >= 900:
        return f"{u} Fri Data"
    if data_dk == 0:
        return f"{u} Tale"
    return f"{u} {data_dk} GB"


def oversaet(post, i):
    u = slug(post.get("programName"))
    if not u:
        return None, f"ukendt udbyder: {post.get('programName')!r}"

    normal = tal(post.get("monthlyPrice"))
    if normal <= 0:
        return None, f"ingen månedspris (uniqueId {post.get('uniqueId')})"

    intro = tal(post.get("discountPrice"), 0) or None
    mdr = introperiode(post) if intro else 0
    if intro and (intro >= normal or not mdr):
        # Uden en kendt periode kan vi ikke regne 12-måneders-prisen ærligt
        intro, mdr = None, 0

    data_dk = datamaengde(post, "dataDK", "unlimitedDataDK")
    data_eu = datamaengde(post, "dataEU", "unlimitedDataEU")

    link = post.get("trackingURL")
    if not link:
        return None, f"intet sporingslink (uniqueId {post.get('uniqueId')})"

    return {
        "id": f"{u}-{post.get('uniqueId')}",
        "udbyder": u,
        "navn": navngiv(post, data_dk),
        "data_gb": data_dk,
        "pris": normal,
        "intro_pris": intro,
        "intro_mdr": mdr,
        "tale": taletid(post),
        "sms": "fri" if post.get("unlimitedSMS") else "begrænset",
        "binding": tal(post.get("minimumSubscriptionPeriod"), 0),
        "oprettelse": tal(post.get("initialFee"), 0),
        "eu_gb": data_eu,
        "femg": bool(post.get("5g")),
        "esim": bool(post.get("eSim")),
        "streaming": inkluderet(post),
        "forbrugsafregnet": False,
        "badge": None,
        "link": link,
        # Feedets egne oplysninger, som vi bruger andre steder
        "_net": post.get("operatorNetwork"),
        "_usp": [post.get(f"usp{n}") for n in (1, 2, 3) if post.get(f"usp{n}")],
        "_kampagnetekst": post.get("promotionText"),
    }, None


# Feedets netværksnavne oversat til vores
NET_KORT = {
    "3": "3",
    "tdc": "TDC NET",
    "tdc net": "TDC NET",
    "telenor": "Telenor",
    "norlys/telenor": "Telenor",
    "telia": "Telia",
    "telia/telenor": "Telenor",
}


def opdater_netvaerk(abonnementer):
    """Feedet oplyser hvilket net hver udbyder kører på — brug det."""
    sti = os.path.join(ROD, "data", "udbydere.json")
    d = json.load(open(sti, encoding="utf-8"))
    fundet = {}
    for a in abonnementer:
        n = (a.get("_net") or "").strip().lower()
        if n in NET_KORT:
            fundet[a["udbyder"]] = NET_KORT[n]
    aendret = []
    for u in d["udbydere"]:
        nyt = fundet.get(u["slug"])
        if nyt and u["netvaerk"] != nyt:
            aendret.append(f"{u['navn']}: {u['netvaerk']} -> {nyt}")
            u["netvaerk"] = nyt
    if aendret:
        json.dump(d, open(sti, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return aendret


def udpak(raa):
    if isinstance(raa, list):
        return raa
    for n in ("units", "products", "data", "items"):
        if isinstance(raa.get(n), list):
            return raa[n]
    return []


def inspect(raa):
    poster = udpak(raa)
    print(f"Feedet indeholder {len(poster)} poster.\n")
    if not poster:
        print("Rå struktur:", json.dumps(raa, ensure_ascii=False)[:1500])
        return
    print("Feltnavne i første post:")
    for k, v in poster[0].items():
        vis = str(v)[:70].replace("\n", " ")
        print(f"  {k:28} {vis}")
    print("\nFørste post som JSON:")
    print(json.dumps(poster[0], ensure_ascii=False, indent=1)[:2000])



def gem_historik(abonnementer):
    """Tilføjer et dagligt øjebliksbillede til data/prishistorik.json.

    Vi gemmer aggregerede tal, ikke hele datasættet — filen skal kunne vokse i
    årevis uden at fylde. Én linje pr. dag; køres importøren flere gange samme
    dag, overskrives dagens post."""
    sti = os.path.join(ROD, "data", "prishistorik.json")
    try:
        with open(sti, encoding="utf-8") as f:
            historik = json.load(f)
    except (FileNotFoundError, ValueError):
        historik = {"maalinger": []}

    # Samme skelnen som resten af sitet: kun UBEGRAENSET er fri data.
    # Dukas 1000 GB har et loft og hører i "201+", ikke i "fri".
    grupper = [("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40),
               ("41-80", 41, 80), ("81-200", 81, 200),
               ("201+", 201, UBEGRAENSET - 1), ("fri", UBEGRAENSET, UBEGRAENSET)]
    betalte = [a for a in abonnementer if a.get("pris", 0) > 0]
    maaling = {"dato": date.today().isoformat(), "antal": len(betalte),
               "udbydere": len({a["udbyder"] for a in betalte}),
               "grupper": {}, "pr_udbyder": {}}

    # Prisen på hvert enkelt abonnement. Det er dét, der gør det muligt at
    # skrive "Duka 10 GB faldt fra 59 til 49 kr. i går" — en oplysning ingen
    # konkurrent kan give, fordi ingen andre gemmer historik.
    # 56 heltal pr. måling fylder under 1 KB.
    maaling["priser"] = {a["id"]: a["pris"] for a in betalte}

    # Pr. udbyder gemmes også. Det gør det muligt at skrive "Telmores priser er
    # steget 8 % siden august" på selskabssiden — noget ingen konkurrent kan,
    # fordi ingen andre gemmer historik. Fire tal pr. selskab fylder intet.
    for slug in sorted({a["udbyder"] for a in betalte}):
        p_u = sorted(a["pris"] for a in betalte if a["udbyder"] == slug)
        if not p_u:
            continue
        m = len(p_u)
        maaling["pr_udbyder"][slug] = {
            "antal": m,
            "min": p_u[0],
            "median": round(p_u[m // 2] if m % 2
                            else (p_u[m // 2 - 1] + p_u[m // 2]) / 2, 2),
            "maks": p_u[-1],
        }
    for navn, lav, hoej in grupper:
        priser = sorted(a["pris"] for a in betalte if lav <= a["data_gb"] <= hoej)
        if not priser:
            continue
        n = len(priser)
        maaling["grupper"][navn] = {
            "antal": n,
            "min": priser[0],
            "median": round(priser[n // 2] if n % 2
                            else (priser[n // 2 - 1] + priser[n // 2]) / 2, 2),
            "gns": round(sum(priser) / n, 2),
            "maks": priser[-1],
        }

    historik["maalinger"] = [m for m in historik["maalinger"]
                             if m["dato"] != maaling["dato"]]
    historik["maalinger"].append(maaling)
    historik["maalinger"].sort(key=lambda m: m["dato"])
    with open(sti, "w", encoding="utf-8") as f:
        json.dump(historik, f, ensure_ascii=False, indent=1)
    print(f"\nPrishistorik: {len(historik['maalinger'])} målinger gemt "
          f"({historik['maalinger'][0]['dato']} til {maaling['dato']})")


def main():
    if not KANAL:
        sys.exit("ADTRACTION_CHANNEL_ID er ikke sat. Sæt den som miljøvariabel.")

    print(f"Henter {URL.replace(KANAL, '***')}")
    raa = hent(URL)

    if "--inspect" in sys.argv:
        inspect(raa)
        return

    poster = udpak(raa)
    abonnementer, sprunget = [], []
    for i, p in enumerate(poster):
        rk, grund = oversaet(p, i)
        if rk:
            abonnementer.append(rk)
        else:
            sprunget.append(grund)

    if not abonnementer:
        sys.exit("Ingen abonnementer kunne oversættes. Kør med --inspect og ret "
                 "feltnavnene i oversaet().")

    abonnementer.sort(key=lambda a: a["pris"])
    ud = {
        "_kilde": "Adtraction data feed",
        "_hentet": date.today().isoformat(),
        "_advarsel": ("Genereret automatisk af _build/adtraction.py ved hvert build. "
                      "Redigér ikke i hånden, og overskriv ikke filen med en ældre "
                      "version — så mister du de nyeste priser."),
        "kilde": "adtraction",
        "opdateret": date.today().isoformat(),
        "abonnementer": abonnementer,
    }
    sti = os.path.join(ROD, "data", "abonnementer.json")
    with open(sti, "w", encoding="utf-8") as f:
        json.dump(ud, f, ensure_ascii=False, indent=1)

    net_aendret = opdater_netvaerk(abonnementer)
    for a in abonnementer:
        for k in ("_net", "_usp", "_kampagnetekst"):
            a.pop(k, None)
    with open(sti, "w", encoding="utf-8") as f:
        json.dump(ud, f, ensure_ascii=False, indent=1)

    print(f"\nSkrev {len(abonnementer)} abonnementer til data/abonnementer.json")
    gem_historik(abonnementer)
    if net_aendret:
        print("\nNetværk opdateret fra feedet:")
        for x in net_aendret:
            print("  ", x)
    udbydere = {}
    for a in abonnementer:
        udbydere[a["udbyder"]] = udbydere.get(a["udbyder"], 0) + 1
    for u, n in sorted(udbydere.items()):
        print(f"  {u:14} {n}")
    if sprunget:
        print(f"\nSprunget over ({len(sprunget)}):")
        for s in sorted(set(sprunget))[:12]:
            print("  -", s)

    # Sæt verificeringsflaget, når data kommer fra en rigtig kilde
    site_sti = os.path.join(ROD, "data", "site.json")
    site = json.load(open(site_sti, encoding="utf-8"))
    site["data_verificeret"] = True
    site["priskilde"] = "Adtraction data feed"
    json.dump(site, open(site_sti, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\ndata_verificeret sat til true i site.json")


if __name__ == "__main__":
    main()
