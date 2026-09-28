# Telemobils testprotokol

Testresultater vises KUN på sitet, når der står en test i `data/tests.json`.
Skriv aldrig tal, du ikke selv har målt. Markedsføringsloven § 5 forbyder
vildledende påstande — også påstanden "vi har testet".

## 1. Køb abonnementerne
- Ét pr. net: fx Oister (3), Lebara (Telenor/Norlys) og eesy (TDC NET).
- Uden binding og med eSIM. Gem kvitteringen.
- Er et abonnement stillet gratis til rådighed, skriv selskabets navn i
  `betalt_af`. Så oplyser siden det automatisk.

## 2. Aktivering
Notér minutter fra bestilling til fungerende eSIM → `aktivering_minutter`.

## 3. Hastighed
- Samme telefon og samme app hver gang (fx Speedtest by Ookla).
- Tre målinger pr. sted. Skriv MEDIANEN.
- Mindst: storby, forstad, land. Både inde og ude.
- Notér dato, sted, `omraade` (by/land), `inde` (true/false), download, upload og ping.

## 4. Kundeservice
Én henvendelse pr. selskab med et konkret spørgsmål. Notér dato, klokkeslæt,
kanal, ventetid i minutter, om sagen blev løst og emnet.

## 5. Billeder
Tag et par ægte billeder (aktivering, hastighedsmåling). Gem som .webp i
`assets/img/test/` og skriv filnavn + beskrivende alt-tekst i `billeder`.

## 6. Udfyld tests.json
Kopiér `_skabelon` ind i listen `"tests"`, udfyld med dine tal, og slet
eksempelteksten i `observationer`. Byg, tjek siden, commit.

Når første test ligger der, dukker afsnittet "Vi har testet …" op på
udbydersiden, metoden kommer på /metode/, og siden får Review-schema.
