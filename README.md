# telemobil.dk

Statisk affiliate-side om mobilabonnementer. Alle sider genereres fra `data/`.

## Byg

```bash
python3 _build/build.py      # genererer alle HTML-sider + sitemap, robots, .htaccess
python3 _build/validate.py   # tjekker SEO, links, struktur. Fejl = exit 1
```

## Struktur

```
data/site.json           Domæne, udgivelsesdato, data_verificeret-flag
data/udbydere.json       De 10 udbydere: anmeldelse, fordele, ulemper, FAQ
data/abonnementer.json   Alle abonnementer og priser  <- Adtraction skriver KUN denne
_build/skabelon.py       HTML-shell, SEO-head, nav, footer, komponenter, pristabel
_build/indhold.py        Langt redaktionelt indhold til hovedsiderne
_build/build.py          Orkestrering + sidegeneratorer
_build/validate.py       Validering
assets/                  CSS, JS, logoer, portrætfoto
```

Genererede filer (index.html, undermapper, sitemap.xml, robots.txt, .htaccess,
404.html, favicon.svg, site.webmanifest) commites, så FTP-deploy bare spejler mappen.

## FØR LANCERING

1. **Priserne i `data/abonnementer.json` er placeholders.** Erstat med rigtige tal
   eller lad Adtraction-feedet skrive filen.
2. **Netværk for 5 udbydere er sat til "MVNO"**, fordi de ikke er verificeret:
   greentel, duka, lyca-mobile, eesy, flexii. Verificér på udbyderens egen side
   og ret `netvaerk`-feltet til "TDC NET", "Telenor" eller "3".
3. **Sæt `data_verificeret: true` i `data/site.json`**, når 1 og 2 er på plads.
   Build og validate advarer indtil da.
4. Udskift `kontakt@telemobil.dk` med en rigtig adresse.
5. Tilføj GA4-snippet hvis ønsket — JS'en sender allerede `klik_udbyder`-events
   via `gtag`, hvis den findes.
6. Lav et `assets/img/telemobil-social.png` (1200x630) til OG-billedet.

## Adtraction-integration

Byg et script der henter feedet og skriver `data/abonnementer.json` i samme format.
Felter pr. abonnement:

```json
{ "id": "", "udbyder": "<slug fra udbydere.json>", "navn": "", "data_gb": 0,
  "pris": 0, "foer_pris": null, "tale": "fri", "sms": "fri", "binding": 0,
  "oprettelse": 0, "eu_gb": 0, "femg": true, "badge": null, "link": "" }
```

`data_gb: 999` betyder fri data. Kør derefter `build.py` og commit.

---

## Adtraction-integration

Priserne hentes automatisk fra Adtractions data feed ved hvert build.

### Første gang

1. Sæt `ADTRACTION_CHANNEL_ID` som GitHub Secret (samme sted som FTP-oplysningerne).
2. Kør `python3 _build/adtraction.py --inspect` lokalt og send outputtet videre,
   hvis feltnavnene i feedet ikke matcher. Importøren gætter på almindelige
   navne, men Adtraction varierer mellem annoncører.
3. Erstat `.github/workflows/deploy.yml` med `deploy-workflow.yml` fra roden.

### Sådan virker det

```
_build/adtraction.py   henter feedet -> skriver data/abonnementer.json
_build/build.py        bygger 88 sider ud fra den fil
_build/validate.py     stopper deploy hvis noget er galt
```

Workflowet kører ved hvert push og desuden to gange dagligt via cron, så
priserne holdes friske uden at du rører noget. Ændrede priser committes
tilbage til repoet, så du kan se prishistorikken i git-loggen.

### Kortlægning af udbydere

`UDBYDER_KORT` i adtraction.py oversætter Adtractions annoncørnavne til vores
slugs. Får du en ny annoncør godkendt, tilføj den der — ellers springes den over
med en besked i byggeloggen.

### Hvis noget går galt

Importøren skriver aldrig en tom fil. Kan ingen abonnementer oversættes, stopper
den med en fejl, og det gamle datasæt bliver stående. Byggeloggen viser, hvad der
blev sprunget over og hvorfor.


## Vigtigt: data/abonnementer.json

Filen genereres automatisk ved hvert build og committes tilbage af workflowet.

**Overskriv den aldrig manuelt.** Lægger du en ældre version ind — for eksempel fra en
zip — mister du de nyeste priser, indtil næste kørsel henter dem igen. Nye udbydere
forsvinder fra tabellerne i mellemtiden.

Skal du lægge nye filer ind udefra, så lad `data/abonnementer.json` og `data/site.json`
blive stående som de er.
