import csv, json, os, collections, gzip, sys, shutil
src="/mnt/user-data/uploads/BBK26_udbudt_private_hatigheder_inkl__mobil.csv"
ud=sys.argv[1]
def n(v):
    v=(v or "").strip().replace(",",".")
    if not v: return 0
    try: return int(float(v))
    except: return 0
pr=collections.defaultdict(lambda: {"kom":collections.Counter(),"prof":{},"veje":collections.OrderedDict()})
with open(src,encoding="utf-8-sig",newline="") as f:
    for row in csv.DictReader(f,delimiter=";"):
        p=row["postnr"].strip()
        if not p.isdigit(): continue
        d=pr[p]; d["kom"][row["kommunenavn"]]+=1
        t=(n(row["download_fiber"]),n(row["upload_fiber"]),n(row["download_kabel_tv"]),n(row["upload_kabel_tv"]),
           n(row["download_xdsl"]),n(row["download_mobil"]),n(row["upload_mobil"]),n(row["download_fasttraadloest"]))
        pi=d["prof"].setdefault(t,len(d["prof"]))
        d["veje"].setdefault(row["vejnavn"],[]).append(f'{row["husnr"]}:{pi}')
if os.path.exists(ud): shutil.rmtree(ud)
os.makedirs(ud)
tot=totgz=maks=0
for p,d in pr.items():
    prof=[list(t) for t in sorted(d["prof"],key=d["prof"].get)]
    obj={"p":p,"k":d["kom"].most_common(1)[0][0],"f":prof,
         "v":[[v," ".join(h)] for v,h in d["veje"].items()]}
    s=json.dumps(obj,ensure_ascii=False,separators=(",",":"))
    open(f"{ud}/{p}.json","w",encoding="utf-8").write(s)
    b=len(s.encode()); tot+=b; totgz+=len(gzip.compress(s.encode())); maks=max(maks,b)
print("postnumre",len(pr),"i alt MB",round(tot/1e6,1),"gzip MB",round(totgz/1e6,1),"største KB",maks//1024)
