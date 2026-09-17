"""Samler prishistorikken fra hele git-historikken.

Problemet: data/prishistorik.json ligger kun i repoet — ikke i den zip, sitet
udvikles i. Bliver filen slettet eller overskrevet ved en upload, starter
målingerne forfra, og prisudviklingssiden falder tilbage til "1 måling".

Løsningen: git husker alle tidligere udgaver af filen. Før hvert build læser vi
dem alle og fletter målingerne sammen pr. dato. En måling, der én gang er
committet, kan derfor ikke gå tabt igen — uanset hvad der sker med filen.

Kræver fuld historik i checkout (fetch-depth: 0). Fejler aldrig buildet.
"""
import json
import os
import subprocess
import sys

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIL = "data/prishistorik.json"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROD, capture_output=True, text=True, check=False)


def main():
    samlet = {}
    commits = git("log", "--format=%H", "--", FIL).stdout.split()
    # Ældste først, så nyere udgaver af samme dato vinder
    for c in reversed(commits[:2000]):
        ud = git("show", f"{c}:{FIL}")
        if ud.returncode != 0:
            continue
        try:
            for m in json.loads(ud.stdout).get("maalinger", []):
                if m.get("dato"):
                    samlet[m["dato"]] = m
        except ValueError:
            continue

    sti = os.path.join(ROD, FIL)
    nu = []
    try:
        with open(sti, encoding="utf-8") as f:
            nu = json.load(f).get("maalinger", [])
    except (FileNotFoundError, ValueError):
        pass
    for m in nu:
        if m.get("dato"):
            samlet[m["dato"]] = m

    if len(samlet) <= len(nu):
        print(f"Prishistorik: {len(nu)} målinger, intet at genskabe "
              f"({len(commits)} tidligere udgaver gennemset).")
        return
    maalinger = [samlet[d] for d in sorted(samlet)]
    os.makedirs(os.path.dirname(sti), exist_ok=True)
    with open(sti, "w", encoding="utf-8") as f:
        json.dump({"maalinger": maalinger}, f, ensure_ascii=False, indent=1)
    print(f"Prishistorik GENSKABT: {len(nu)} → {len(maalinger)} målinger "
          f"({maalinger[0]['dato']} til {maalinger[-1]['dato']}).")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:  # må aldrig vælte et build
        print(f"Prishistorik: kunne ikke genskabe ({ex}) — fortsætter.", file=sys.stderr)
