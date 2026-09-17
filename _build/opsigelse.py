"""Opsigelse pr. selskab.

Search Console (sept. 2026) viste, at den generelle opsigelsesguide allerede
lå på plads 9-12 for "3 mobil opsigelse", "telmore opsigelsesperiode" og "cbb
opsigelsesperiode" — uden at have en side om nogen af dem. Her er siderne.

REGEL: et selskab kommer kun med, når varsel og fremgangsmåde er læst i
selskabets EGNE vilkår eller hjælpesider. Under researchen angav flere
konkurrentsider forkerte varsler (fx "løbende måned + 30 dage" for CBB, hvor
vilkårene siger løbende måned). En side med et forkert varsel koster læseren en
måneds betaling — så hellere tre rigtige sider end fjorten usikre.

Nyt selskab: læs vilkårene, udfyld en post herunder med kilde og dato, byg.
"""

# varseltype: "dage30" = 30 dage fra opsigelsen · "maaned1" = én måned fra
# opsigelsen · "maanedsudgang" = til udgangen af den måned, du opsiger i
SELSKABER = {
    "telmore": {
        "navn": "Telmore", "udbyder_slug": "telmore",
        "varseltype": "maaned1", "varsel_kort": "1 måneds varsel",
        "varsel_lang": ("Telmores abonnementsvilkår giver dig ret til at opsige med én måneds "
                        "varsel. Varslet løber fra den dag, Telmore modtager opsigelsen — ikke "
                        "fra et månedsskifte."),
        "metode_kort": "Mit Telmore-appen",
        "trin": [
            ("Åbn Mit Telmore-appen", "Log ind med det nummer, du vil opsige. Har du flere numre, "
             "skal du være logget ind på det rigtige."),
            ("Find opsigelse under dit abonnement", "Telmore oplyser selv, at opsigelsen sker "
             "direkte i appen."),
            ("Vent på bekræftelsen", "Telmore sender en bekræftelse, når opsigelsen er modtaget. "
             "Gem den — det er dit bevis for datoen."),
            ("Kan du ikke logge ind?", "Så kan du skrive til Telmore via kontaktformularen på "
             "deres hjælpeside. Bed om en skriftlig bekræftelse."),
        ],
        "saerligt_h2": "Har du streaming med i dit Telmore-abonnement?",
        "saerligt": ("Mange Telmore-abonnementer har en streamingtjeneste indbygget. Når "
                     "abonnementet stopper, stopper adgangen gennem Telmore også. Vil du beholde "
                     "tjenesten, skal du selv tegne den direkte hos udbyderen bagefter — og "
                     "regne den pris med, når du sammenligner med et billigere mobilabonnement. "
                     "Et abonnement til 99 kr. plus en tjeneste til 129 kr. er ikke billigere "
                     "end et samlet til 199 kr."),
        "kilder": [("Telmore: Opsigelse af abonnement",
                    "https://www.telmore.dk/hjaelp/abonnement/opsigelse-af-abonnement"),
                   ("Telmore: Abonnementsvilkår for mobil",
                    "https://www.telmore.dk/mobilabonnement/vilkaar-og-sikkerhed/abonnementsvilkaar-mobil")],
        "tjekket": "2026-09-17",
    },
    "3": {
        "navn": "3", "udbyder_slug": None,
        "varseltype": "dage30", "varsel_kort": "30 dages varsel",
        "varsel_lang": ("Ifølge 3's abonnementsvilkår for privatkunder (punkt 27.3) kan du opsige "
                        "med 30 dages varsel, når du ikke har binding, eller når bindingen er "
                        "udløbet. Har du binding, kan du opsige til bindingens udløb med samme "
                        "varsel."),
        "metode_kort": "Mit 3 på 3.dk eller kundeservice",
        "trin": [
            ("Log ind på Mit 3 på 3.dk", "Brug hjemmesiden, ikke appen. 3's vilkår siger "
             "udtrykkeligt, at opsigelse ikke er mulig i Mit 3-appen."),
            ("Vælg abonnementet og opsig", "Find nummeret under dine abonnementer, og vælg "
             "opsigelse. Alternativt kan du ringe til kundeservice på 70 313 313 eller skrive "
             "til kundeservice@3.dk."),
            ("Du skal selv stå for det", "Kun den, der står på aftalen, kan opsige — ikke en "
             "bruger af abonnementet, fx et barn eller en ægtefælle."),
            ("Bekræftelse inden for en uge", "3 oplyser i vilkårene, at du får en bekræftelse "
             "inden for en uge. Kommer den ikke, så følg op skriftligt."),
        ],
        "saerligt_h2": "Har du telefon på afbetaling hos 3?",
        "saerligt": ("Så fortsætter afbetalingen, selv om abonnementet stopper. 3's vilkår siger "
                     "direkte, at afbetalingsaftalen ikke bortfalder ved opsigelse — den løber "
                     "videre, indtil den er betalt eller opsagt særskilt. Køb med 3Afbetaling "
                     "giver desuden seks måneders binding på abonnementet. Vil du ud før tid, "
                     "kan du betale de resterende måneder og opsige med det samme. Alle tilvalg "
                     "som musik, tv og forsikring falder bort sammen med abonnementet."),
        "kilder": [("3: Abonnementsvilkår for privatkunder, gældende fra 16. juli 2026, punkt 27",
                    "https://www.3.dk/globalassets/documents/vilkaar/privat-abonnementsvilkar.pdf")],
        "tjekket": "2026-09-17",
    },
    "cbb-mobil": {
        "navn": "CBB Mobil", "udbyder_slug": "cbb-mobil",
        "varseltype": "maanedsudgang", "varsel_kort": "løbende måned",
        "varsel_lang": ("CBB Mobils generelle vilkår (punkt 18) giver løbende måneds opsigelse: "
                        "abonnementet stopper den sidste dag i den måned, hvor du opsiger. Det er "
                        "blandt de korteste varsler på markedet. Opsiger du den 25., er du ude "
                        "under en uge senere — opsiger du den 2., betaler du næsten en hel måned."),
        "metode_kort": "Mit CBB eller kundeservice@cbb.dk",
        "trin": [
            ("Log ind på din side på cbb.dk", "Vilkårene siger, at opsigelse skal ske skriftligt, "
             "via din personlige side eller ved kontakt til kundeservice."),
            ("Eller skriv til kundeservice@cbb.dk", "En mail giver dig samtidig dokumentation for "
             "datoen. Kundeservice har telefon 50 50 50 50."),
            ("Oplys et kontonummer", "Har du penge til gode, udbetaler CBB dem til den konto, du "
             "oplyser — ifølge vilkårene senest 30 dage efter opsigelsen."),
            ("Tjek datoen i bekræftelsen", "Der skal stå den sidste dag i måneden. Står der noget "
             "andet, så spørg med det samme."),
        ],
        "saerligt_h2": "Time din opsigelse hos CBB",
        "saerligt": ("Fordi abonnementet altid løber måneden ud, er der ingen grund til at opsige "
                     "tidligt på måneden — du betaler for hele måneden uanset hvad. Har du købt "
                     "telefon med minimumsforbrug hos CBB, skal det manglende minimumsforbrug "
                     "betales, før nummeret frigives, og en afdragsordning løber videre, selv om "
                     "mobilaftalen stopper."),
        "kilder": [("CBB Mobil: Generelle vilkår, punkt 18 Opsigelse",
                    "https://www.cbb.dk/vilkar/generelle-vilkar/"),
                   ("CBB Mobil: Vilkår for afdragsordning og minimumsforbrug",
                    "https://www.cbb.dk/vilkar/mobiltelefoner/afdrag-og-minimumsforbrug/")],
        "tjekket": "2026-09-17",
    },
}

STI = "/guides/opsig-mobilabonnement/{slug}/"


def sti(slug):
    return STI.format(slug=slug)


def oversigt(e):
    """Tabel til hovedguiden — linker ned til selskabssiderne."""
    raekker = "".join(
        f'<tr><td><a href="{sti(s)}"><strong>Opsig {e(d["navn"])}</strong></a></td>'
        f'<td>{e(d["varsel_kort"])}</td><td>{e(d["metode_kort"])}</td></tr>'
        for s, d in SELSKABER.items())
    return f"""<h2 id="pr-selskab">Opsigelsesvarsel og fremgangsmåde pr. selskab</h2>
<p>Vi har læst selskabernes egne vilkår — ikke andre sammenligningssider, som ofte angiver
forkerte varsler. Et selskab kommer først på listen, når vi har set varslet i deres vilkår.</p>
<div class="tabelrul"><table><thead><tr><th>Selskab</th><th>Varsel</th><th>Sådan opsiger du</th>
</tr></thead><tbody>{raekker}</tbody></table></div>"""


def beregner(d):
    """Lille datoberegner. Ingen afhængigheder, virker uden resten af sitets JS."""
    return f"""<div class="ops-beregner" data-varsel="{d['varseltype']}">
  <p class="ops-b-titel">Hvornår stopper dit {d['navn']}-abonnement?</p>
  <label for="ops-dato">Jeg opsiger den</label>
  <input type="date" id="ops-dato">
  <p class="ops-b-svar" aria-live="polite"></p>
  <p class="ops-b-note">Vejledende beregning ud fra {d['navn']}s vilkår. Har du binding,
  gælder den først. Den bindende dato står i {d['navn']}s bekræftelse.</p>
</div>
<script>(function(){{var b=document.currentScript.previousElementSibling,i=b.querySelector('input'),
s=b.querySelector('.ops-b-svar'),t=b.dataset.varsel,m=['januar','februar','marts','april','maj','juni',
'juli','august','september','oktober','november','december'];
function f(d){{return d.getDate()+'. '+m[d.getMonth()]+' '+d.getFullYear()}}
function r(){{if(!i.value)return;var d=new Date(i.value+'T12:00:00'),u;
if(t==='dage30'){{u=new Date(d);u.setDate(u.getDate()+30)}}
else if(t==='maaned1'){{u=new Date(d);var dag=u.getDate();u.setMonth(u.getMonth()+1);
if(u.getDate()!==dag)u.setDate(0)}}
else{{u=new Date(d.getFullYear(),d.getMonth()+1,0,12)}}
var dage=Math.round((u-d)/864e5);
s.innerHTML='Abonnementet stopper omkring <strong>'+f(u)+'</strong>'+(dage>1?' — du betaler altså for cirka '
+dage+' dage mere.':' — altså med det samme.')}}
var n=new Date();i.value=n.getFullYear()+'-'+('0'+(n.getMonth()+1)).slice(-2)+'-'+('0'+n.getDate()).slice(-2);
i.addEventListener('input',r);r()}})();</script>"""


def brodtekst(slug, e, gennemgang, D, udbyderlink):
    d = SELSKABER[slug]
    n = d["navn"]
    trin = "".join(f"<li><strong>{e(t)}</strong>\n{e(b)}</li>" for t, b in d["trin"])
    kilder = "".join(f'<li><a href="{u}" rel="noopener nofollow" target="_blank">{e(t)}</a></li>'
                     for t, u in d["kilder"])
    dag, md, aar = d["tjekket"][8:].lstrip("0"), int(d["tjekket"][5:7]), d["tjekket"][:4]
    mdr = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september",
           "oktober", "november", "december"][md - 1]
    return f"""<section class="sektion baand-smal artikel">
{gennemgang}

<div class="udtag">
<p><strong>Kort svar:</strong> {e(n)} har <strong>{e(d["varsel_kort"])}</strong>, og du opsiger via
{e(d["metode_kort"])}. Skifter du til et andet selskab og vil beholde dit nummer, skal du
<strong>ikke</strong> opsige selv — det nye selskab gør det for dig.</p>
</div>

{beregner(d)}

<h2>Opsigelsesvarsel hos {e(n)}</h2>
<p>{e(d["varsel_lang"])}</p>

<h2>Sådan opsiger du {e(n)} — trin for trin</h2>
<ol class="trin">{trin}</ol>

<div class="advarsel">
<p><strong>Vil du beholde dit nummer?</strong> Så bestil det nye abonnement først, og oplys dit
nummer ved bestillingen. Det nye selskab opsiger {e(n)} og flytter nummeret. Opsiger du selv
først, bliver nummeret frigivet og kan i værste fald ikke genskabes.
<a href="/guides/skift-mobilselskab/">Sådan skifter du uden at miste nummeret</a>.</p>
</div>

<h2>{e(d["saerligt_h2"])}</h2>
<p>{e(d["saerligt"])}</p>

<h2>Binding og fortrydelsesret</h2>
<p>Et mobilselskab må højst binde dig i seks måneder. Er du inden for de første 14 dage efter et
køb på nettet eller i telefonen, har du som udgangspunkt fortrydelsesret — den er hurtigere end
en opsigelse, fordi aftalen annulleres i stedet for at løbe varslet ud.
<a href="/guides/opsig-mobilabonnement/">Læs de generelle regler for opsigelse</a>.</p>

<h2>Hvad skal du have i stedet?</h2>
<p>De fleste opsiger, fordi prisen er løbet fra dem. Lige nu følger vi {D['antal']} abonnementer
fra {D['antal_udbydere']} selskaber, og {D['antal_uden_binding']} af dem er helt uden binding.
{udbyderlink}</p>

<h2>Kilder</h2>
<p>Varsel og fremgangsmåde er læst i {e(n)}s egne vilkår og hjælpesider den {dag}. {mdr} {aar}.
Vilkår kan ændre sig — står der noget andet i din egen aftale, er det den, der gælder.</p>
<ul>{kilder}</ul>
</section>"""


def faq(slug):
    d = SELSKABER[slug]
    n = d["navn"]
    return [
        {"sp": f"Hvor langt opsigelsesvarsel har {n}?",
         "sv": f"{n} har {d['varsel_kort']}. {d['varsel_lang']}"},
        {"sp": f"Hvordan opsiger jeg mit abonnement hos {n}?",
         "sv": f"Du opsiger via {d['metode_kort']}. {d['trin'][0][1]} Gem bekræftelsen som "
               f"dokumentation for datoen."},
        {"sp": f"Skal jeg opsige {n}, hvis jeg skifter til et andet selskab?",
         "sv": f"Nej. Bestil hos det nye selskab og oplys dit nummer — så opsiger de {n} for dig "
               f"og flytter nummeret. Opsiger du selv først, risikerer du at miste nummeret."},
        {"sp": f"Koster det noget at opsige {n}?",
         "sv": f"Selve opsigelsen er gratis. Du betaler for varslet, og har du binding eller "
               f"telefon på afbetaling, skal det resterende beløb betales."},
    ]
