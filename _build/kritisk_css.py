#!/usr/bin/env python3
"""Beregner kritisk CSS pr. sidetype med Chromium (Playwright).

Kører lokalt, ikke i workflowet. Resultatet gemmes i assets/css/kritisk/ og
committes. Byg sitet først (så siderne findes), start en lokal server, og kør:

    python3 -m http.server 8765 &   # i repo-roden
    python3 _build/kritisk_css.py

Hver sidetype får de CSS-regler, dens repræsentative sider faktisk bruger på
mobil og desktop. Resten af stylesheetet hentes asynkront og caches."""
import json
import os
from playwright.sync_api import sync_playwright

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import re


def minificer_css(css):
    """Samme minificering som i build.py — offsets skal passe på tegnet."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>~])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


CSS_MIN = minificer_css(open(os.path.join(ROD, "assets", "css", "telemobil.css"),
                             encoding="utf-8").read())
CSS = CSS_MIN


def at_blokke(css):
    """Finder @media/@supports-blokke: (start, indhold_start, slut, prelude)."""
    ud = []
    for m in re.finditer(r"@(media|supports)[^{]*\{", css):
        dybde, i = 1, m.end()
        while i < len(css) and dybde:
            if css[i] == "{":
                dybde += 1
            elif css[i] == "}":
                dybde -= 1
            i += 1
        ud.append((m.start(), m.end(), i, css[m.start():m.end() - 1]))
    return ud


def altid_med(css):
    """@font-face og @keyframes rapporteres ikke som brugte — tag dem altid med."""
    ud = []
    for m in re.finditer(r"@(?:font-face|(?:-webkit-)?keyframes)[^{]*\{", css):
        dybde, i = 1, m.end()
        while i < len(css) and dybde:
            if css[i] == "{":
                dybde += 1
            elif css[i] == "}":
                dybde -= 1
            i += 1
        ud.append(css[m.start():i])
    return ud
UD = os.path.join(ROD, "assets", "css", "kritisk")
BASE = "http://localhost:8765"

TYPER = {
    "forside": ["/"],
    "kategori": ["/billigste-mobilabonnement/", "/mobilabonnement-med-fri-data/",
                 "/mobilabonnement-10-30-gb/", "/mobilabonnement-til-boern/",
                 "/bedste-mobilabonnement/", "/mobilabonnement-med-netflix/",
                 "/mobilabonnement-med-streaming/", "/taletidskort/"],
    "udbyder": ["/udbydere/oister/", "/udbydere/eesy/", "/udbydere/yousee/", "/udbydere/"],
    "guide": ["/guides/mistet-telefon/", "/guides/esim/", "/guides/hvor-meget-data/",
              "/guides/", "/guides/skift-mobilselskab/", "/mobilabonnement-til-familie/"],
    "bredbaand": ["/bredbaand/", "/bredbaand/fibernet/", "/bredbaand/5g/"],
    "sammenlign": ["/sammenlign/", "/sammenlign/telmore-vs-yousee/"],
    "kampagner": ["/kampagner/", "/mobilabonnementer-black-friday/"],
    "data": ["/prisarkiv/", "/prisudvikling/", "/aabne-data/", "/12-maaneders-prisen/"],
    "vaerktoej": ["/speedtest/", "/daekningskort/", "/landekoder/", "/hvem-ringer-til-mig/",
                  "/ordbog/", "/pin-og-puk-kode/", "/netvaerk/", "/driftsstatus/"],
    "statisk": ["/om/", "/metode/", "/kontakt/", "/om/emil-rostgaard/", "/presse/",
                "/privatlivspolitik/", "/404.html"],
}


def brugt(page, url, ranges):
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    cdp.send("CSS.startRuleUsageTracking")
    page.goto(BASE + url, wait_until="load")
    page.wait_for_timeout(400)
    res = cdp.send("CSS.stopRuleUsageTracking")
    tekster = {}
    for r in res["ruleUsage"]:
        if not r["used"]:
            continue
        sid = r["styleSheetId"]
        if sid not in tekster:
            try:
                tekster[sid] = cdp.send("CSS.getStyleSheetText", {"styleSheetId": sid})["text"]
            except Exception:
                tekster[sid] = ""
        if tekster[sid][:60] == CSS_MIN[:60]:
            ranges.add((int(r["startOffset"]), int(r["endOffset"])))
    cdp.detach()


def main():
    os.makedirs(UD, exist_ok=True)
    stat = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for typ, urls in TYPER.items():
            ranges = set()
            for vw in ({"width": 390, "height": 844}, {"width": 1280, "height": 900}):
                page = b.new_page(viewport=vw)
                for u in urls:
                    try:
                        brugt(page, u, ranges)
                    except Exception as ex:
                        print("  springer", u, ex)
                page.close()
            blokke = at_blokke(CSS)
            # Bevar kildens rækkefølge, så cascaden er den samme som i fuld CSS.
            dele = altid_med(CSS)
            aaben = None
            for s_, e_ in sorted(ranges):
                tekst = CSS[s_:e_]
                if not tekst.strip() or "{" not in tekst:
                    continue
                noegle, drop = "", False
                for bs, bi, be, prelude in blokke:
                    if s_ < bi and e_ > bs:
                        drop = True
                        break
                    if bi <= s_ and e_ <= be:
                        noegle = (bs, prelude)
                        break
                if drop:
                    continue
                if noegle != aaben:
                    if aaben:
                        dele.append("}")
                    if noegle:
                        dele.append(noegle[1] + "{")
                    aaben = noegle
                dele.append(tekst)
            if aaben:
                dele.append("}")
            kritisk = "".join(dele)
            with open(os.path.join(UD, typ + ".css"), "w", encoding="utf-8") as f:
                f.write(kritisk)
            stat[typ] = (len(kritisk), len(CSS))
            print(f"{typ:12} {len(kritisk)//1024:3} KB af {len(CSS)//1024} KB")
        b.close()
    with open(os.path.join(UD, "_stat.json"), "w") as f:
        json.dump(stat, f)


if __name__ == "__main__":
    main()
