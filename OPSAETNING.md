# Sådan kommer du ud af merge-konflikter én gang for alle

Konflikterne opstår, fordi de genererede HTML-filer ligger i git, og både du og
robotten ændrer dem. Denne opsætning fjerner dem fra git — så rører I aldrig de
samme filer igen.

## Trin 1 — start forfra lokalt (5 minutter)

1. Tryk **Abort Merge** i GitHub Desktop, hvis dialogen er åben.
2. I GitHub Desktop: **File → Clone repository → mobilabonnement**.
   Vælg en **ny** mappe, fx `mobilabonnement-ny` på skrivebordet.
3. Når den er klonet, arbejder du kun i den nye mappe. Den gamle kan slettes.

Du mister ingenting — alt ligger på GitHub og i zip-filen.

## Trin 2 — læg zip'ens indhold i den nye mappe

Erstat alt. `.gitignore` følger med og sørger for, at HTML'en holdes ude.

## Trin 3 — fjern HTML fra sporingen

I GitHub Desktop vil du se, at ~91 HTML-filer står som **slettet**. Det er
meningen: de forsvinder fra git, men bygges stadig af workflowet.

Skriv "Fjern genereret HTML fra git" i Summary → **Commit to main** → **Push**.

## Fremover

Du redigerer kun `_build/`, `data/` og `assets/`. HTML'en bygges automatisk.
Push, og workflowet klarer resten.

Konflikter kan ikke længere opstå, fordi robotten kun rører `data/abonnementer.json`
— og den fil ligger ikke i de zip-filer, du får.
