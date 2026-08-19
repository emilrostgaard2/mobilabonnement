# -*- coding: utf-8 -*-
"""Indhold til: gennemsnitspris, uden kreditvurdering, familie, opsigelse, erhverv."""

from skabelon import kr


def hvad_koster(D, S, t):
    """S er statistik-dictet fra build.py."""
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et mobilabonnement i Danmark koster i gennemsnit
<strong>{S['gns']} kr. om måneden</strong> regnet over 12 måneder. Medianprisen er
{S['median']} kr., og spændet går fra {S['min']} til {S['maks']} kr. Tallene er beregnet på
de {S['antal']} abonnementer, vi følger — ikke på skøn.</p>
</div>

<h2>Gennemsnitsprisen på et mobilabonnement</h2>

<p>De fleste sider svarer på dette spørgsmål med et interval: "fra 19 til 300 kr." Det er
sandt, men ubrugeligt. Du skal ikke bruge yderpunkterne — du skal bruge midten, og du skal
vide, hvor bredt der er spredt omkring den.</p>

<p>Derfor regner vi det ud. Alle tal på denne side er beregnet på vores egne prisdata, som
opdateres to gange dagligt, og de bruger <a href="/12-maaneders-prisen/">12-måneders-prisen</a>
frem for introprisen. Det er en vigtig forskel, som vi vender tilbage til.</p>

{t['statistiktabel']}

<p>Læg mærke til forskellen mellem gennemsnit og median. Gennemsnittet er {S['gns']} kr.,
medianen {S['median']} kr. At medianen er lavere betyder, at nogle få dyre abonnementer
trækker gennemsnittet op. Det typiske abonnement ligger altså tættere på medianen — og det
er det tal, du skal måle din egen regning mod.</p>

<div class="tip">
<h3>Betaler du over {S['median']} kr.?</h3>
<p>Så ligger du i den dyre halvdel af markedet. Det kan sagtens være berettiget, hvis du har
et stort dataforbrug, kører på et premiumnet eller har streaming med. Men det er værd at
tjekke, om du får noget for pengene, du reelt bruger.
<a href="/billigste-mobilabonnement/">Se hele sammenligningen</a>.</p>
</div>

<h2>Det tal, der overrasker: 69 % sælges på intropris</h2>

<p>Af de {S['antal']} abonnementer, vi følger, er <strong>{S['antal_intro']}</strong> solgt
med en kampagnepris — altså {S['andel_intro']} %. Kun {S['antal_fast']} har fast pris fra
dag ét.</p>

<p>Introperioden varer i gennemsnit <strong>{S['gns_intro_mdr']} måneder</strong>. Når den
udløber, stiger prisen med i snit <strong>{S['gns_stigning']} kr. om måneden</strong>. Den
største enkeltstigning i vores data er {S['maks_stigning']} kr.</p>

<p>Det er derfor, gennemsnitsprisen på {S['gns']} kr. er højere end den pris, du ser
annonceret. Markedsføringen viser introprisen. Regningen viser normalprisen på
{S['gns_normal']} kr. i gennemsnit.</p>

<div class="advarsel">
<p><strong>Regn altid på 12 måneder.</strong> Et abonnement til 44 kr. i 3 måneder og 89 kr.
derefter koster 78 kr. i gennemsnit over året — ikke 44. Sammenligner du én udbyders
intropris med en andens normalpris, sammenligner du to forskellige ting.
<a href="/12-maaneders-prisen/">Se formlen vi bruger</a>.</p>
</div>

<h2>Hvad du får for pengene</h2>

<p>Det gennemsnitlige abonnement med en fast datamængde indeholder
<strong>{S['gns_data']} GB</strong>, mens medianen er {S['median_data']} GB. Igen fortæller
forskellen noget: der findes nogle meget store pakker, som trækker gennemsnittet op.</p>

<p>Prisen pr. gigabyte ligger i gennemsnit på
{f"{S['gns_prgb']:.2f}".replace(".", ",")} kr., men det bedste tilbud i markedet ligger på
{f"{S['bedste_prgb']:.2f}".replace(".", ",")} kr. Der er altså en faktor seks til otte
mellem det gennemsnitlige og det bedste køb, hvis du måler på data alene.</p>

<p>Tre ting er blevet standard og bør ikke koste ekstra:</p>

<ul>
<li><strong>Ingen binding.</strong> {S['uden_binding']} ud af {S['antal']} abonnementer er
uden bindingsperiode.</li>
<li><strong>eSIM.</strong> {S['med_esim']} udbydere tilbyder det, så du kan være i gang
samme dag. <a href="/guides/esim/">Se hvordan eSIM virker</a>.</li>
<li><strong>5G.</strong> {S['med_5g']} abonnementer inkluderer det uden tillæg.</li>
</ul>

<p>Til gengæld er EU-data værd at kigge på. Gennemsnittet ligger på {S['gns_eu']} GB, altså
markant lavere end datamængden i Danmark. Rejser du, er det den kolonne, du skal tjekke
først. <a href="/guides/mobilabonnement-i-udlandet/">Læs om roaming og EU-regler</a>.</p>

{t['prisfordeling']}

<h2>Hvad koster et mobilabonnement til forskellige typer brugere?</h2>

<table>
<thead><tr><th>Bruger</th><th>Typisk behov</th><th>Realistisk pris</th></tr></thead>
<tbody>
<tr><td><strong>Barn eller let bruger</strong></td><td>Under 5 GB, mest wi-fi</td><td>{S['min']}–50 kr./md.</td></tr>
<tr><td><strong>Almindelig bruger</strong></td><td>10–20 GB, fri tale</td><td>50–90 kr./md.</td></tr>
<tr><td><strong>Pendler</strong></td><td>30–50 GB</td><td>70–110 kr./md.</td></tr>
<tr><td><strong>Storforbruger</strong></td><td>100 GB eller mere</td><td>90–140 kr./md.</td></tr>
<tr><td><strong>Uden fastnet</strong></td><td>Fri data, hotspot</td><td>110–{S['maks']} kr./md.</td></tr>
</tbody>
</table>

<p>Bemærk hvor lille springet er mellem kategorierne. Fra almindelig bruger til
storforbruger fordobles prisen sjældent, mens datamængden femdobles. Det er hovedgrunden
til, at vi anbefaler ét trin over dit målte forbrug — prisen for at ramme for lavt er
højere end prisen for at ramme lidt for højt.</p>

<h2>Hvad koster det over et år og over tre?</h2>

<table>
<thead><tr><th>Månedspris</th><th>Pr. år</th><th>Over 3 år</th><th>For en husstand med 2</th></tr></thead>
<tbody>
<tr><td>{S['min']} kr.</td><td>{S['min'] * 12} kr.</td><td>{S['min'] * 36} kr.</td><td>{S['min'] * 72} kr.</td></tr>
<tr><td>{S['median']} kr. (median)</td><td>{S['median'] * 12} kr.</td><td>{S['median'] * 36} kr.</td><td>{S['median'] * 72} kr.</td></tr>
<tr><td>{S['gns']} kr. (gennemsnit)</td><td>{S['gns'] * 12} kr.</td><td>{S['gns'] * 36} kr.</td><td>{S['gns'] * 72} kr.</td></tr>
<tr><td>{S['maks']} kr.</td><td>{S['maks'] * 12} kr.</td><td>{S['maks'] * 36} kr.</td><td>{S['maks'] * 72} kr.</td></tr>
</tbody>
</table>

<p>Forskellen mellem det billigste og det dyreste er
{(S['maks'] - S['min']) * 36} kr. over tre år for én person. For en husstand med to
abonnementer er det {(S['maks'] - S['min']) * 72} kr. Det er penge, der ikke kræver en
livsstilsændring at spare — kun tyve minutters opmærksomhed.</p>

<h2>Hvorfor er priserne så forskellige?</h2>

<p>Fire ting forklarer stort set hele prisspændet:</p>

<ol class="trin">
<li><strong>Datamængde</strong>
Den største enkeltfaktor, men ikke lineær. Prisen pr. gigabyte falder kraftigt, jo større
pakken er.</li>
<li><strong>Netværk</strong>
Der findes kun tre mobilnet i Danmark. Det mest udbyggede koster typisk mere at leje sig
ind på, og det slår igennem på prisen. <a href="/netvaerk/">Se de tre net</a>.</li>
<li><strong>Kundeservice</strong>
Discountudbydere har skåret telefonisk support og butikker væk. Det er en reel besparelse
for dig, hvis du ikke bruger dem — og en reel risiko, hvis du gør.</li>
<li><strong>Tillægsydelser</strong>
Streaming, musik og forsikring lægges oveni. Bruger du dem ikke, betaler du for luft.
<a href="/mobilabonnement-med-streaming/">Se hvad streaming reelt koster ekstra</a>.</li>
</ol>

<h2>Betaler danskerne for meget?</h2>

<p>Vores data siger ja for manges vedkommende, og af én bestemt grund: intropriser der
udløber uden at nogen reagerer.</p>

<p>Med {S['andel_intro']} % af markedet på kampagnepris og en gennemsnitlig stigning på
{S['gns_stigning']} kr., når perioden slutter, sidder en stor gruppe på en pris, de aldrig
aktivt har valgt. De valgte introprisen. Normalprisen kom af sig selv.</p>

<p>Den nemmeste kontrol tager to minutter: find din seneste regning, sammenlign beløbet med
medianen på {S['median']} kr., og se om du får noget for forskellen. Gør du ikke,
<a href="/guides/skift-mobilselskab/">er skiftet gjort på under en time</a> — og du beholder
dit nummer.</p>

<div class="tip">
<h3>Prøv at forhandle først</h3>
<p>Ring til dit selskab og sig, at du overvejer at skifte. De fleste har en
fastholdelsesafdeling, der kan give dig samme pris som nye kunder. Det tager ti minutter og
lykkes overraskende ofte, netop fordi det koster dem mere at skaffe en ny kunde end at
beholde dig. <a href="/guides/prisstigning-mobilabonnement/">Læs mere om dine
rettigheder</a>.</p>
</div>

<h2>Sådan har vi regnet</h2>

<p>Tallene på denne side er beregnet på {S['antal']} abonnementer fra de udbydere, vi har
datafeed fra. Vi bruger 12-måneders-prisen, altså intropris ganget med introperioden plus
normalpris for de resterende måneder, plus eventuelt oprettelsesgebyr, divideret med tolv.</p>

<p>Gennemsnittet er det aritmetiske gennemsnit af alle abonnementer, ikke vægtet efter
salgstal — vi kender ikke udbydernes salgsfordeling og foregiver ikke andet. Medianen er
derfor ofte det mere retvisende tal for "hvad koster et typisk abonnement".</p>

<p>Tallene opdateres automatisk, hver gang priserne ændrer sig. Se
<a href="/metode/">hele vores metode</a>.</p>
</section>
"""


def uden_kreditvurdering(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et almindeligt mobilabonnement kræver kreditvurdering, fordi
du bruger tjenesten først og betaler bagud. Vil du undgå vurderingen, skal du vælge en
løsning, hvor du betaler forud — et <strong>taletidskort</strong>. Der er ingen
kreditrisiko for udbyderen, og derfor intet opslag.</p>
</div>

<h2>Hvorfor kreditvurderer udbyderne?</h2>

<p>Et mobilabonnement er teknisk set en kredit. Du bruger data og taletid i en måned og
betaler bagud. Udbyderen løber altså en risiko for, at regningen ikke bliver betalt.</p>

<p>Den indsigt peger direkte på løsningen: fjerner du kreditrisikoen, fjerner du
kreditvurderingen. Det er præcis det, forudbetalte løsninger gør — og det er derfor, de
altid er tilgængelige uanset din betalingshistorik.</p>

<h2>Fire veje uden om kreditvurderingen</h2>

<table>
<thead><tr><th>Løsning</th><th>Kreditvurdering</th><th>Sandsynlighed</th><th>Ulempe</th></tr></thead>
<tbody>
<tr><td><strong>Taletidskort</strong></td><td>Nej</td><td>Meget høj</td><td>Højere pris pr. GB, du fylder selv op</td></tr>
<tr><td><strong>Forudbetalt abonnement</strong></td><td>Sjældent</td><td>Høj</td><td>Du betaler for flere måneder ad gangen</td></tr>
<tr><td><strong>Abonnement med depositum</strong></td><td>Ja, men med sikkerhed</td><td>Middel</td><td>Du binder et beløb</td></tr>
<tr><td><strong>Almindeligt abonnement</strong></td><td>Ja</td><td>Afhænger</td><td>Afslag efterlader spor</td></tr>
</tbody>
</table>

<p>Rækkefølgen er ikke tilfældig. Start øverst. Hver ansøgning udløser et opslag, og mange
opslag på kort tid kan i sig selv tælle imod dig hos den næste udbyder.</p>

<h2>Taletid er den sikre vej</h2>

<p>Med taletid fylder du penge på forud. Der er ingen regning, der kan udeblive, og derfor
ingen grund for udbyderen til at tjekke noget som helst.</p>

<p>Prisen pr. gigabyte er højere end på et abonnement, men forskellen bliver mindre, hvis du
køber datapakker frem for at betale løbende takst. Se vores gennemgang af
<a href="/taletidskort/">taletidskort og hvornår de betaler sig</a>.</p>

<div class="tip">
<h3>Du beholder dit nummer</h3>
<p>Skifter du fra abonnement til taletid — eller den anden vej senere — følger dit nummer
med. Nummerportering er en rettighed i Danmark og gælder begge veje.</p>
</div>

<h2>Bed om en manuel vurdering</h2>

<p>Bliver du afvist automatisk online, er det ikke nødvendigvis det endelige svar. Ringer du
til kundeservice og beder om en manuel vurdering, kan en sagsbehandler se på et bredere
billede end det rene ja eller nej fra databasen.</p>

<p>Det hjælper at være forberedt: kend din situation, vid om en eventuel registrering er
under afvikling, og overvej om du kan stille et depositum. Det er ingen garanti, men det er
en reel mulighed, mange ikke kender.</p>

<h2>Hvad kigger udbyderen på?</h2>

<ul>
<li><strong>Registrering som dårlig betaler.</strong> Det tungeste enkeltpunkt. Se vores
gennemgang af <a href="/guides/mobilabonnement-trods-rki/">mobilabonnement trods RKI</a>.</li>
<li><strong>Antal nylige opslag.</strong> Mange ansøgninger på kort tid ser ud som
økonomisk pres.</li>
<li><strong>Alder og folkeregisteradresse.</strong> Er du under 18, kræves der typisk en
forælder som medunderskriver.</li>
<li><strong>Hardware på afbetaling.</strong> Telefon med i aftalen vurderes markant
strengere, fordi beløbet er større. <a href="/mobilabonnement-med-telefon/">Køb den
kontant i stedet</a>.</li>
</ul>

<div class="advarsel">
<p><strong>Pas på lister med "udbydere der siger ja".</strong> Flere sider udgiver navne på
selskaber, der angiveligt godkender alle. Ingen dansk udbyder offentliggør sine
kreditkriterier, de ændrer sig løbende, og vurderingen er individuel. Følger du en sådan
liste, risikerer du en række afslag, hvor hvert eneste efterlader et spor.</p>
</div>

<h2>Til dig under 18</h2>

<p>Er du under 18, kan du normalt ikke indgå en abonnementsaftale alene. En forælder skal
stå som aftalepart. Taletid er derimod muligt, fordi der ikke er nogen kredit involveret —
og det er samtidig den tryggeste løsning, fordi regningen ikke kan løbe løbsk.</p>

<p>Se vores side om <a href="/mobilabonnement-til-boern/">mobilabonnement til børn</a> for
de indstillinger, der forhindrer overraskelser.</p>

<h2>Dine rettigheder</h2>

<ul>
<li><strong>Nødopkald virker altid.</strong> 112 kan ringes fra enhver telefon med simkort,
uanset saldo og abonnement.</li>
<li><strong>Du har ret til en begrundelse.</strong> Afvises du på baggrund af et opslag i et
kreditoplysningsbureau, skal du have oplyst hvilket bureau der er brugt.</li>
<li><strong>Du har ret til indsigt</strong> i det, der er registreret om dig, og til at få
rettet forkerte oplysninger.</li>
<li><strong>En registrering forsvinder.</strong> Når gælden er betalt, skal den slettes.</li>
</ul>
</section>
"""


def familie(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Der findes sjældent ægte familierabatter på det danske
mobilmarked. Til gengæld er de billigste abonnementer så billige, at fire separate
discountabonnementer typisk koster mindre end én familiepakke hos en premiumudbyder. Regn
på totalen, ikke på rabatprocenten.</p>
</div>

<h2>Familierabat er ofte en illusion</h2>

<p>Familiepakker markedsføres med en rabat pr. ekstra simkort. Det lyder som en besparelse,
men rabatten regnes af en udgangspris, der i forvejen ligger over markedet.</p>

<p>Regnestykket, du skal lave, er simpelt: gang prisen på det billigste abonnement, der
dækker hvert familiemedlems behov, og sammenlign totalen med familiepakken. I langt de
fleste tilfælde vinder de separate abonnementer.</p>

<div class="tip">
<h3>Et eksempel</h3>
<p>To voksne med 30-50 GB og to børn med 5-10 GB. Vælger du separate abonnementer fra den
billige ende, lander I typisk på 200-280 kr. samlet om måneden. En familiepakke med
tilsvarende data hos en premiumudbyder ligger ofte over 500 kr. Forskellen er 3.000 kr. om
året — for den samme dækning, fordi begge kører på et af landets tre net.</p>
</div>

<h2>Hvornår giver en familiepakke alligevel mening?</h2>

<ul>
<li><strong>Delt datapulje.</strong> Har I meget forskelligt forbrug fra måned til måned,
kan en fælles pulje være praktisk. Det er den ene reelle fordel.</li>
<li><strong>Én regning.</strong> Administrativt lettere, hvis I er mange.</li>
<li><strong>Samlerabat med bredbånd eller tv.</strong> Har I i forvejen andre produkter hos
samme selskab, kan den samlede pris blive konkurrencedygtig.</li>
<li><strong>Kundeservice ét sted.</strong> Værd noget, hvis I ikke selv vil håndtere fire
forskellige selskaber.</li>
</ul>

<p>Bemærk at ingen af punkterne handler om pris pr. gigabyte. De handler om bekvemmelighed —
og det er fint, så længe du ved, hvad bekvemmeligheden koster.</p>

<h2>Sådan sammensætter du husstandens abonnementer</h2>

<ol class="trin">
<li><strong>Mål hvert enkelt forbrug</strong>
Ikke husstandens samlede. Familiemedlemmer bruger meget forskelligt, og den mest
dataslugende bør ikke bestemme alles abonnement.
<a href="/guides/hvor-meget-data/">Sådan finder du tallet</a>.</li>
<li><strong>Vælg efter behov, ikke ens</strong>
Der er ingen grund til, at alle har samme pakke. Et barn med 5 GB og en voksen med 50 GB er
den rigtige løsning, ikke et kompromis i midten.</li>
<li><strong>Tjek dækningen ét sted</strong>
I bor samme sted, så nettet skal passe til adressen.
<a href="/daekningskort/">Tjek dækningen her</a>.</li>
<li><strong>Slå datastop til på alle</strong>
Særligt på børnenes. Det er den ene indstilling, der forhindrer chokregninger.</li>
<li><strong>Sæt én fælles påmindelse</strong>
Har flere af jer intropriser, så noter datoerne samme sted. Ellers glider I op i pris uden
at opdage det.</li>
</ol>

<h2>Ekstra simkort til samme nummer</h2>

<p>Flere udbydere tilbyder et ekstra simkort, der deler abonnementets data — typisk til et
ur, en tablet eller en bil. Det er ikke det samme som et familieabonnement, men det er ofte
billigere end et selvstændigt abonnement til enheden.</p>

<p>Tjek to ting: om det ekstra kort deler datapuljen eller har sin egen, og om det koster et
månedligt gebyr. Deler det puljen, er det den samme datamængde, der nu skal dække flere
enheder.</p>

<h2>Til børnene i husstanden</h2>

<p>Til et barns første telefon er tryghed vigtigere end pris. De to ting, der betyder mest,
er datastop og spærring for overtakserede numre — begge er gratis og tager under et minut
at slå til.</p>

<p>Overvej også taletid frem for abonnement. Regningen kan ikke overskrides, og barnet
lærer at forholde sig til et synligt forbrug. Se
<a href="/mobilabonnement-til-boern/">mobilabonnement til børn</a> og
<a href="/taletidskort/">taletidskort</a>.</p>

<h2>Skal alle skifte samtidig?</h2>

<p>Nej, og det er ofte en fordel at lade være. Skifter I én ad gangen, kan I mærke, om
dækningen holder, før hele husstanden er flyttet. Har I forskellige bindingsperioder, er
det alligevel nødvendigt.</p>

<p>Nummerportering fungerer individuelt, så der er ingen teknisk grund til at samle det.
<a href="/guides/skift-mobilselskab/">Se hvordan skiftet foregår</a>.</p>
</section>
"""


def opsigelse(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Skifter du til et nyt selskab, skal du <strong>ikke</strong>
opsige selv — den nye udbyder klarer det som en del af nummerflytningen. Opsiger du selv
først, mister du dit nummer. Vil du helt ud af et abonnement uden at få et nyt, opsiger du
direkte hos udbyderen.</p>
</div>

<div class="advarsel">
<p><strong>Den dyreste fejl på hele dette site:</strong> at opsige sit gamle abonnement, før
det nye er bestilt. Nummeret bliver frigivet, og så kan det ikke flyttes med. Det kan i
værste fald ikke genskabes.</p>
</div>

<h2>To situationer — to fremgangsmåder</h2>

<table>
<thead><tr><th></th><th>Du skifter til et nyt selskab</th><th>Du vil helt ud</th></tr></thead>
<tbody>
<tr><td><strong>Hvem opsiger?</strong></td><td>Den nye udbyder</td><td>Dig selv</td></tr>
<tr><td><strong>Beholder du nummeret?</strong></td><td>Ja, automatisk</td><td>Nej, det frigives</td></tr>
<tr><td><strong>Hvad gør du?</strong></td><td>Bestiller hos den nye og oplyser dit nummer</td><td>Kontakter udbyderen skriftligt</td></tr>
<tr><td><strong>Hvornår stopper det gamle?</strong></td><td>Når nummeret er flyttet</td><td>Efter opsigelsesvarslet</td></tr>
<tr><td><strong>Risiko</strong></td><td>Meget lav</td><td>Nummeret er tabt</td></tr>
</tbody>
</table>

<h2>Sådan opsiger du korrekt</h2>

<ol class="trin">
<li><strong>Find dit opsigelsesvarsel</strong>
Det står i abonnementsvilkårene, typisk under opsigelse. Mange abonnementer kan opsiges med
en måneds varsel til udgangen af en måned. Har du binding, gælder den først.</li>
<li><strong>Tjek om du har binding tilbage</strong>
Log ind i udbyderens app eller selvbetjening. Har du telefon på afbetaling, løber den
videre — restgælden skal typisk indfries.</li>
<li><strong>Opsig skriftligt</strong>
Brug selvbetjeningen eller send en mail, så du har dokumentation for datoen. Gem
kvitteringen.</li>
<li><strong>Bekræft at det er registreret</strong>
Følg op efter et par dage, hvis du ikke har fået en bekræftelse. Det er her, tvister
opstår.</li>
<li><strong>Tjek den sidste regning</strong>
Der kan komme en afsluttende opgørelse med forbrug fra den sidste periode.</li>
</ol>

<h2>Hvad koster det at opsige?</h2>

<p>Selve opsigelsen er gratis. De omkostninger, der kan opstå, er tre:</p>

<ul>
<li><strong>Restbinding.</strong> Er du bundet, skal de resterende måneder typisk betales.
Blandt de abonnementer, vi følger, er {D['antal_uden_binding']} ud af {D['antal']} helt uden
binding. <a href="/mobilabonnement-uden-binding/">Se dem her</a>.</li>
<li><strong>Restgæld på telefon.</strong> Hardware er en separat aftale, der ikke ophører,
fordi abonnementet gør.</li>
<li><strong>Opsigelsesvarsel.</strong> Du betaler for den periode, varslet løber — også hvis
du er holdt op med at bruge abonnementet.</li>
</ul>

<div class="tip">
<h3>Vil du bare have en lavere pris?</h3>
<p>Så prøv at ringe og sige det, før du opsiger. De fleste selskaber har en
fastholdelsesafdeling med mulighed for at matche prisen til nye kunder. Det tager ti
minutter, og du slipper for at skifte.
<a href="/guides/prisstigning-mobilabonnement/">Læs mere</a>.</p>
</div>

<h2>Fortrydelsesret ved onlinekøb</h2>

<p>Har du bestilt abonnementet online, har du som udgangspunkt fortrydelsesret efter
forbrugeraftaleloven. Fristen løber fra aftalens indgåelse.</p>

<p>Bemærk at fortrydelsesret og opsigelse er to forskellige ting. Fortrydelse annullerer
aftalen, som om den aldrig var indgået. Opsigelse afslutter en løbende aftale efter dens
egne vilkår. Er du inden for fortrydelsesfristen, er det den, du skal bruge — den er
hurtigere og billigere.</p>

<h2>Hvis udbyderen ikke reagerer</h2>

<p>Klag først skriftligt til selskabet og gem korrespondancen. Får du ikke medhold — eller
intet svar inden for rimelig tid — kan sagen indbringes for Teleankenævnet. Klagegebyret er
175 kr. og refunderes, hvis du får helt eller delvist medhold.</p>

<h2>Husk at hente dine ting</h2>

<ul>
<li><strong>Voicemail-beskeder</strong> forsvinder med abonnementet.</li>
<li><strong>Mailadresser</strong> hos udbyderen lukkes typisk ned.</li>
<li><strong>Streamingtjenester i pakken</strong> stopper. Din profil hos tjenesten
overlever, men adgangen gør ikke.</li>
<li><strong>Tofaktorkoder</strong> sendes til dit nummer. Skifter du nummer, skal du opdatere
bank, MitID og andre tjenester først.</li>
</ul>

<p>Det sidste punkt er det vigtigste og bliver oftest glemt. Flytter du dit nummer med, sker
der ingenting. Får du et nyt, skal du gennemgå alle tjenester, der sender koder på sms.</p>
</section>
"""


def erhverv(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Erhvervsabonnementer prissættes eksklusive moms, hvilket får
dem til at se billigere ud end de er. Sammenlign altid inklusive moms mod et privat
abonnement. For en enkeltmandsvirksomhed eller et lille firma er et almindeligt
discountabonnement ofte billigere — også efter momsfradrag.</p>
</div>

<h2>Momsfælden i sammenligningen</h2>

<p>Erhvervspriser oplyses uden moms. Et abonnement til 149 kr. ekskl. moms koster 186 kr.
inkl. moms. Sammenligner du de 149 med et privatabonnement til 89 kr., sammenligner du to
forskellige ting.</p>

<p>Er du momsregistreret, kan du trække momsen fra, og så er de 149 kr. den reelle
udgift. Er du ikke, betaler du 186 kr. Regn derfor altid ud fra din egen momssituation, før
du beslutter.</p>

<div class="tip">
<h3>Tommelfingerreglen</h3>
<p>Er du momsregistreret og har brug for support i arbejdstiden, kan erhverv give mening.
Er du ikke momsregistreret, eller klarer du dig selv teknisk, er et privat
discountabonnement næsten altid billigere.
<a href="/billigste-mobilabonnement/">Se priserne her</a>.</p>
</div>

<h2>Hvad får du reelt ekstra?</h2>

<table>
<thead><tr><th>Ydelse</th><th>Findes på privat?</th><th>Værd at betale for?</th></tr></thead>
<tbody>
<tr><td>Prioriteret kundeservice</td><td>Sjældent</td><td>Ja, hvis nedetid koster dig penge</td></tr>
<tr><td>Én samlet faktura for flere numre</td><td>Nej</td><td>Ja, ved mere end tre-fire numre</td></tr>
<tr><td>Administrationsportal</td><td>Nej</td><td>Ja, ved mange medarbejdere</td></tr>
<tr><td>Fast kontaktperson</td><td>Nej</td><td>Afhænger af størrelse</td></tr>
<tr><td>5G og EU-roaming</td><td>Ja</td><td>Nej, det er standard</td></tr>
<tr><td>Ingen binding</td><td>Ja</td><td>Nej, det er standard privat</td></tr>
</tbody>
</table>

<p>Læg mærke til de to nederste rækker. 5G og fravær af binding sælges nogle gange som
erhvervsfordele, men er standard på privatmarkedet. Det er ikke noget, du skal betale
ekstra for.</p>

<h2>Hvornår giver erhverv mening?</h2>

<ul>
<li><strong>Fra cirka fem numre.</strong> Under det er administrationen sjældent besværet
værd.</li>
<li><strong>Når nedetid koster penge.</strong> Er telefonen dit arbejdsredskab, er
prioriteret support pengene værd.</li>
<li><strong>Ved international brug.</strong> Erhvervsaftaler har ofte bedre vilkår uden for
EU, hvor privatabonnementer er dyrest.</li>
<li><strong>Når medarbejdere kommer og går.</strong> En portal, hvor du selv kan oprette og
lukke numre, sparer tid.</li>
</ul>

<h2>Hvornår gør det ikke?</h2>

<p>Er du enkeltmandsvirksomhed, freelancer eller har under fem numre, er svaret som regel
nej. Du betaler for en administrationsstruktur, du ikke har brug for, og du kan trække
momsen fra på et privatabonnement på nøjagtig samme måde, hvis det bruges erhvervsmæssigt.</p>

<p>Tjek i stedet, om dit nuværende privatabonnement dækker behovet. Med
{D['antal_uden_binding']} af {D['antal']} abonnementer uden binding kan du skifte, så snart
behovet ændrer sig.</p>

<h2>Skat og fri telefon</h2>

<p>Stiller virksomheden en telefon til rådighed for privat brug, udløser det beskatning af
fri telefon efter gældende regler. Beløbet fastsættes årligt, og det er et område, hvor
reglerne har ændret sig flere gange.</p>

<p>Vi giver ikke skatterådgivning, og du bør tjekke de aktuelle satser hos Skattestyrelsen
eller din revisor, før du beslutter, hvordan telefonen skal håndteres. Fejl her koster
typisk mere end forskellen mellem to abonnementer.</p>

<h2>Sådan sammenligner du rigtigt</h2>

<ol class="trin">
<li><strong>Læg moms på erhvervsprisen</strong>
Gang med 1,25. Nu kan du sammenligne med private priser.</li>
<li><strong>Træk momsfradraget fra igen, hvis du er momsregistreret</strong>
Så har du din reelle udgift.</li>
<li><strong>Gang med antal numre</strong>
Det er totalen, der betyder noget — ikke prisen pr. abonnement.</li>
<li><strong>Læg værdien af support på</strong>
Vurdér hvad en times nedetid koster dig. Er det mere end prisforskellen om måneden, er
erhverv billigt.</li>
</ol>

<p>Vores sammenligning dækker privatmarkedet, og priserne på siden er inklusive moms. Vil du
se, hvad et tilsvarende privatabonnement koster, så start på
<a href="/billigste-mobilabonnement/">billigste mobilabonnement</a>.</p>
</section>
"""
