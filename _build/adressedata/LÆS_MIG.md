# Adressedata til adressetjekket på bredbåndssiderne

Kilde: Digitaliseringsstyrelsens Bredbåndskortlægning 2026, filen
"BBK26_udbudt_private_hatigheder_inkl__mobil.csv" (hentet fra tjekditnet.dk).
Den viser for hver adresse de hastigheder, der udbydes til private, pr. teknologi.

Opdatering én gang om året, når en ny kortlægning udkommer (typisk sommer):

    python3 _build/adressedata/1_postnumre.py assets/adr/p
    python3 _build/adressedata/2_vejindeks.py assets/adr/p assets/adr/v

Ret stien til CSV-filen øverst i 1_postnumre.py. Ret også BBK i build.py
(årstal og landstal fra "baggrundsdata_landsplan.xlsx").

Format pr. postnummer (assets/adr/p/8000.json):
  f: hastighedsprofiler [fiber ned, fiber op, kabel ned, kabel op, xDSL ned,
     mobil ned, mobil op, fast trådløst ned]  (Mbit/s, 0 = ikke udbudt)
  v: [vejnavn, "husnr:profil husnr:profil ..."]
