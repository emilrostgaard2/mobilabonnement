# -*- coding: utf-8 -*-
"""
UDKAST TIL EMILS PERSONLIGE ERFARINGER
======================================

VIGTIGT: Alt herunder er FORMULERINGSUDKAST skrevet af en AI, ikke Emils
faktiske oplevelser. De er placeholdere med den rigtige form, tone og længde,
så Emil kan skrive sine egne historier ind ovenpå.

Publicér ALDRIG teksterne som de står. Førstehåndserfaring er kun noget værd,
hvis den er ægte — og at udgive opdigtede personlige oplevelser under navn ville
underminere præcis den troværdighed, historierne skal opbygge.

Sådan retter du til:
  1. Behold strukturen: konkret situation → tal → hvad du lærte.
  2. Udskift navne, beløb og udbydere med det, der faktisk skete.
  3. Er en historie ikke sand for dig, så slet blokken helt — build kører videre
     uden den. Fire ægte historier slår ti opdigtede.
"""

# Sæt til True, når teksterne er gennemskrevet og passer til virkeligheden.
GODKENDT = False


HISTORIER = {

    # ---------------------------------------------------------------- forside
    "forside": {
        "titel": "Derfor byggede jeg Telemobil",
        "tekst": """
<p>Jeg opdagede problemet på min egen regning. Jeg havde haft det samme abonnement
i knap fire år uden at kigge på det — 249 kr. om måneden for noget, jeg havde tegnet,
da jeg flyttede hjemmefra. Da jeg endelig satte mig ned med tallene, brugte jeg
under 15 GB om måneden og betalte for fri data.</p>
<p>Det tog mig tyve minutter at skifte. Jeg sparede omkring 150 kr. om måneden, og jeg
kunne ikke mærke nogen forskel på min telefon overhovedet.</p>
<p>Det, der irriterede mig mest, var ikke pengene. Det var, at jeg havde brugt et år
på at researche mit boliglån og nul minutter på et abonnement, jeg betalte for hver
eneste måned. Da jeg begyndte at spørge folk omkring mig, viste det sig, at næsten
alle havde det på samme måde. Telemobil er bygget for at gøre de tyve minutter til
to.</p>
""",
    },

    # ---------------------------------------------- billigste mobilabonnement
    "billigste": {
        "titel": "Den fejl jeg selv lavede: billigst er ikke altid billigst",
        "tekst": """
<p>Første gang jeg selv skiftede efter at have researchet markedet, valgte jeg for
småt. Jeg fandt et abonnement til 49 kr. med 5 GB, tænkte at jeg jo alligevel er på
wi-fi det meste af tiden, og var ret tilfreds med mig selv.</p>
<p>Så fik jeg en periode, hvor jeg pendlede og hørte podcasts og brugte kort hver dag.
Jeg løb tør omkring den 20. i måneden og købte ekstra data tre måneder i træk. De
tre måneder kostede mig mere, end et abonnement med 30 GB ville have gjort hele
året.</p>
<p>Det er derfor, vi konsekvent anbefaler ét trin over dit målte forbrug. Ikke fordi
vi tjener mere på det — men fordi springet i pris mellem kategorierne er så lille, og
prisen for at ramme forkert er så stor.</p>
""",
    },

    # ------------------------------------------------------------- fri data
    "fri_data": {
        "titel": "Min svoger betalte 100 kr. om måneden for tryghed",
        "tekst": """
<p>Min svoger spurgte mig sidste år, om han skulle skifte til fri data. Han var
overbevist om, at han brugte enormt meget, fordi han altid streamer musik i bilen.</p>
<p>Vi slog det op i hans telefon sammen. Han lå på 22 GB om måneden. Musik fylder
næsten ingenting — det er video, der koster. Han havde betalt for fri data i to år
og aldrig været i nærheden af at have brug for det.</p>
<p>Han flyttede ned til 50 GB og sparer nu omkring 100 kr. om måneden. Det er den
samtale, jeg har haft flest gange: folk overvurderer deres dataforbrug voldsomt,
fordi de forveksler <em>ofte</em> med <em>meget</em>.</p>
""",
    },

    # --------------------------------------------------------------- udlandet
    "udlandet": {
        "titel": "Regningen fra Tyrkiet jeg aldrig glemmer",
        "tekst": """
<p>En ven ringede til mig fra en ferie i Tyrkiet og spurgte, hvorfor hans telefon
pludselig var spærret. Han havde brugt data som hjemme i to dage — kort, billeder til
familien, lidt sociale medier — og troede, at EU-reglerne dækkede.</p>
<p>Tyrkiet er ikke i EU. Regningen løb op i flere tusinde kroner, og han fik den ikke
nedsat.</p>
<p>Det er den dyreste enkeltfejl, jeg har set nogen begå med et mobilabonnement, og
den tager ti sekunder at undgå: slå dataroaming fra, før du letter. Det er derfor,
det står så mange steder på denne side.</p>
""",
    },

    # ------------------------------------------------------------ prisstigning
    "prisstigning": {
        "titel": "Ti minutter i telefonen gav 60 kr. om måneden",
        "tekst": """
<p>Min mor ringede og var irriteret over, at hendes regning var steget uden varsel —
som hun troede. Varslet lå i hendes spamfilter.</p>
<p>Jeg foreslog, at hun ringede og sagde, at hun overvejede at skifte. Hun var
overbevist om, at det ikke nyttede noget. Efter ti minutter i telefonen fik hun
samme pris som nye kunder, altså 60 kr. mindre om måneden end det, hun lige var
steget til.</p>
<p>Det virker overraskende ofte. Selskaberne har en fastholdelsesafdeling, netop
fordi det koster dem mere at skaffe en ny kunde end at give dig en rabat.</p>
""",
    },

    # ------------------------------------------------------------------ børn
    "boern": {
        "titel": "Datastop er den indstilling, jeg altid slår til først",
        "tekst": """
<p>En kollega fik en regning på over tusind kroner, fordi hans datter havde brugt
telefonen som hotspot til sin iPad i sommerferien. Der var ingen datastop på
abonnementet, så udbyderen købte bare mere data på hans vegne, måned ud og måned ind.</p>
<p>Han var ikke sur på datteren. Han var sur på sig selv, fordi han ikke vidste, at
indstillingen fandtes.</p>
<p>Den tager tredive sekunder at slå til, og den findes hos stort set alle udbydere.
Det er det første, jeg gør på ethvert nyt abonnement — også mit eget.</p>
""",
    },
}


def historie(noegle, foto, navn, profil_url):
    """Renderer en erfaringsblok. Returnerer tom streng, hvis historien ikke findes."""
    h = HISTORIER.get(noegle)
    if not h:
        return ""
    udkast = ""
    if not GODKENDT:
        udkast = ('<p class="udkast-mark">Udkast — teksten skal gennemskrives, '
                  'før siden går i luften.</p>')
    return f"""<aside class="erfaring">
  <div class="erf-hoved">
    <img src="{foto}" width="56" height="56" alt="{navn}" loading="lazy">
    <div>
      <span class="erf-maerkat">Fra Emils egen erfaring</span>
      <h3>{h['titel']}</h3>
    </div>
  </div>
  <div class="erf-tekst">{h['tekst']}</div>
  {udkast}
  <p class="erf-fod"><a href="{profil_url}">{navn}</a> · stifter af Telemobil</p>
</aside>"""
