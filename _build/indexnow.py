#!/usr/bin/env python3
"""Sender de sider, der er ændret i dag, til IndexNow (Bing, Yandex, Seznam m.fl.).

Kører efter upload i workflowet. Fejler den, stopper intet andet."""
import json
import os
import urllib.request
from datetime import date

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site = json.load(open(os.path.join(ROD, "data", "site.json"), encoding="utf-8"))
noegle = site.get("indexnow_key")
domaene = site["domaene"].rstrip("/")
host = domaene.split("//", 1)[1]
try:
    hist = json.load(open(os.path.join(ROD, "data", "sidehistorik.json"), encoding="utf-8"))
except (FileNotFoundError, ValueError):
    hist = {}
idag = date.today().isoformat()
urls = [domaene + sti for sti, v in hist.items() if (v or {}).get("dato") == idag][:10000]
if not noegle or not urls:
    print("IndexNow: intet at sende")
    raise SystemExit(0)
data = json.dumps({"host": host, "key": noegle,
                   "keyLocation": f"{domaene}/{noegle}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=data,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: {len(urls)} sider sendt, svar {r.status}")
except Exception as ex:
    print(f"IndexNow fejlede (ikke kritisk): {ex}")
