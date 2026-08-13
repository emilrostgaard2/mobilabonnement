# -*- coding: utf-8 -*-
"""Langt indhold til de seks kategorisider (del 1)."""

from skabelon import kr


def fri_tale(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Billigste mobilabonnement med fri tale koster
{kr(D['pris_fritale'])} kr. om måneden. Fri tale dækker ubegrænsede opkald til danske
mobil- og fastnetnumre, men <em>ikke</em> særnumre, udlandsopkald eller opkald til
tjenester med tillægstakst. Næsten alle abonnementer over cirka 50 kr. har fri tale
inkluderet, så i praksis handler valget om, hvor meget data du skal have ved siden af.</p>
</div>

<h2>Hvad betyder fri tale egentlig?</h2>

<p>Fri tale betyder ubegrænsede opkald fra Danmark til danske numre — både mobil og
fastnet. Der er ingen minuttæller, og der er ingen ekstraregning, uanset hvor længe du
taler. For langt de fleste danskere gør det spørgsmålet om taletid fuldstændig
uinteressant, og det er en af de største forskelle på det danske marked i dag og for ti
år siden, hvor minutpakker var normen.</p>

<p>Der er dog fire ting, fri tale som regel <em>ikke</em> dækker, og de er værd at kende,
fordi det er dem, der producerer overraskelser på regningen:</p>

<table>
<thead><tr><th>Ikke dækket</th><th>Hvad det er</th><th>Typisk pris</th></tr></thead>
<tbody>
<tr><td>Særnumre</td><td>Numre der starter med 90 og lignende servicenumre</td><td>Tillægstakst pr. minut</td></tr>
<tr><td>Opkald til udlandet</td><td>Når du ringer fra Danmark til et udenlandsk nummer</td><td>Varierer voldsomt fra land til land</td></tr>
<tr><td>Roaming uden for EU</td><td>Når du selv er uden for EU og ringer</td><td>Ofte meget høje minuttakster</td></tr>
<tr><td>Indholdstjenester</td><td>Sms-afstemninger, donationer, parkeringsapps</td><td>Faktureres separat</td></tr>
</tbody>
</table>

<p>Den vigtigste af dem er skellet mellem roaming og udlandsopkald, fordi de to ting
konstant bliver blandet sammen. Roaming er, når <em>du</em> befinder dig i udlandet og
bruger dit danske abonnement — og inden for EU er det reguleret, så det stort set virker
som herhjemme. Udlandsopkald er, når du sidder i Danmark og ringer til et nummer i et
andet land. Det er ikke reguleret, det er ikke inkluderet i fri tale, og priserne
varierer med flere hundrede procent mellem selskaberne.</p>

<div class="tip">
<h3>Ringer du fast til udlandet?</h3>
<p>Så skal du ikke lede efter fri tale — du skal lede efter et abonnement med
inkluderede udlandsminutter til netop dit land. Specialiserede udbydere kan spare dig
hundredvis af kroner om måneden i forhold til et almindeligt dansk abonnement med fri
tale. Tjek altid, om landelisten dækker mobilnumre eller kun fastnet, da det ofte
prissættes forskelligt.</p>
</div>

<h2>Fri tale mod timepakker — hvornår kan det betale sig?</h2>

<p>Nogle af de allerbilligste abonnementer på markedet har ikke fri tale, men en
timepakke: 3 timer, 5 timer eller lignende. De er markant billigere, og for en del
brugere er de reelt et bedre køb. Spørgsmålet er, hvor meget du faktisk taler.</p>

<p>Tre timers taletid svarer til cirka seks minutter om dagen. Det lyder af lidt, men for
en person, der primært kommunikerer via beskeder og kun ringer ved behov, er det
rigeligt. Fem timer svarer til ti minutter om dagen og dækker langt de fleste
almindelige brugere.</p>

<table>
<thead><tr><th>Du taler ca.</th><th>Vælg</th><th>Fordi</th></tr></thead>
<tbody>
<tr><td>Under 5 min./dag</td><td>Timepakke på 3 timer</td><td>Billigst, og du kommer ikke i nærheden af loftet</td></tr>
<tr><td>5–10 min./dag</td><td>Timepakke på 5 timer eller fri tale</td><td>Prisforskellen er lille — vælg fri tale for ro i sindet</td></tr>
<tr><td>Over 10 min./dag</td><td>Fri tale</td><td>Overforbrug på en timepakke koster hurtigt mere end forskellen</td></tr>
<tr><td>Svinger meget</td><td>Fri tale</td><td>En enkelt lang samtale kan sprænge en timepakke</td></tr>
</tbody>
</table>

<p>Vores generelle anbefaling er fri tale, med mindre du er sikker på, at du taler meget
lidt. Grunden er marginalprisen: forskellen mellem en timepakke og fri tale er sjældent
mere end 10–20 kr. om måneden, mens overforbrug på en timepakke kan koste det mangedobbelte
på en enkelt regning. Du køber ikke minutter for de 20 kr. — du køber, at du aldrig skal
tænke over det igen.</p>

<h2>Sådan finder du ud af, hvor meget du taler</h2>

<p>Du behøver ikke gætte. Tallet findes allerede på din telefon.</p>

<ol class="trin">
<li><strong>På iPhone</strong>
Åbn Telefon-appen og gå til Seneste. Under Indstillinger → Telefon findes desuden
opkaldsstatistik hos nogle operatører. Den mest præcise kilde er dog din udbyders app.</li>
<li><strong>På Android</strong>
Åbn Telefon-appen, gå til opkaldshistorik og se opkaldsvarigheder. Nogle producenter
viser en samlet månedsstatistik direkte.</li>
<li><strong>I din udbyders app</strong>
Her står det faktiske forbrug pr. afregningsperiode. Det er det tal, du skal bruge, fordi
det matcher, hvordan du faktisk faktureres.</li>
</ol>

<p>Kig på tre måneder og tag den højeste. Ligger du under to timer om måneden, kan du
roligt vælge en timepakke og spare pengene.</p>

<h2>Fri tale i EU — hvad gælder der?</h2>

<p>Inden for EU gælder roamingreglerne, der som udgangspunkt betyder, at du kan bruge dit
danske abonnement på samme vilkår, som hvis du var hjemme. Det gælder også fri tale: du
kan ringe til danske numre fra Spanien uden ekstra betaling.</p>

<p>Der er to forbehold. For det første har de fleste abonnementer et loft på, hvor meget
<em>data</em> du kan bruge i EU, selvom tale er fri. For det andet gælder reglerne
midlertidigt ophold — bor du permanent i et andet EU-land og bruger et dansk abonnement
hele året, kan udbyderen efter en periode opkræve tillæg. Det rammer stort set kun
udlandsdanskere, men det er værd at vide.</p>

<div class="advarsel">
<p><strong>Uden for EU er der ingen beskyttelse.</strong> Storbritannien, Schweiz, Tyrkiet,
USA og resten af verden falder uden for roamingreglerne. Her gælder udbyderens egne
takster, og de kan være meget høje. Slå dataroaming fra, tjek minuttaksten for landet, og
overvej et lokalt eSIM til data, mens du beholder dit danske nummer til opkald.</p>
</div>

<h2>Hvem har brug for fri tale — og hvem har ikke?</h2>

<div class="kortgitter kg-2" style="margin:1.8rem 0">
  <div class="kort">
    <h3>Fri tale giver mening for dig der…</h3>
    <p>Ringer dagligt i forbindelse med arbejde, har familie du taler længe med, bruger
    telefonen frem for beskeder, eller bare ikke gider holde øje med en tæller. Også hvis
    du er den i familien, alle ringer til.</p>
  </div>
  <div class="kort">
    <h3>Du kan spare pengene hvis du…</h3>
    <p>Primært skriver, bruger arbejdstelefon til arbejdsopkald, eller taler under to
    timer om måneden. Så er en timepakke billigere, og forskellen er reel over et år.</p>
  </div>
</div>

<h2>De typiske fælder ved billige abonnementer med fri tale</h2>

<h3>Kampagneprisen der udløber</h3>
<p>Det er markedets mest udbredte konstruktion: en lav pris i tre eller seks måneder,
hvorefter den stiger markant. Et abonnement til 39 kr., der bliver til 99 kr. i måned
syv, koster i gennemsnit 69 kr. over et år. Det er ikke nødvendigvis en dårlig aftale,
men det er en anden aftale end den, der står i annoncen. Regn altid tolv måneder ud.</p>

<h3>Fri tale uden fri sms</h3>
<p>Sjældent, men det findes. Tjek at både tale og sms er inkluderet, særligt på de
allerbilligste abonnementer og på timepakker.</p>

<h3>Særnumre og tjenester</h3>
<p>Parkeringsapps, sms-donationer og servicenumre faktureres separat, uanset fri tale.
Har du en måned med en uventet post på regningen, er det næsten altid her, den kommer fra.</p>

<h3>Data der ikke passer</h3>
<p>Fri tale er nemt. Data er det, folk vælger forkert. Vælg efter dit faktiske forbrug de
seneste tre måneder — se vores guide til <a href="/guides/hvor-meget-data/">hvor meget
data du har brug for</a>.</p>

<h2>Sådan skifter du til et abonnement med fri tale</h2>

<p>Du bestiller hos den nye udbyder, oplyser dit nuværende nummer og krydser af, at du vil
beholde det. Du skal ikke opsige noget selv. Nummeret flyttes typisk inden for 1–5
hverdage, og afbrydelsen varer sjældent mere end nogle minutter.</p>

<p>Det eneste, du skal undersøge før bestilling, er om du har binding eller restgæld på en
telefon købt på afbetaling. Restgælden følger ikke med til det nye selskab og skal typisk
indfries. Se hele fremgangsmåden i vores guide til
<a href="/guides/skift-mobilselskab/">at skifte mobilselskab</a>.</p>

</section>
"""


def bedste(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Der findes ikke ét bedste mobilabonnement — der findes et
bedste abonnement til din situation. Bor du i en by og bruger under 30 GB, er det
billigste abonnement, der dækker dit forbrug, også det bedste. Bor du på landet eller
pendler langt, er netværket vigtigere end prisen, og så er et abonnement på TDC NET
oftest det bedste valg, selvom det koster mere.</p>
</div>

<h2>Hvorfor "bedste" er et sværere spørgsmål end "billigste"</h2>

<p>Billigst kan afgøres med en sortering. Bedst kan ikke, fordi det afhænger af, hvad du
vægter. En pendler i Vestjylland og en studerende på Nørrebro kan begge have ret i, at de
har markedets bedste abonnement — og det er to helt forskellige produkter.</p>

<p>Det, vi kan gøre, er at gøre kriterierne eksplicitte, så du selv kan se, hvor du lander.
Vi vurderer abonnementer på fem parametre og siger klart, hvor meget hvert af dem vejer.</p>

<table>
<thead><tr><th>Parameter</th><th>Vægt</th><th>Hvad vi ser på</th></tr></thead>
<tbody>
<tr><td><strong>Pris pr. GB</strong></td><td>Høj</td><td>Månedspris divideret med data. Gør abonnementer af forskellig størrelse sammenlignelige.</td></tr>
<tr><td><strong>Vilkår</strong></td><td>Høj</td><td>Binding, oprettelse, opsigelsesvarsel og om prisen stiger efter en kampagneperiode.</td></tr>
<tr><td><strong>Netværk</strong></td><td>Middel-høj</td><td>Hvilket af de tre danske net udbyderen kører på, og eventuelle hastighedsvilkår.</td></tr>
<tr><td><strong>EU-data</strong></td><td>Middel</td><td>Hvor meget af datamængden du kan bruge på rejse i EU.</td></tr>
<tr><td><strong>Gennemsigtighed</strong></td><td>Middel</td><td>Hvor let det er at finde de faktiske vilkår uden at grave.</td></tr>
</tbody>
</table>

<p>Bemærk hvad der <em>ikke</em> er på listen. Vi vægter ikke streamingtjenester som en
generel fordel, fordi de kun er penge værd, hvis de erstatter noget, du allerede betaler
for. Og vi laver ikke egne hastighedsmålinger, fordi netværksejerne og de uafhængige
måleinstitutter har adgang til datamængder, vi ikke kan matche.</p>

<h2>Bedste abonnement efter hvem du er</h2>

<p>Den mest brugbare måde at svare på spørgsmålet er at dele brugerne op. Find den
beskrivelse, der ligner dig mest.</p>

<div class="kortgitter kg-3" style="margin:1.8rem 0">
  <div class="kort"><h3>Bybo med almindeligt forbrug</h3>
  <p>Alle tre net fungerer fint der, hvor du er. Vælg det billigste abonnement med
  20–50 GB. Du får intet ud af at betale for premiumdækning.</p></div>
  <div class="kort"><h3>Bor på landet eller ved kysten</h3>
  <p>Her betaler netværket sig. Vælg det billigste abonnement, der kører på TDC NET,
  frem for det billigste i alt. Forskellen mærkes i hverdagen.</p></div>
  <div class="kort"><h3>Pendler</h3>
  <p>Dækning i tog og bil svinger. TDC NET står historisk stærkest langs jernbanen.
  Vælg mindst 50 GB, da du bruger data uden wi-fi hver dag.</p></div>
  <div class="kort"><h3>Storforbruger uden fastnet</h3>
  <p>Bruger du mobilen som hjemmets internet via hotspot, er fri data det rigtige. Tjek
  at hotspot er tilladt i vilkårene, og se på EU-loftet.</p></div>
  <div class="kort"><h3>Let bruger og senior</h3>
  <p>5–10 GB rækker langt. Til gengæld er telefonisk kundeservice ofte mere værd end de
  40 kr., der kan spares hos en rent digital udbyder.</p></div>
  <div class="kort"><h3>Familie med børn</h3>
  <p>Fire separate discountabonnementer er ofte billigere end en familiepakke. Regn
  efter. Datastop på børnenes numre betyder mere end prisen.</p></div>
</div>

<h2>Er dyrere abonnementer bedre?</h2>

<p>Ikke på selve mobilforbindelsen. Det er den vigtigste enkeltindsigt på hele markedet:
der findes kun tre mobilnetværk i Danmark, og alle selskaber lejer sig ind hos en af dem.
Et abonnement til 49 kr. og et til 299 kr. kan køre på præcis de samme master med præcis
den samme hastighed.</p>

<p>Det, du betaler ekstra for i den dyre ende, er fire ting: adgang til det mest udbyggede
net, bemandet kundeservice og fysiske butikker, tillægsydelser som streaming eller
forsikring, og i nogle tilfælde en prioritering af din trafik, når nettet er belastet.</p>

<p>Om det er pengene værd afhænger fuldstændig af, om du bruger det. Bor du et sted, hvor
alle tre net leverer fuld dækning, og har du aldrig ringet til kundeservice, betaler du et
tillæg for noget, du ikke får glæde af. Bor du derimod et sted med svingende dækning,
eller er du utryg ved selv at sætte et eSIM op, kan de ekstra 100 kr. om måneden være
blandt de bedst brugte penge i dit budget.</p>

<div class="tip">
<h3>Test det, mens du kan fortryde</h3>
<p>Køber du abonnementet online, har du som udgangspunkt fortrydelsesret efter
forbrugeraftaleloven. Brug den aktivt: test dækningen hjemme, på arbejdet, i kælderen og
på din pendlerrute i de første dage. Det er den eneste rigtige måde at finde ud af, om et
billigere net kan bruges der, hvor du faktisk er.</p>
</div>

<h2>Hvad med tests og anmeldelser?</h2>

<p>Der findes uafhængige tests af de danske mobilnet, og de er værd at kende. Teknologisk
Institut har gennem en årrække målt netkvalitet, og TDC NET har konsekvent klaret sig
bedst i den type måling. Forbrugerrådet Tænk har lavet omfattende sammenligninger af
abonnementer, om end de ikke opdateres løbende.</p>

<p>Brugeranmeldelser på for eksempel Trustpilot kan sige noget om kundeservice, men skal
læses med forbehold. Folk skriver anmeldelser, når noget går galt eller går overraskende
godt, og sjældent når alt bare virker. En udbyder med få anmeldelser og høj score er ikke
nødvendigvis bedre end en med mange anmeldelser og lidt lavere score.</p>

<p>Vi bruger ikke anmeldelsesscorer som rangeringskriterium i vores tabeller, fordi de
ikke er sammenlignelige på tværs af selskaber med meget forskellige kundeantal. Vi bruger
dem som baggrundsviden, når vi skriver om det enkelte selskab.</p>

<h2>Sådan finder du dit bedste abonnement på ti minutter</h2>

<ol class="trin">
<li><strong>Find dit dataforbrug</strong>
Telefonens indstillinger, seneste tre måneder, tag det højeste og læg 20 procent til.</li>
<li><strong>Afgør om netværket betyder noget for dig</strong>
Tjek dækningskortet på din bopæl, arbejdsplads og pendlerrute. Er alle tre net grønne,
kan du vælge frit efter pris.</li>
<li><strong>Sortér efter pris pr. GB inden for din datakategori</strong>
Ikke efter månedspris. Det er her, de fleste vælger forkert.</li>
<li><strong>Tjek vilkårene på de to-tre bedste</strong>
Er prisen en kampagnepris? Er der binding? Hvor meget EU-data følger med?</li>
<li><strong>Bestil, og test i fortrydelsesperioden</strong>
Slå datastop til med det samme, og test dækningen de steder, du faktisk er.</li>
</ol>

</section>
"""


def uden_data(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Mobilabonnement uden data findes stadig i Danmark, men
udvalget er lille. Priserne starter omkring {kr(D['pris_udendata'])} kr. om måneden for et
abonnement med taletid og sms. Alternativt findes forbrugsafregnede abonnementer, hvor du
betaler 0 kr. i fast pris og kun for de minutter og sms'er, du faktisk bruger. For mange
er et lille dataabonnement dog reelt billigere end et rent taleabonnement.</p>
</div>

<h2>Hvad er et mobilabonnement uden data?</h2>

<p>Det er et abonnement, hvor du kan ringe og sende sms, men hvor der ikke er inkluderet
mobildata. Telefonen kan stadig gå på internettet — men kun via wi-fi. Alt andet fungerer
som normalt: du kan ringe, blive ringet op, sende og modtage beskeder.</p>

<p>Kategorien er blevet mindre gennem årene, fordi data er blevet så billigt, at de fleste
udbydere har droppet de rene taleprodukter. Det efterlader tre reelle muligheder på det
danske marked i dag:</p>

<table>
<thead><tr><th>Type</th><th>Sådan virker det</th><th>Bedst til</th></tr></thead>
<tbody>
<tr><td><strong>Fast abonnement uden data</strong></td><td>Fast månedspris for taletid og sms, 0 GB data</td><td>Dig der vil have en forudsigelig regning</td></tr>
<tr><td><strong>Forbrugsafregnet</strong></td><td>0 kr. i fast pris, du betaler pr. minut og pr. sms</td><td>Meget lavt og uregelmæssigt forbrug</td></tr>
<tr><td><strong>Taletidskort</strong></td><td>Du fylder penge på forud og kan ikke overskride</td><td>Børn, ekstra telefon, fuld udgiftskontrol</td></tr>
</tbody>
</table>

<h2>Den ubehagelige sandhed: det er sjældent billigst</h2>

<p>Her adskiller vi os fra en del andre sider, og vi mener, det er vigtigt at sige rent
ud. Et abonnement uden data er ofte <em>ikke</em> den billigste løsning, selvom det
intuitivt burde være det.</p>

<p>Årsagen er, at konkurrencen i Danmark foregår på dataabonnementer. Der er dusinvis af
selskaber, der slås om kunder med 5–20 GB, og priserne er presset helt i bund. De rene
taleprodukter er derimod en lille niche uden reelt priskrig, og derfor følger prisen ikke
med ned.</p>

<p>I praksis betyder det, at du ofte kan få et abonnement med fri tale <em>og</em> 5 GB
data til nogenlunde samme pris som et rent taleabonnement — og nogle gange billigere. Og
har du først dataen, kan du bare lade være med at bruge den, eller slå mobildata fra i
telefonens indstillinger.</p>

<div class="tip">
<h3>Det praktiske råd</h3>
<p>Vil du undgå mobildata helt, er den enkleste løsning at købe et billigt abonnement med
en lille datapakke og slå mobildata fra på telefonen. På iPhone: Indstillinger →
Mobildata → slå fra. På Android: Indstillinger → Netværk og internet → Mobilnetværk →
slå mobildata fra. Så har du et abonnement uden data i praksis, til en pris der er sat af
et marked med rigtig konkurrence.</p>
</div>

<h2>Hvornår giver det alligevel mening?</h2>

<p>Der er fire situationer, hvor et rent taleabonnement eller et forbrugsafregnet
abonnement er det rigtige valg, og hvor vi anbefaler det uden forbehold.</p>

<ul>
<li><strong>Telefon nummer to.</strong> En arbejdstelefon, en sommerhustelefon eller en
telefon i bilen, der kun skal kunne ringe. Her er et forbrugsafregnet abonnement til 0 kr.
i fast pris ofte den billigste løsning overhovedet, fordi du kun betaler i de måneder,
telefonen faktisk bruges.</li>
<li><strong>Barnets første telefon.</strong> Ingen data betyder ingen sociale medier og
ingen YouTube uden for hjemmets wi-fi. For mange forældre er det ikke en begrænsning — det
er hele pointen. Se vores side om
<a href="/mobilabonnement-til-boern/">mobilabonnement til børn</a>.</li>
<li><strong>Bevidst mindre skærmtid.</strong> Nogle vælger det aktivt for at bryde vanen
med at tjekke telefonen konstant. Uden mobildata bliver telefonen igen et
kommunikationsværktøj frem for en underholdningsmaskine.</li>
<li><strong>Ældre pårørende der kun ringer.</strong> Hvis telefonen udelukkende bruges til
opkald, er der ingen grund til at betale for data. Her vejer enkel og bemandet
kundeservice dog tungere end de sidste tyve kroner.</li>
</ul>

<h2>Forbrugsafregnet: sådan regner du på det</h2>

<p>Forbrugsafregnede abonnementer har typisk 0 kr. i fast månedspris og en takst pr.
minut og pr. sms. Det lyder ubetinget godt, men det kan blive dyrt, hvis forbruget
alligevel er der.</p>

<p>Regnestykket er enkelt. Med en takst omkring en halv krone pr. minut koster hundrede
minutters tale cirka 50 kr. Det er stadig billigt. Men bruger du 300 minutter, altså ti
minutter om dagen, lander du omkring 150 kr. — og der er du langt over, hvad et almindeligt
abonnement med fri tale og data ville have kostet.</p>

<table>
<thead><tr><th>Dit taleforbrug</th><th>Forbrugsafregnet koster ca.</th><th>Bedre valg?</th></tr></thead>
<tbody>
<tr><td>Under 30 min./md.</td><td>Under 20 kr.</td><td>Nej, forbrugsafregnet er klart billigst</td></tr>
<tr><td>30–100 min./md.</td><td>20–50 kr.</td><td>Tæt løb — begge dele fungerer</td></tr>
<tr><td>100–200 min./md.</td><td>50–100 kr.</td><td>Ja, vælg fast abonnement med fri tale</td></tr>
<tr><td>Over 200 min./md.</td><td>Over 100 kr.</td><td>Ja, klart. Fri tale er billigere</td></tr>
</tbody>
</table>

<p>Bemærk at taksterne varierer mellem udbydere, og at nogle har opkaldsafgift oveni
minutprisen. Tjek altid de aktuelle takster hos udbyderen, før du vælger.</p>

<h2>Sådan sikrer du, at der ikke bliver brugt data</h2>

<p>Har du et abonnement uden data, kan telefonen stadig forsøge at bruge mobildata, og hos
nogle udbydere udløser det en takst pr. megabyte. Det er den klassiske fælde. Sådan lukker
du den:</p>

<ol class="trin">
<li><strong>Slå mobildata fra i telefonen</strong>
Det er første og vigtigste skridt. Wi-fi virker stadig.</li>
<li><strong>Slå dataroaming fra</strong>
Særligt vigtigt hvis du rejser. Ligger under mobilindstillinger.</li>
<li><strong>Bed udbyderen om datastop eller dataspærring</strong>
De fleste kan spærre helt for data på abonnementet. Det er det sikreste, fordi det
virker uanset hvad der sker i telefonens indstillinger.</li>
<li><strong>Tjek første regning</strong>
Kig efter poster med data eller mb. Er der noget, så ring med det samme — det er nemmere
at få rettet den første måned.</li>
</ol>

<h2>Uden data mod taletidskort</h2>

<p>De to ting minder om hinanden, men fungerer forskelligt. Et abonnement har en fast
månedspris og faktureres bagud. Et taletidskort er forudbetalt: du fylder penge på, og når
de er brugt, stopper det.</p>

<p>Taletidskortets store fordel er, at det er umuligt at få en overraskelsesregning. Det
gør det til et stærkt valg til børn og til alle, der vil have absolut udgiftskontrol.
Ulempen er, at du selv skal huske at fylde op, og at prisen pr. minut typisk er højere end
på et abonnement.</p>

<p>Et abonnement uden data er omvendt nemmere i hverdagen — der er ingenting, du skal
huske — men du kan i princippet bruge mere, end du havde tænkt dig, hvis der ikke er
spærret for data.</p>

</section>
"""
