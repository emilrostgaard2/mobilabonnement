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
    """Udleder introprisens længde. Feedet har den kun i promotionText."""
    t = post.get("promotionText") or ""
    m = re.search(r"første\s+(\d+)\s*(mdr|måned)", t, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"i\s+(\d+)\s*(mdr|måned)", t, re.I)
    if m:
        return int(m.group(1))
    return 0


def datamaengde(post, felt, ubegraenset_felt):
    if post.get(ubegraenset_felt):
        return 999
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
        "streaming": [],
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
        "_advarsel": ("Genereret automatisk. Redigér ikke i hånden — kør "
                      "_build/adtraction.py i stedet."),
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
