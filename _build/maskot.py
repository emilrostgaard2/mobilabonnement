"""Signe — Telemobils maskot.

Én figur, flere positurer, alt som inline SVG. Hver positur er 2-3 KB og har
faste dimensioner, så den koster hverken et netværkskald eller et layoutskift.

Reglen for brug: Signe står der, hvor læseren er i tvivl eller skal videre —
hero, tomme tilstande, 404, anbefalinger. Aldrig inde i selve prislisten.

    from maskot import signe
    signe("vinker", 220)            # hero
    signe("kigger", 150)            # sidder på kanten af et kort eller en CTA
    signe("peger", 120)             # ved en knap eller et råd
    signe("tommel", 96)             # ved en anbefaling
    signe("leder", 160)             # 404 og nul resultater
"""

NAT, SIGNAL, BERRY, PULS, LEM = "#0B1026", "#3D5AFE", "#7C4DFF", "#00D18F", "#2E43E0"
KIND = "#FF7AB6"

_DEFS = (f'<defs><linearGradient id="sg-g" x1="0" y1="1" x2=".6" y2="0">'
         f'<stop offset="0" stop-color="{PULS}"/><stop offset=".55" stop-color="{SIGNAL}"/>'
         f'<stop offset="1" stop-color="{BERRY}"/></linearGradient></defs>')


def _lem(d, w=13):
    return (f'<path d="{d}" fill="none" stroke="{LEM}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _haand(x, y, r=12):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{LEM}"/>'


def _sko(x, y):
    return f'<ellipse cx="{x}" cy="{y}" rx="24" ry="12" fill="{LEM}"/>'


def _oje(x, y, dx=3, dy=2, r=21):
    return (f'<g class="sg-oje"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
            f'<circle cx="{x+dx}" cy="{y+dy}" r="{r*.55:.1f}" fill="{NAT}"/>'
            f'<circle cx="{x+dx+4}" cy="{y+dy-5}" r="{r*.2:.1f}" fill="#fff"/></g>')


def _ansigt(udtryk="glad"):
    kinder = (f'<ellipse cx="128" cy="240" rx="11" ry="7" fill="{KIND}" opacity=".75"/>'
              f'<ellipse cx="272" cy="240" rx="11" ry="7" fill="{KIND}" opacity=".75"/>')
    if udtryk == "undrende":
        # Øjnene kigger til siden, munden er et lille o
        return (_oje(160, 200, -6, 1) + _oje(240, 200, -6, 1) + kinder +
                f'<ellipse cx="200" cy="252" rx="11" ry="13" fill="{NAT}" opacity=".85"/>')
    if udtryk == "begejstret":
        return (_oje(160, 200) + _oje(240, 200) + kinder +
                '<path d="M168 238 Q200 286 232 238 Z" fill="#fff"/>')
    if udtryk == "ned":
        # Kigger ned på det, hun holder om
        return (_oje(160, 204, 1, 7) + _oje(240, 204, -1, 7) + kinder +
                '<path d="M172 250 Q200 274 228 250" fill="none" stroke="#fff" '
                'stroke-width="7" stroke-linecap="round"/>')
    return (_oje(160, 200) + _oje(240, 200) + kinder +
            '<path d="M170 244 Q200 272 230 244" fill="none" stroke="#fff" '
            'stroke-width="7" stroke-linecap="round"/>')


def _antenne(top="boelger"):
    stang = (f'<path d="M200 64 V112" stroke="{LEM}" stroke-width="9" stroke-linecap="round"/>'
             f'<circle cx="200" cy="62" r="11" fill="{PULS}"/>')
    if top == "spoergsmaal":
        return stang + (f'<text x="232" y="66" font-family="Inter,Arial,sans-serif" '
                        f'font-weight="800" font-size="58" fill="{BERRY}">?</text>')
    buer = "".join(
        f'<path class="sg-bue sg-bue{i}" d="M{200-r} 62 A{r} {r} 0 0 1 {200+r} 62" fill="none" '
        f'stroke="{PULS}" stroke-width="7" stroke-linecap="round" opacity="{o}"/>'
        for i, (r, o) in enumerate(((16, 1), (32, .7), (48, .4))))
    return buer + stang


_KROP = '<circle cx="200" cy="222" r="118" fill="url(#sg-g)"/>'
_BEN = (_lem("M158 318 L152 354") + _lem("M242 318 L248 354") + _sko(144, 360) + _sko(256, 360))

_TELEFON = (f'<rect x="306" y="120" width="56" height="92" rx="12" fill="{NAT}"/>'
            f'<rect x="313" y="130" width="42" height="66" rx="5" fill="#fff"/>'
            f'<rect x="320" y="176" width="6" height="12" rx="2" fill="{PULS}"/>'
            f'<rect x="330" y="166" width="6" height="22" rx="2" fill="{SIGNAL}"/>'
            f'<rect x="340" y="154" width="6" height="34" rx="2" fill="{BERRY}"/>')


def _vinker():
    return (_antenne() + _BEN +
            f'<g class="sg-vink">{_lem("M92 196 Q52 170 58 120")}{_haand(58, 116)}</g>' +
            _KROP + _ansigt() +
            _lem("M312 236 Q338 222 330 190") + _TELEFON + _haand(330, 196))


def _peger():
    # Venstre hånd i siden, højre arm strakt ud mod det, der ligger til højre
    return (_antenne() + _BEN +
            _lem("M94 250 Q60 262 84 296") + _KROP + _ansigt() +
            _lem("M310 250 Q350 262 384 250") + _haand(372, 252, 13) +
            f'<path d="M378 250 L398 246" stroke="{LEM}" stroke-width="10" stroke-linecap="round"/>')


def _tommel():
    return (_antenne() + _BEN +
            _lem("M92 236 Q58 252 62 288") + _haand(62, 290) + _KROP + _ansigt("begejstret") +
            _lem("M310 214 Q350 198 350 158") +
            f'<rect x="334" y="128" width="34" height="32" rx="12" fill="{LEM}"/>'
            f'<path d="M346 132 V104" stroke="{LEM}" stroke-width="13" stroke-linecap="round"/>')


def _leder():
    lup = (f'<circle cx="344" cy="150" r="30" fill="#fff" fill-opacity=".55" stroke="{NAT}" stroke-width="9"/>'
           f'<path d="M326 176 L314 196" stroke="{NAT}" stroke-width="11" stroke-linecap="round"/>')
    return (_antenne("spoergsmaal") + _BEN +
            _lem("M92 236 Q58 252 62 288") + _haand(62, 290) + _KROP + _ansigt("undrende") +
            _lem("M306 250 Q322 232 314 204") + lup + _haand(314, 202))


def _kigger(del_="alt"):
    # Kun overkroppen. Hænderne ligger hen over underkanten, så hun ser ud til
    # at sidde bag det element, hun placeres ovenpå.
    def greb(x):
        return (f'<rect x="{x-27}" y="262" width="54" height="36" rx="17" fill="{LEM}"/>'
                f'<path d="M{x-9} 276 V291 M{x+9} 276 V291" stroke="#fff" stroke-opacity=".35" '
                f'stroke-width="3" stroke-linecap="round"/>')
    if del_ == "krop":
        return _antenne() + _KROP + _ansigt("ned")
    if del_ == "haender":
        return greb(84) + greb(316)
    return _antenne() + _KROP + _ansigt("ned") + greb(84) + greb(316)


_POSITURER = {
    # navn: (funktion, viewBox x, y, bredde, højde)
    "vinker": (_vinker, 20, 0, 360, 380),
    "peger": (_peger, 40, 0, 364, 380),
    "tommel": (_tommel, 30, 0, 350, 380),
    "leder": (_leder, 30, 0, 360, 380),
    "kigger": (_kigger, 40, 0, 320, 300),
    # Samme figur delt i to lag: kroppen bag kortet, hænderne foran kanten
    "kigger-krop": (lambda: _kigger("krop"), 40, 0, 320, 300),
    "kigger-haender": (lambda: _kigger("haender"), 40, 0, 320, 300),
}


def signe(positur="vinker", bredde=200, klasse="", alt=""):
    """Inline SVG af Signe. Uden alt-tekst er hun ren dekoration for skærmlæsere."""
    f, x, y, w, h = _POSITURER[positur]
    hoejde = round(bredde * h / w)
    a11y = f'role="img" aria-label="{alt}"' if alt else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{("signe signe-" + positur + " " + klasse).strip()}" '
            f'xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
            f'width="{bredde}" height="{hoejde}" {a11y}>{_DEFS}{f()}</svg>')


def signe_fil(positur="vinker", bredde=400):
    """Selvstændig SVG-fil — til og:image, favicon-variant og sociale profiler."""
    return signe(positur, bredde).replace(' aria-hidden="true" focusable="false"', "")


if __name__ == "__main__":
    import sys
    ud = sys.argv[1] if len(sys.argv) > 1 else "."
    for p in [p for p in _POSITURER if "-" not in p]:
        open(f"{ud}/signe-{p}.svg", "w", encoding="utf-8").write(signe_fil(p))
    print("Skrev", ", ".join(_POSITURER))
