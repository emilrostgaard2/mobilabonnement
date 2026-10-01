import json, os, glob, collections, gzip, re, sys, shutil
src=sys.argv[1]; ud=sys.argv[2]
def noegle(s):
    s=s.lower().replace("æ","ae").replace("ø","oe").replace("å","aa").replace("é","e").replace("ü","u").replace("ö","oe").replace("ä","ae")
    s=re.sub(r"[^a-z0-9]","",s)
    return (s[:2] or "_").ljust(2,"_")
idx=collections.defaultdict(lambda: collections.defaultdict(list))
for f in glob.glob(f"{src}/*.json"):
    d=json.load(open(f,encoding="utf-8"))
    for v,_ in d["v"]:
        idx[noegle(v)][v].append([d["p"],d["k"]])
if os.path.exists(ud): shutil.rmtree(ud)
os.makedirs(ud)
tot=maks=0
for k,veje in idx.items():
    obj=[[v,sorted(ps)] for v,ps in sorted(veje.items())]
    s=json.dumps(obj,ensure_ascii=False,separators=(",",":"))
    open(f"{ud}/{k}.json","w",encoding="utf-8").write(s); tot+=len(s.encode()); maks=max(maks,len(s.encode()))
print("filer",len(idx),"MB",round(tot/1e6,1),"største KB",maks//1024)
