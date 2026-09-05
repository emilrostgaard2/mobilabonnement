#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Henter bredbåndsabonnementer fra Adtractions broadband-feed og skriver dem til
data/bredbaand.json.

Kør før build:
    python3 _build/bredbaand.py
    python3 _build/build.py

Undersøg feedet uden at skrive noget:
    python3 _build/bredbaand.py --inspect

Bredbåndsfeedet har helt andre felter end mobilfeedet: hastighed op og ned,
forbindelsestype og en 6-måneders totalpris i stedet for datamængde og taletid.
Derfor en selvstændig importør frem for et tilbygget hjørne på adtraction.py.
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
URL = f"https://api.adtraction.com/v3/public/data/{MARKED}/broadband?channelId={KANAL}"

# Feedet skriver forbindelsestypen forskelligt fra selskab til selskab:
# "5G", "5G internet", "Coax", "Kabel (COAX)". Uden normalisering ender
# samme teknologi i to grupper, og filtrene bliver ubrugelige.
TEKNOLOGI = {
    "fiber": "fiber",
    "coax": "coax", "kabel (coax)": "coax", "kabel": "coax",
    "5g": "5g", "5g internet": "5g",
    "4g": "4g", "4g internet": "4g",
    "dsl": "dsl", "adsl": "dsl", "vdsl": "dsl",
}

TEKNOLOGI_NAVN = {
    "fiber": "Fiber",
    "coax": "Coax",
    "5g": "5G",
    "4g": "4G",
    "dsl": "DSL",
}


def hent(url):
    if not KANAL:
        sys.exit("Sæt ADTRACTION_CHANNEL_ID før du kører importøren.")
    req = urllib.request.Request(url, headers={"User-Agent": "telemobil/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def slug(tekst):
    s = (tekst or "").lower().strip()
    s = re.sub(r"\s+dk$", "", s)
    s = s.replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def tal(v, standard=0):
    try:
        return int(round(float(v)))
    except (TypeError, ValueError):
        return standard


def teknologi(post):
    raa = (post.get("connection") or "").strip().lower()
    return TEKNOLOGI.get(raa, re.sub(r"[^a-z0-9]+", "-", raa).strip("-") or "andet")


def kampagnemaaneder(post):
    """Hvor længe tilbudsprisen løber. Feedet har det kun i fritekst.

    Formuleringerne varierer: "99 kr/md første 3 mdr", "Spar 100 kr/md i 6 mdr",
    "25 % rabat i 6 mdr". Genkender vi ikke teksten, antager vi 6 måneder,
    fordi feedets egne totalpriser regnes over netop 6 måneder."""
    t = post.get("promotion") or ""
    m = re.search(r"(?:første|i)\s+(\d+)\s*mdr", t, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*(?:mdr|måneder)", t, re.I)
    if m:
        return int(m.group(1))
    return 6 if post.get("discountPriceFrom") else 0


def oversaet(post, i):
    navn = (post.get("unitName") or post.get("provider") or "").strip()
    if not navn:
        return None, "mangler selskabsnavn"

    normal = tal(post.get("priceFrom"))
    if normal <= 0:
        return None, f"ingen månedspris (uniqueId {post.get('uniqueId')})"

    intro = tal(post.get("discountPriceFrom"), 0) or None
    if intro and intro >= normal:
        intro = None
    mdr = kampagnemaaneder(post) if intro else 0

    ned = tal(post.get("speedDownloadMB"))
    op = tal(post.get("speedUploadMB"))
    oprettelse = tal(post.get("initialFee"))

    # Feedets egne totalpriser over seks måneder. Vi bruger dem frem for selv
    # at gange, fordi de er annoncørens egne tal — og fordi de nogle steder
    # også dækker fragt og oprettelse.
    seks = tal(post.get("price6Month")) or None
    seks_tilbud = tal(post.get("discountPrice6Month")) or None

    usper = [post.get(f"usp{n}") for n in (1, 2, 3)]
    usper = [u.strip() for u in usper if u and u.strip()]

    return {
        "id": f"bb-{post.get('uniqueId') or i}",
        "udbyder": slug(navn),
        "udbyder_navn": navn if navn.lower() != "yousee" else "YouSee",
        "navn": (post.get("campaign") or "").strip() or "Bredbånd",
        "teknologi": teknologi(post),
        "ned": ned,
        "op": op,
        "pris": normal,
        "intro_pris": intro,
        "intro_mdr": mdr,
        "oprettelse": oprettelse,
        "binding": tal(post.get("bindingMonth")),
        "seks_maaneder": seks,
        "seks_maaneder_tilbud": seks_tilbud,
        "net": (post.get("provider") or "").strip(),
        "fordele": usper,
        "kampagnetekst": (post.get("promotion") or "").strip() or None,
        "logo_url": post.get("logoUrl"),
        "link": post.get("trackingURL"),
    }, None


def main():
    data = hent(URL)
    enheder = data.get("units", [])

    if "--inspect" in sys.argv:
        print(f"{len(enheder)} enheder i broadband-feedet\n")
        felter = {}
        for p in enheder:
            for k, v in p.items():
                felter.setdefault(k, set()).add(type(v).__name__)
        print("Felter:")
        for k in sorted(felter):
            print(f"   {k:24} {', '.join(sorted(felter[k]))}")
        print("\nForbindelsestyper i feedet:")
        for c in sorted({(p.get("connection") or "?") for p in enheder}):
            print(f"   {c!r}  →  {TEKNOLOGI.get(c.strip().lower(), 'ukendt')}")
        return

    ud, fejl = [], []
    for i, p in enumerate(enheder):
        a, f = oversaet(p, i)
        (ud.append(a) if a else fejl.append(f))

    ud.sort(key=lambda a: (a["intro_pris"] or a["pris"]))
    sti = os.path.join(ROD, "data", "bredbaand.json")
    with open(sti, "w", encoding="utf-8") as f:
        json.dump({"hentet": date.today().isoformat(), "abonnementer": ud},
                  f, ensure_ascii=False, indent=1)

    fra = {}
    for a in ud:
        fra.setdefault(a["teknologi"], []).append(a)
    print(f"Bredbånd: {len(ud)} produkter fra "
          f"{len({a['udbyder'] for a in ud})} selskaber")
    for t in sorted(fra, key=lambda x: -len(fra[x])):
        priser = [a["pris"] for a in fra[t]]
        print(f"   {TEKNOLOGI_NAVN.get(t, t):8} {len(fra[t]):>2} produkter, "
              f"fra {min(priser)} kr.")
    if fejl:
        print(f"\n{len(fejl)} kasseret:")
        for f in fejl[:5]:
            print("   ", f)


if __name__ == "__main__":
    main()
