# -*- coding: utf-8 -*-
"""Fem nye artikler. Hver med datatabeller, interne links og kildeangivelser."""

from skabelon import kr


def rki(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et almindeligt mobilabonnement kræver som regel en
kreditvurdering, og en aktiv RKI-registrering fører oftest til afslag. Men du kan altid få
et <strong>taletidskort</strong>, fordi du betaler forud — der er ingen kreditrisiko for
udbyderen og dermed ingen kreditvurdering. Telefon på afbetaling er derimod en kreditaftale
og bliver næsten altid afvist. Køb telefonen kontant eller brugt.</p>
</div>

<div class="advarsel">
<p><strong>Vær kritisk over for lister med "selskaber der siger ja til RKI".</strong> Flere
sider udgiver navne på udbydere, der angiveligt godkender kunder med RKI. Ingen dansk
udbyder offentliggør sine kreditkriterier, de ændrer sig løbende, og vurderingen er
individuel. En liste kan derfor sende dig ud i en række afslag, hvor hvert eneste opslag
efterlader et spor. Vi navngiver ingen udbydere her — vi viser i stedet de veje, der
virker uanset selskab.</p>
</div>

<h2>Hvorfor kreditvurderer udbyderne overhovedet?</h2>

<p>Et mobilabonnement er teknisk set en kredit. Du bruger tjenesten i en måned og betaler
bagud. Udbyderen løber altså en risiko for, at regningen ikke bliver betalt, og derfor
tjekker de din betalingshistorik, før de siger ja.</p>

<p>Det er værd at forstå, fordi det peger direkte på løsningen: fjerner du kreditrisikoen,
fjerner du kreditvurderingen. Det er præcis dét, forudbetalte løsninger gør.</p>

<h2>De fire veje — og hvor sandsynlige de er</h2>

<table>
<thead><tr><th>Løsning</th><th>Kreditvurdering?</th><th>Sandsynlighed med RKI</th><th>Ulempe</th></tr></thead>
<tbody>
<tr><td><strong>Taletidskort</strong></td><td>Nej</td><td>Meget høj</td><td>Højere pris pr. GB, du skal selv fylde op</td></tr>
<tr><td><strong>Abonnement med depositum</strong></td><td>Ja, men med sikkerhed</td><td>Middel</td><td>Du binder et beløb, ofte flere måneders forbrug</td></tr>
<tr><td><strong>Abonnement med forudbetaling</strong></td><td>Ofte lempeligere</td><td>Middel</td><td>Du betaler for flere måneder ad gangen</td></tr>
<tr><td><strong>Almindeligt abonnement</strong></td><td>Ja</td><td>Lav</td><td>Afslag efterlader spor i din historik</td></tr>
<tr><td><strong>Telefon på afbetaling</strong></td><td>Ja, streng</td><td>Meget lav</td><td>Reelt et lån — afvises næsten altid</td></tr>
</tbody>
</table>

<p>Rækkefølgen er ikke tilfældig. Start øverst. Hver gang du søger og får afslag, sker der
et opslag, og for hyppige opslag kan i sig selv trække ned hos den næste udbyder. Søg
derfor ikke bredt — søg målrettet på den løsning, der har den højeste sandsynlighed.</p>

<h2>Taletidskort er den sikre vej</h2>

<p>Med taletid betaler du forud. Der er ingen regning, der kan udeblive, og derfor ingen
grund for udbyderen til at tjekke din historik. Det gør taletid til den eneste løsning, der
i praksis altid er tilgængelig, uanset registrering.</p>

<p>Prisen er højere pr. gigabyte end på et abonnement, men forskellen er mindre, end mange
tror, hvis du køber datapakker frem for at betale løbende takst. Se vores gennemgang af
<a href="/taletidskort/">taletidskort og hvornår de kan betale sig</a>.</p>

<div class="tip">
<h3>Behold dit nummer</h3>
<p>Skifter du fra et almindeligt abonnement til taletid — eller den anden vej senere — kan
du beholde dit mobilnummer. Nummerportering er en rettighed i Danmark og gælder begge veje.
Du mister altså ikke dit nummer ved at gå over på taletid.</p>
</div>

<h2>Bed om en manuel vurdering</h2>

<p>Bliver du afvist automatisk online, er det ikke nødvendigvis det endelige svar. Ringer du
til kundeservice og beder om en manuel kreditvurdering, kan sagsbehandleren se på et bredere
billede end det rene ja/nej fra databasen.</p>

<p>Det hjælper at kunne oplyse: hvad registreringen drejer sig om, om den er under
afvikling, og om du kan stille et depositum. Vær konkret og forbered dig, før du ringer. Det
er ikke en garanti, men det er en reel mulighed, som mange ikke kender.</p>

<h2>Tjek din egen registrering først</h2>

<p>Der findes to store registre i Danmark, og de er ikke ens. RKI drives af Experian, mens
Debitor Registret drives af Dun &amp; Bradstreet (tidligere Bisnode). En kreditor kan have
registreret dig i det ene og ikke i det andet, og de fleste udbydere slår op i begge.</p>

<ol class="trin">
<li><strong>Få indsigt i dine registreringer</strong>
Du har efter databeskyttelsesreglerne ret til at få oplyst, hvad der er registreret om dig.
Kontakt registrene direkte for indsigt.</li>
<li><strong>Tjek om registreringen er korrekt</strong>
Forældede eller fejlagtige registreringer forekommer. Er beløbet betalt, skal kreditor
slette registreringen.</li>
<li><strong>Kend fristerne</strong>
En registrering slettes, når gælden er betalt, og senest efter en periode fastsat i
reglerne for kreditoplysningsbureauer. Har du betalt, så følg op på, at sletningen er sket
— den sker ikke altid automatisk.</li>
<li><strong>Vent hvis du er tæt på sletning</strong>
Er du få uger fra at blive slettet, står du markant stærkere ved at vente med at søge end
ved at samle afslag.</li>
</ol>

<h2>Telefonen: køb den kontant</h2>

<p>Telefon på afbetaling er en kreditaftale og den sværeste del at få igennem. Den gode
nyhed er, at du slet ikke har brug for den.</p>

<p>En brugt eller renoveret telefon fra et par år tilbage koster typisk halvdelen af en ny
og fungerer fint til alt almindeligt brug. Køber du den kontant, undgår du både
kreditvurderingen og en bindingsperiode på 24-36 måneder. Se regnestykket i vores gennemgang
af <a href="/mobilabonnement-med-telefon/">telefon på afbetaling</a>.</p>

<h2>Dine rettigheder</h2>

<ul>
<li><strong>Nødopkald virker altid.</strong> 112 kan ringes fra enhver telefon med et
simkort, uanset saldo, abonnement eller registrering.</li>
<li><strong>Du har ret til indsigt</strong> i de oplysninger, der er registreret om dig, og
til at få rettet forkerte oplysninger.</li>
<li><strong>Du skal have en begrundelse.</strong> Afvises du på baggrund af et opslag i et
kreditoplysningsbureau, har du krav på at få oplyst, hvilket bureau der er brugt.</li>
<li><strong>En registrering forsvinder.</strong> Når gælden er betalt, skal registreringen
slettes. Den følger dig ikke resten af livet.</li>
</ul>

<div class="tip">
<h3>Har du brug for hjælp til gælden?</h3>
<p>Er registreringen del af en større økonomisk situation, findes der gratis og uvildig
gældsrådgivning i Danmark gennem flere organisationer. Det er ofte et bedre første skridt
end at lede efter en udbyder, der siger ja — og det løser problemet frem for at flytte det.</p>
</div>
</section>
"""


def under100(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Der findes {D['antal_u100']} mobilabonnementer under 100 kr.
om måneden i vores sammenligning, og de starter ved {kr(D['min_pris'])} kr. Under 100 kr.
får du typisk fri tale, fri sms og mellem 5 og 60 GB data uden binding. Det billigste
abonnement med mobildata koster {kr(D['min_pris_data'])} kr. for
{D['min_data_gb']} GB.</p>
</div>

<h2>Hvad kan man reelt få for under 100 kr.?</h2>

<p>Mere end de fleste tror. Hundredekronen er ikke længere grænsen for et minimumsprodukt —
den dækker i dag et fuldt abonnement med fri tale, fri sms, 5G og datamængder, der rækker
til langt over gennemsnitsdanskerens forbrug.</p>

<p>Det skyldes, at konkurrencen i Danmark er hårdest netop i dette prisleje. Tyve selskaber
slås om de samme kunder mellem 50 og 99 kr., og det presser både prisen og datamængden. Går
du over 100 kr., betaler du typisk for noget andet end data: bedre netværk, streaming eller
kundeservice.</p>

<h2>Sådan fordeler abonnementerne under 100 kr. sig</h2>

<table>
<thead><tr><th>Prisniveau</th><th>Hvad du typisk får</th><th>Passer til</th></tr></thead>
<tbody>
<tr><td><strong>Under 40 kr.</strong></td><td>Taletid eller timepakke, ingen eller lidt data</td><td>Telefon nummer to, børn, meget let brug</td></tr>
<tr><td><strong>40–59 kr.</strong></td><td>Fri tale og 5–20 GB, ofte på intropris</td><td>Almindelig bruger med wi-fi det meste af dagen</td></tr>
<tr><td><strong>60–79 kr.</strong></td><td>Fri tale og 20–50 GB</td><td>Pendler og daglig bruger</td></tr>
<tr><td><strong>80–99 kr.</strong></td><td>Fri tale og 30–100 GB</td><td>Storforbruger uden behov for premiumnet</td></tr>
</tbody>
</table>

<div class="advarsel">
<p><strong>Pas på introprisen.</strong> En stor del af abonnementerne under 100 kr. er
kampagnepriser, der gælder i to til seks måneder. Derefter stiger de — nogle gange til
det dobbelte. Vores tabel viser derfor <strong>gennemsnitsprisen over 12 måneder</strong>,
så du kan se, hvilke abonnementer der reelt er under hundrede kroner hele vejen, og hvilke
der kun er det i starten.</p>
</div>

<h2>Hvad koster det over et år?</h2>

<p>Månedsprisen er den, der sælger. Årsprisen er den, der betyder noget for din økonomi.</p>

<table>
<thead><tr><th>Månedspris</th><th>Pris pr. år</th><th>Over 3 år</th><th>Forskel mod 199 kr./md.</th></tr></thead>
<tbody>
<tr><td>19 kr.</td><td>228 kr.</td><td>684 kr.</td><td>−6.480 kr.</td></tr>
<tr><td>49 kr.</td><td>588 kr.</td><td>1.764 kr.</td><td>−5.400 kr.</td></tr>
<tr><td>79 kr.</td><td>948 kr.</td><td>2.844 kr.</td><td>−4.320 kr.</td></tr>
<tr><td>99 kr.</td><td>1.188 kr.</td><td>3.564 kr.</td><td>−3.600 kr.</td></tr>
<tr><td>199 kr.</td><td>2.388 kr.</td><td>7.164 kr.</td><td>—</td></tr>
</tbody>
</table>

<p>For en husstand med to voksne fordobles tallene. Skiftet fra et premiumabonnement til et
under hundrede kroner er derfor en af de største enkeltbesparelser, der findes i et
almindeligt husholdningsbudget — og den tager under en time at gennemføre.</p>

<h2>Hvad giver du afkald på?</h2>

<div class="plusminus">
  <div class="pm pm-plus"><h3>Det får du stadig</h3><ul>
    <li>Fri tale og fri sms til danske numre</li>
    <li>5G på samme master som de dyre abonnementer</li>
    <li>EU-roaming inden for de gældende regler</li>
    <li>Ingen binding og som regel ingen oprettelse</li>
    <li>eSIM og mulighed for at beholde dit nummer</li>
  </ul></div>
  <div class="pm pm-minus"><h3>Det får du typisk ikke</h3><ul>
    <li>Bemandet telefonisk kundeservice hele døgnet</li>
    <li>Fysiske butikker at gå ind i</li>
    <li>Streamingtjenester i abonnementet</li>
    <li>Adgang til det mest udbyggede net i alle tilfælde</li>
    <li>Store datamængder i EU — loftet er ofte lavere</li>
  </ul></div>
</div>

<p>Er nogen af punkterne i højre kolonne vigtige for dig, så betal de ekstra hundrede
kroner. Er de ikke, betaler du for noget, du ikke bruger. Se vores gennemgang af
<a href="/bedste-mobilabonnement/">hvad der gør et abonnement godt</a>.</p>

<h2>Tre fælder i den billige ende</h2>

<ol class="trin">
<li><strong>Introprisen der udløber</strong>
Sæt en kalenderpåmindelse ved kampagneperiodens udløb, eller vælg et abonnement med fast
pris fra dag ét.</li>
<li><strong>For lidt data</strong>
Et abonnement til 49 kr. med 5 GB er ikke billigt, hvis du bruger 15 GB og køber ekstra
hver måned. Find dit faktiske forbrug først —
<a href="/guides/hvor-meget-data/">sådan gør du</a>.</li>
<li><strong>Forkert netværk</strong>
Bor du på landet, kan det billigste abonnement være ubrugeligt. Tjek dækningen på din
adresse, før du bestiller — <a href="/daekningskort/">se hvordan</a>.</li>
</ol>
</section>
"""


def bredbaand(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et mobilabonnement er til din telefon og følger dig rundt.
Bredbånd er til dit hjem og leveres via kabel eller fiber til adressen. Mobilt bredbånd er
en tredje ting: mobilnettet brugt som hjemmeforbindelse via en router eller et hotspot. For
en enkelt person med moderat forbrug kan et stort mobilabonnement erstatte bredbånd. For en
husstand med flere personer, streaming og hjemmearbejde kan det som regel ikke.</p>
</div>

<h2>De tre produkter, kort fortalt</h2>

<table>
<thead><tr><th></th><th>Mobilabonnement</th><th>Mobilt bredbånd</th><th>Fast bredbånd</th></tr></thead>
<tbody>
<tr><td><strong>Til hvad</strong></td><td>Telefonen</td><td>Hjemmet, via mobilnettet</td><td>Hjemmet, via kabel eller fiber</td></tr>
<tr><td><strong>Følger dig?</strong></td><td>Ja</td><td>Delvist — routeren kan flyttes</td><td>Nej, bundet til adressen</td></tr>
<tr><td><strong>Typisk hastighed</strong></td><td>Afhænger af dækning</td><td>Afhænger af dækning</td><td>Stabil og høj</td></tr>
<tr><td><strong>Datamængde</strong></td><td>Fra 5 GB til fri data</td><td>Ofte stor eller fri</td><td>Altid ubegrænset</td></tr>
<tr><td><strong>Installation</strong></td><td>Simkort</td><td>Router, ingen tekniker</td><td>Ofte tekniker og gravearbejde</td></tr>
<tr><td><strong>Flere brugere samtidig</strong></td><td>Begrænset</td><td>Middel</td><td>Godt</td></tr>
</tbody>
</table>

<h2>Kan et mobilabonnement erstatte dit bredbånd?</h2>

<p>Det kan det for nogle. Spørgsmålet afgøres af tre ting, og du skal svare ja til alle
tre, før det er en god idé.</p>

<ol class="trin">
<li><strong>Er dækningen god hos dig?</strong>
Mobilnettet svinger med afstand til masten, bygningens mure og hvor mange der er på nettet
samtidig. Bredbånd via kabel gør ikke. Tjek dækningen først —
<a href="/daekningskort/">se hvordan</a>.</li>
<li><strong>Er I få om forbindelsen?</strong>
En person, der streamer og browser, klarer sig fint. En husstand med fire personer, hvor to
er på videomøde og to streamer, gør ikke.</li>
<li><strong>Har du fri data eller en meget stor pakke?</strong>
Et hjem uden fastnet bruger let 150-300 GB om måneden. Med et abonnement på 50 GB løber du
tør midt i måneden.</li>
</ol>

<div class="tip">
<h3>Regn på det, før du opsiger noget</h3>
<p>Fri data koster fra {kr(D['pris_fri'])} kr. om måneden. Er det billigere end dit
bredbånd, og passer de tre svar ovenfor, kan du reelt spare pengene. Test det i en måned,
mens du stadig har bredbåndet, før du opsiger. Det er den eneste måde at finde ud af, om det
holder i praksis.</p>
</div>

<h2>Hotspot: sådan virker det</h2>

<p>Deler du din telefons forbindelse med en laptop eller et tv, kaldes det hotspot eller
internetdeling. Det fungerer teknisk godt på et moderne 5G-net, men der er tre forbehold
værd at kende.</p>

<ul>
<li><strong>Batteriet dræner hurtigt.</strong> Telefonen skal typisk være i opladeren, når
den bruges som router.</li>
<li><strong>Dataforbruget eksploderer.</strong> En laptop henter automatiske opdateringer og
streamer i højere opløsning end en telefon. Regn med langt mere, end du bruger på telefonen
alene.</li>
<li><strong>Tjek vilkårene.</strong> De fleste danske udbydere tillader hotspot, men enkelte
begrænser deling til andre enheder. Det står i abonnementsvilkårene.</li>
</ul>

<h2>Hvornår er hvad det rigtige?</h2>

<div class="kortgitter kg-3" style="margin:1.8rem 0">
  <div class="kort"><h3>Kun mobilabonnement</h3>
  <p>Enlig eller par uden meget streaming, god mobildækning, og fri data eller 150 GB+.
  Sparer hele bredbåndsregningen.</p></div>
  <div class="kort"><h3>Mobilt bredbånd</h3>
  <p>Sommerhus, midlertidig bolig, eller adresse hvor fiber ikke er trukket. Ingen
  installation, og routeren kan flyttes med.</p></div>
  <div class="kort"><h3>Fast bredbånd</h3>
  <p>Husstand med flere personer, hjemmearbejde, gaming eller meget streaming. Stabiliteten
  er det, du betaler for.</p></div>
</div>

<h2>Datamængder sammenlignet</h2>

<table>
<thead><tr><th>Husstand</th><th>Typisk månedsforbrug</th><th>Mobilabonnement rækker?</th></tr></thead>
<tbody>
<tr><td>Én person, mest telefon</td><td>20–50 GB</td><td>Ja, et stort abonnement er nok</td></tr>
<tr><td>Én person med laptop</td><td>80–150 GB</td><td>Ja, men kræver fri data</td></tr>
<tr><td>Par med streaming</td><td>200–400 GB</td><td>Grænsetilfælde — test først</td></tr>
<tr><td>Familie med børn</td><td>500 GB og opefter</td><td>Nej, vælg fast bredbånd</td></tr>
</tbody>
</table>

<p>Tallene er vejledende og afhænger især af, hvor meget video der ses, og i hvilken
opløsning. Ser I meget i 4K, ligger I i den høje ende af hvert interval.</p>

<h2>Hvis du vælger mobilen som hjemmeforbindelse</h2>

<p>Så vælg fri data, ikke en stor pakke. Forskellen i pris er mindre end risikoen for at
løbe tør, og du får friheden til ikke at holde øje. Se
<a href="/mobilabonnement-med-fri-data/">abonnementer med fri data</a> og tjek EU-loftet,
hvis du rejser.</p>
</section>
"""


def udlandet(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Inden for EU og EØS bruger du dit danske abonnement på
stort set samme vilkår som herhjemme — det kaldes roaming. Uden for EU gælder reglerne
ikke, og priserne kan være meget høje. Den mest almindelige dyre fejl er at forveksle
roaming med opkald til udlandet: at ringe fra Danmark til et udenlandsk nummer er ikke
dækket af fri tale hos de fleste udbydere.</p>
</div>

<h2>De tre situationer, der bliver blandet sammen</h2>

<table>
<thead><tr><th>Situation</th><th>Hvor er du?</th><th>Reguleret?</th><th>Typisk pris</th></tr></thead>
<tbody>
<tr><td><strong>Roaming i EU/EØS</strong></td><td>I udlandet</td><td>Ja</td><td>Som herhjemme, med loft på data</td></tr>
<tr><td><strong>Roaming uden for EU</strong></td><td>I udlandet</td><td>Nej</td><td>Udbyderens egne takster — kan være høje</td></tr>
<tr><td><strong>Opkald til udlandet</strong></td><td>I Danmark</td><td>Delvist</td><td>Ikke dækket af fri tale hos de fleste</td></tr>
</tbody>
</table>

<p>Læg mærke til nederste række. Det er den, der overrasker flest. Fri tale betyder fri tale
til <em>danske</em> numre. Ringer du fra din sofa i Aarhus til et nummer i Tyrkiet, er det
et udlandsopkald, og det afregnes efter en særskilt takst.</p>

<h2>Roaming i EU — det du skal vide</h2>

<p>Inden for EU og EØS kan du bruge dit danske abonnement til at ringe, sende sms og bruge
data på vilkår, der svarer til dem herhjemme. Det gælder også opkald til danske numre, mens
du er afsted.</p>

<p>Der er to forbehold, som står i vilkårene hos alle udbydere:</p>

<ul>
<li><strong>Nogle abonnementer har slet ingen EU-data.</strong> Det gælder især i den
billige ende. Vi markerer dem med "Ingen" i EU-kolonnen, så du kan se det, før du
bestiller.</li>
<li><strong>Loft på data.</strong> Din datamængde i EU er ofte lavere end i Danmark. Har du
fri data herhjemme, kan du have 30 eller 50 GB i EU. Det er den enkeltoplysning, flest
opdager for sent, og den står i EU-kolonnen i vores tabeller.</li>
<li><strong>Midlertidigt ophold.</strong> Reglerne dækker rejser, ikke permanent brug i et
andet land. Bor du reelt i udlandet og bruger et dansk abonnement hele året, kan udbyderen
efter en periode opkræve tillæg.</li>
</ul>

<h2>Uden for EU: her opstår de store regninger</h2>

<div class="advarsel">
<p><strong>Storbritannien, Schweiz, Tyrkiet, USA og resten af verden falder uden for
EU-reglerne.</strong> Her sætter udbyderen selv taksten, og både data, opkald og sms kan
koste mange gange mere end herhjemme. En enkelt ubemærket app-opdatering kan koste
hundredvis af kroner.</p>
</div>

<p>Sådan sikrer du dig, før du rejser:</p>

<ol class="trin">
<li><strong>Slå dataroaming fra</strong>
På iPhone under Mobildata, på Android under Mobilnetværk. Det er den vigtigste enkelte
indstilling, og den tager ti sekunder.</li>
<li><strong>Tjek taksten for netop dit land</strong>
Priserne varierer voldsomt. Din udbyders side har en landeliste.</li>
<li><strong>Bed om spærring eller forbrugsloft</strong>
Mange udbydere kan sætte et loft for roamingforbrug uden for EU. Ring og bed om det inden
afrejse.</li>
<li><strong>Køb et lokalt data-eSIM</strong>
Den billigste løsning på langt de fleste rejser. Du beholder dit danske nummer aktivt til
opkald og sms, mens data kører på en lokal pakke.
<a href="/guides/esim/">Se hvordan eSIM virker</a>.</li>
</ol>

<h2>Ringer du fast til udlandet fra Danmark?</h2>

<p>Så er det ikke roaming, du skal kigge på — det er et abonnement bygget til
udlandsopkald. Forskellen kan løbe op i hundredvis af kroner om måneden for en familie med
bånd til et andet land.</p>

<p>Når du sammenligner, så kig ikke på antallet af inkluderede minutter. Kig på tre ting:
hvilke lande der er dækket, om dækningen gælder mobilnumre eller kun fastnet, og hvad
minutter ud over pakken koster. To abonnementer med samme antal minutter kan være vidt
forskellige produkter. Se <a href="/landekoder/">alle landekoder</a> og vores gennemgang af
<a href="/mobilabonnement-med-fri-tale/">abonnementer med fri tale</a>.</p>

<h2>Hvor meget data bruger du på ferien?</h2>

<table>
<thead><tr><th>Aktivitet på rejsen</th><th>Ca. forbrug pr. dag</th><th>På en uge</th></tr></thead>
<tbody>
<tr><td>Kort, beskeder og lidt sociale medier</td><td>0,3–0,7 GB</td><td>2–5 GB</td></tr>
<tr><td>Plus billeder og video til familien</td><td>1–2 GB</td><td>7–14 GB</td></tr>
<tr><td>Plus streaming om aftenen</td><td>3–5 GB</td><td>21–35 GB</td></tr>
<tr><td>Telefonen som eneste internet</td><td>5–10 GB</td><td>35–70 GB</td></tr>
</tbody>
</table>

<p>De fleste ferierejsende lander i de to øverste rækker. Har du 20 GB eller mere til
rådighed i EU, skal du normalt ikke tænke over det. Ligger dit EU-loft under 10 GB, og
streamer du om aftenen, bør du enten hente indhold hjem på hotellets wi-fi eller købe et
lokalt eSIM.</p>
</section>
"""


def prisstigning(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Stiger prisen på dit mobilabonnement, har du som
udgangspunkt ret til at blive varslet i god tid, og du kan opsige aftalen, hvis ændringen
er til ugunst for dig. De fleste prisstigninger er ikke fejl — det er intropriser, der
udløber som aftalt. Tjek først, om du oprindeligt tegnede abonnementet på et tilbud.</p>
</div>

<h2>Find ud af hvilken type stigning det er</h2>

<p>Der er tre grunde til, at din regning pludselig er højere, og de kræver forskellige svar.</p>

<table>
<thead><tr><th>Type</th><th>Sådan genkender du den</th><th>Hvad du gør</th></tr></thead>
<tbody>
<tr><td><strong>Intropris udløbet</strong></td><td>Stigningen falder 2–6 mdr. efter oprettelse og rammer et rundt tal</td><td>Var aftalt fra start. Sammenlign markedet og skift</td></tr>
<tr><td><strong>Generel prisregulering</strong></td><td>Du har fået et varsel, ofte på sms eller mail</td><td>Du kan typisk opsige uden varsel, hvis den er til ugunst</td></tr>
<tr><td><strong>Overforbrug</strong></td><td>Stigningen er engangs og svinger fra måned til måned</td><td>Slå datastop til, og gå eventuelt op i datamængde</td></tr>
</tbody>
</table>

<p>Den første type er langt den hyppigste, og det er også den, folk oftest oplever som
uretfærdig. Den er dog aftalt på forhånd — den stod i vilkårene ved bestillingen. Det gør
den ikke mindre dyr, men det ændrer, hvad du kan gøre ved den.</p>

<h2>Dine rettigheder ved en varslet prisstigning</h2>

<ul>
<li><strong>Du skal varsles.</strong> Væsentlige ændringer til ugunst for dig skal varsles
inden ikrafttræden. Varslet kommer typisk på sms eller e-mail — tjek dit spamfilter.</li>
<li><strong>Du kan opsige.</strong> Er ændringen til ugunst, kan du som udgangspunkt opsige
aftalen i forbindelse med ændringen, også hvis du ellers ville have et varsel.</li>
<li><strong>Binding gælder stadig for hardware.</strong> Har du telefon på afbetaling, skal
restgælden typisk indfries, selvom du opsiger abonnementet.</li>
<li><strong>Du kan klage.</strong> Er du uenig med udbyderen, kan sagen indbringes for
Teleankenævnet, når du først har klaget skriftligt til selskabet og fået svar — eller ikke
har fået svar inden for rimelig tid, typisk op til tre måneder. Klagegebyret er 175 kr., og
du får det retur, hvis du får helt eller delvist medhold eller indgår forlig.</li>
</ul>

<div class="tip">
<h3>Det virker overraskende ofte at ringe</h3>
<p>Ring til dit selskab, sig at du overvejer at skifte, og spørg hvad de kan tilbyde. De
fleste selskaber har en fastholdelsesafdeling med mulighed for at give dig samme pris som
nye kunder. Det tager ti minutter og lykkes ofte — netop fordi det koster dem mere at skaffe
en ny kunde end at beholde dig.</p>
</div>

<h2>Sådan undgår du det næste gang</h2>

<ol class="trin">
<li><strong>Vælg fast pris frem for intropris</strong>
Et abonnement til 79 kr. hele vejen er ofte billigere over et år end et til 39 kr. i tre
måneder og 129 kr. derefter. Vores tabeller viser gennemsnittet over 12 måneder netop af
den grund.</li>
<li><strong>Sæt en påmindelse ved kampagnens udløb</strong>
Skriv datoen i kalenderen samme dag, du bestiller. Det er det enkleste værn, der findes.</li>
<li><strong>Tjek regningen én gang om året</strong>
Sæt en fast dato. Sammenlign din pris med, hvad tilsvarende abonnementer koster nye kunder
i dag.</li>
<li><strong>Undgå lang binding</strong>
Uden binding kan du reagere med det samme, når prisen stiger. Se
<a href="/mobilabonnement-uden-binding/">abonnementer uden binding</a>.</li>
</ol>

<h2>Regn på hvad stigningen koster dig</h2>

<table>
<thead><tr><th>Stigning pr. md.</th><th>Pr. år</th><th>Over 3 år</th><th>For en husstand med 2</th></tr></thead>
<tbody>
<tr><td>20 kr.</td><td>240 kr.</td><td>720 kr.</td><td>1.440 kr.</td></tr>
<tr><td>40 kr.</td><td>480 kr.</td><td>1.440 kr.</td><td>2.880 kr.</td></tr>
<tr><td>60 kr.</td><td>720 kr.</td><td>2.160 kr.</td><td>4.320 kr.</td></tr>
<tr><td>100 kr.</td><td>1.200 kr.</td><td>3.600 kr.</td><td>7.200 kr.</td></tr>
</tbody>
</table>

<p>En stigning på 40 kr. lyder ikke af meget på en enkelt regning. Over tre år for en
husstand med to abonnementer er det knap 3.000 kr. Det er derfor, det kan betale sig at
bruge de ti minutter, det tager at reagere.</p>

<h2>Skal du skifte eller forhandle?</h2>

<p>Forhandl først — det er hurtigst, og du beholder dit setup. Får du ikke markedsprisen,
så skift. Skiftet tager typisk 1-5 hverdage, du beholder dit nummer, og du skal ikke opsige
noget selv. Se <a href="/guides/skift-mobilselskab/">guiden til at skifte mobilselskab</a>
eller start med <a href="/billigste-mobilabonnement/">sammenligningen</a>.</p>
</section>
"""
