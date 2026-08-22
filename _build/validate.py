# -*- coding: utf-8 -*-
"""Validerer det byggede site. Fejl stopper deploy; advarsler gør ikke.

Kør fra projektroden:  python3 _build/validate.py
"""

import os
import re
import sys
import glob
import json
from html.parser import HTMLParser

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRING = {".git", ".github", "_build", "data", "assets", "node_modules"}

fejl = []
advarsler = []


class Sideparser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titel = ""
        self.i_titel = False
        self.beskrivelse = ""
        self.kanonisk = ""
        self.h1 = []
        self.i_h1 = False
        self.billeder = []
        self.links = []
        self.jsonld = []
        self.i_jsonld = False
        self.h_niveauer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.i_titel = True
        elif tag == "meta":
            if a.get("name") == "description":
                self.beskrivelse = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.kanonisk = a.get("href", "")
        elif tag == "h1":
            self.i_h1 = True
            self.h_niveauer.append(1)
        elif tag in ("h2", "h3", "h4"):
            self.h_niveauer.append(int(tag[1]))
        elif tag == "img":
            self.billeder.append(a)
        elif tag == "a" and a.get("href"):
            self.links.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self.i_jsonld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.i_titel = False
        elif tag == "h1":
            self.i_h1 = False
        elif tag == "script":
            self.i_jsonld = False

    def handle_data(self, d):
        if self.i_titel:
            self.titel += d
        if self.i_h1:
            self.h1.append(d)
        if self.i_jsonld:
            self.jsonld.append(d)


def find_sider():
    for rod, mapper, filer in os.walk(ROD):
        mapper[:] = [m for m in mapper if m not in SPRING and not m.startswith(".")]
        for f in filer:
            if f.endswith(".html"):
                yield os.path.join(rod, f)


def url_af(filsti):
    rel = os.path.relpath(filsti, ROD)
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def ordantal(html):
    tekst = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    tekst = re.sub(r"<style.*?</style>", " ", tekst, flags=re.S)
    tekst = re.sub(r"<[^>]+>", " ", tekst)
    return len(tekst.split())


def main():
    sider = sorted(find_sider())
    if not sider:
        fejl.append("Ingen HTML-sider fundet — kørte build.py?")
        return rapporter()

    kendte = set()
    for s in sider:
        kendte.add(url_af(s))

    titler = {}
    beskrivelser = {}
    rapport = []

    for filsti in sider:
        url = url_af(filsti)
        with open(filsti, encoding="utf-8") as f:
            html = f.read()

        p = Sideparser()
        p.feed(html)
        titel = p.titel.strip()
        ord_ = ordantal(html)
        rapport.append((url, len(titel), len(p.beskrivelse), ord_))

        # Titel
        if not titel:
            fejl.append(f"{url}: mangler <title>")
        elif len(titel) > 65:
            advarsler.append(f"{url}: titel er {len(titel)} tegn (over 65 kan blive afkortet)")
        if titel in titler:
            fejl.append(f"{url}: samme titel som {titler[titel]}")
        titler[titel] = url

        # Beskrivelse
        if not p.beskrivelse:
            fejl.append(f"{url}: mangler meta description")
        elif not (70 <= len(p.beskrivelse) <= 165):
            advarsler.append(f"{url}: meta description er {len(p.beskrivelse)} tegn (sigt efter 70-165)")
        if p.beskrivelse in beskrivelser:
            fejl.append(f"{url}: samme meta description som {beskrivelser[p.beskrivelse]}")
        beskrivelser[p.beskrivelse] = url

        # Kanonisk
        if not p.kanonisk:
            fejl.append(f"{url}: mangler canonical")

        # H1
        if len(p.h1) == 0 and not url.endswith("404.html"):
            fejl.append(f"{url}: mangler H1")

        # Overskriftshierarki — spring på mere end ét niveau
        forrige = None
        for n in p.h_niveauer:
            if forrige and n > forrige + 1:
                advarsler.append(f"{url}: overskrift springer fra h{forrige} til h{n}")
                break
            forrige = n

        # Billeder uden alt
        for b in p.billeder:
            if "alt" not in b:
                fejl.append(f"{url}: <img src={b.get('src')}> mangler alt-tekst")

        # Interne links
        for a in p.links:
            href = a["href"]
            if href.startswith(("http", "mailto:", "tel:", "#")):
                if href.startswith("http") and "telemobil.dk" not in href:
                    rel = a.get("rel", "")
                    if "nofollow" not in rel and "sponsored" not in rel:
                        advarsler.append(f"{url}: eksternt link uden rel-attribut: {href}")
                continue
            maal = href.split("#")[0].split("?")[0]
            if maal and maal not in kendte and not maal.startswith("/assets/"):
                if not os.path.exists(os.path.join(ROD, maal.strip("/"))):
                    fejl.append(f"{url}: dødt internt link → {maal}")

        # JSON-LD
        if not p.jsonld and not url.endswith("404.html"):
            advarsler.append(f"{url}: ingen JSON-LD struktureret data")
        for blok in p.jsonld:
            try:
                json.loads(blok)
            except json.JSONDecodeError as ex:
                fejl.append(f"{url}: ugyldig JSON-LD ({ex})")

        # Indholdslængde
        if ord_ < 350 and url not in ("/404.html", "/kontakt/"):
            advarsler.append(f"{url}: kun {ord_} ord")

    # Nødvendige filer
    for f in ("sitemap.xml", "robots.txt", "favicon.svg", ".htaccess", "404.html"):
        if not os.path.exists(os.path.join(ROD, f)):
            fejl.append(f"Mangler fil: {f}")

    # Sitemap-dækning
    smsti = os.path.join(ROD, "sitemap.xml")
    if os.path.exists(smsti):
        with open(smsti, encoding="utf-8") as f:
            sm = f.read()
        for u in kendte:
            if u == "/404.html":
                continue
            if f"<loc>https://telemobil.dk{u}</loc>" not in sm:
                advarsler.append(f"{u}: ikke med i sitemap.xml")

    # Prisløfter i titel og beskrivelse skal kunne findes i prisdata.
    # "fra 0 kr./md." opstår, når en kategori ikke har nogen abonnementer —
    # og et forkert prisløfte i søgeresultatet er værre end ingen pris.
    with open(os.path.join(ROD, "data", "abonnementer.json"), encoding="utf-8") as f:
        _ab = json.load(f)["abonnementer"]
    _gyldige = {a["pris"] for a in _ab if a.get("pris")}
    _gyldige |= {a["intro_pris"] for a in _ab if a.get("intro_pris")}
    _laveste = min(_gyldige) if _gyldige else 0
    for sti_html in sorted(glob.glob(os.path.join(ROD, "**", "index.html"), recursive=True)):
        _h = open(sti_html, encoding="utf-8").read()
        _url = "/" + os.path.relpath(sti_html, ROD).replace("index.html", "")
        _t = re.search(r"<title>(.*?)</title>", _h, re.S)
        _d = re.search(r'name="description" content="(.*?)"', _h, re.S)
        for _felt, _tekst in (("titel", _t.group(1) if _t else ""),
                              ("beskrivelse", _d.group(1) if _d else "")):
            for _tal in re.findall(r"\b(\d{1,4}) kr", _tekst):
                _n = int(_tal)
                if _n == 0:
                    fejl.append(f"{_url}: {_felt} lover 0 kr. — kategorien har "
                                f"ingen abonnementer")
                elif _n < _laveste:
                    fejl.append(f"{_url}: {_felt} lover {_n} kr., men laveste "
                                f"pris i data er {_laveste} kr.")

    # Verificeringsflag
    with open(os.path.join(ROD, "data", "site.json"), encoding="utf-8") as f:
        site = json.load(f)
    if not site.get("data_verificeret"):
        advarsler.append("data_verificeret er false — priser og netværk er ikke kontrolleret")

    # Oversigt
    print(f"\n{'URL':<42}{'Titel':>7}{'Beskr.':>8}{'Ord':>7}")
    print("-" * 64)
    for url, lt, lb, ord_ in sorted(rapport):
        print(f"{url:<42}{lt:>7}{lb:>8}{ord_:>7}")
    print("-" * 64)
    print(f"{len(rapport)} sider, {sum(r[3] for r in rapport):,} ord i alt".replace(",", "."))

    return rapporter()


def rapporter():
    if advarsler:
        print(f"\n{len(advarsler)} advarsler:")
        for a in advarsler:
            print(f"  ! {a}")
    if fejl:
        print(f"\n{len(fejl)} FEJL:")
        for f in fejl:
            print(f"  x {f}")
        sys.exit(1)
    print("\nValidering OK.")
    return 0


if __name__ == "__main__":
    main()
