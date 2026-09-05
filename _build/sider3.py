# -*- coding: utf-8 -*-
"""Indhold til kategorisiderne musik, ældre, telefon på afbetaling og taletidskort."""

from skabelon import kr


def musik(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Mobilabonnement med musik koster fra
{kr(D['pris_musik'])} kr. om måneden. Musiktjenester er langt billigere at få med end
video, fordi de fylder næsten ingenting i datamængden — og fordi de koster mindre at købe
separat. Regnestykket er stadig det samme: betaler du allerede for tjenesten, sparer du
penge. Gør du ikke, betaler du for noget, du ikke bruger.</p>
</div>

<h2>Musik er den billigste streaming at få med</h2>

<p>Der er en reel forskel på musik og video i et mobilabonnement, og den bliver sjældent
nævnt. Video koster 0,7–3 GB i timen. Musik koster 70–150 MB i timen — altså op mod tyve
gange mindre.</p>

<p>Det betyder to ting. For det første kan du nøjes med et lille abonnement og stadig bruge
musiktjenesten hele dagen. Et abonnement med 10 GB rækker til omkring hundrede timers
musik, hvilket for de fleste svarer til flere måneders lytning på farten. For det andet er
musiktjenester billigere for udbyderen at pakke ind, og derfor er merprisen typisk lavere
end ved en videopakke.</p>

<div class="tip">
<h3>Download i stedet for at streame</h3>
<p>Alle større musiktjenester kan gemme musik offline. Sætter du automatisk download til
over wi-fi om natten, bruger du reelt nul mobildata på musik. Det er den enkleste måde at
komme ned i abonnementskategori, og det virker uanset hvilken tjeneste du har.</p>
</div>

<h2>Sådan regner du på det</h2>

<ol class="trin">
<li><strong>Find hvad du betaler i dag</strong>
Musiktjenester ligger typisk i den lave ende sammenlignet med video. Kig i din netbank
eller i abonnementsoversigten på telefonen.</li>
<li><strong>Find prisen på et tilsvarende abonnement uden musik</strong>
Samme datamængde, samme netværk. Det er dit sammenligningsgrundlag.</li>
<li><strong>Træk de to fra hinanden</strong>
Er merprisen lavere end tjenestens egen pris, sparer du. Er den højere, betaler du for at
have det samlet ét sted.</li>
<li><strong>Husk familieabonnementer</strong>
Deler du en familieplan med andre, er din reelle udgift kun en andel af prisen — og så
skal du sammenligne mod den andel, ikke mod den fulde pris.</li>
</ol>

<h2>Operatørernes egne musiktjenester</h2>

<p>Flere danske udbydere har deres egen musiktjeneste, som følger med abonnementet. De er
sværere at værdisætte, fordi de ikke kan købes separat på samme måde som de store
internationale tjenester.</p>

<p>Vores holdning er, at du skal vurdere dem efter, om du reelt vil bruge dem — ikke efter
hvad de siges at være værd. Har du et musikbibliotek, playlister og lyttehistorik hos en
anden tjeneste, er værdien af at skifte tæt på nul, uanset prisskiltet. Starter du fra
bunden, kan det være et fint tilbud.</p>

<h2>Podcast og lydbøger tæller også</h2>

<p>Lydkategorien er bredere end musik. Podcast- og lydbogstjenester indgår i flere
abonnementer, og for pendlere er de ofte den mest brugte del af pakken.</p>

<p>Lydbøger er værd at fremhæve, fordi de er dyre at købe separat sammenlignet med musik.
Lytter du til lydbøger regelmæssigt, er det den enkelttjeneste, hvor et bundle oftest kan
betale sig. Se hvilke abonnementer der inkluderer hvad på vores
<a href="/mobilabonnement-med-streaming/tjenester/">oversigt over streamingtjenester</a>.</p>

<h2>Musiktjenesterne stillet op mod hinanden</h2>
<p>Får du en musiktjeneste med i abonnementet, er det sjældent dit eget valg,
hvilken. Her er forskellen på dem, så du kan vurdere, om den, der følger med,
er den, du ville have valgt.</p>

[[tabel_musiktjenester]]

<h3>Offline er det vigtigste felt i tabellen</h3>
<p>Alle tjenesterne kan hente indhold ned over wi-fi. Gør du det, bruger du nul
data på farten, og så er dataforbruget helt uden betydning for valget af
abonnement. Det er den enkleste måde at gøre et lille abonnement rigeligt.</p>

<h2>Hvor meget data bruger musik egentlig?</h2>
[[tabel_lyd_dataforbrug]]

<h3>Derfor er lyd den billigste streaming at få med</h3>
<p>En time musik i normal kvalitet bruger 0,07 GB. En time video i HD bruger 3 GB
— altså fyrre gange så meget. Selv daglig lytning i høj kvalitet holder sig under
5 GB om måneden.</p>
<p>Det betyder, at et abonnement med musik ikke kræver mere data. Hører du
musik en time om dagen og ellers bruger telefonen normalt, rækker
<a href="/mobilabonnement-10-30-gb/">10-30 GB</a> fint.</p>
<p>Undtagelsen er lossless. Streamer du i tabsfri kvalitet uden at hente ned,
bruger du 15 GB om måneden alene på musik. Det er værd at vide, hvis du har
gode høretelefoner og et lille abonnement.</p>

<table>
<thead><tr><th>Kvalitet</th><th>Ca. forbrug pr. time</th><th>10 GB rækker til</th></tr></thead>
<tbody>
<tr><td>Normal</td><td>ca. 70 MB</td><td>ca. 140 timer</td></tr>
<tr><td>Høj</td><td>ca. 100 MB</td><td>ca. 100 timer</td></tr>
<tr><td>Meget høj</td><td>ca. 150 MB</td><td>ca. 65 timer</td></tr>
<tr><td>Tabsfri</td><td>ca. 350 MB og opefter</td><td>ca. 28 timer</td></tr>
<tr><td>Podcast</td><td>ca. 30–60 MB</td><td>ca. 170–330 timer</td></tr>
</tbody>
</table>

<p>Bemærk den nederste række. Podcasts fylder så lidt, at de i praksis er gratis i
datamæssig forstand. Er det podcasts og ikke musik, du lytter til, er der ingen grund til
at gå op i datamængde overhovedet.</p>

<div class="advarsel">
<p><strong>Tabsfri lyd er undtagelsen.</strong> Vælger du den højeste kvalitet, femdobles
dataforbruget. Har du et lille abonnement og lytter i tabsfri kvalitet på farten, løber du
tør. Sæt tjenesten til normal kvalitet på mobildata og høj på wi-fi — forskellen er svær
at høre gennem almindelige høretelefoner i et tog.</p>
</div>
</section>
"""


def aeldre(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Til en ældre bruger betyder to ting mere end prisen:
telefonisk kundeservice og en regning uden overraskelser. Priserne starter ved
{kr(D['pris_aeldre'])} kr. om måneden, men vi anbefaler sjældent det allerbilligste
abonnement her — de billigste udbydere har kun digital support, og det er præcis dét, der
skaber problemer, når noget driller.</p>
</div>

<h2>Derfor er billigst ikke bedst her</h2>

<p>På resten af dette site anbefaler vi konsekvent at gå efter laveste pris, når dækningen
er i orden. Den anbefaling holder ikke for alle brugere, og her er hvorfor.</p>

<p>Discountudbydere er billige, fordi de har skåret kundeservice, butikker og telefonisk
support væk. For en digitalt tryg bruger er det en ren besparelse. For en bruger, der har
brug for hjælp til at sætte et simkort i, forstå en regning eller genskabe forbindelsen
efter en telefonopdatering, er det ikke en besparelse — det er en risiko.</p>

<p>Forskellen mellem et discountabonnement og et med bemandet kundeservice er typisk
40–80 kr. om måneden. Det er 500–1.000 kr. om året. Vurder det mod, hvad det er værd at
kunne ringe til nogen og få hjælp samme dag — eller at kunne gå ind i en butik med
telefonen i hånden.</p>

<div class="tip">
<h3>Det praktiske spørgsmål</h3>
<p>Hvem hjælper, hvis telefonen holder op med at virke en tirsdag formiddag? Er svaret
"mit barnebarn, når han har tid", så vælg en udbyder med telefonisk support. Er svaret
"det klarer jeg selv", så gå efter prisen som alle andre.</p>
</div>

<h2>Hvor meget data er nok?</h2>

<p>Meget mindre end de fleste tror. En bruger, der ringer, sender beskeder, tjekker vejret
og af og til bruger kort, kommer sjældent over 3–5 GB om måneden. Er der wi-fi i hjemmet —
og det er der næsten altid — sker det meste forbrug slet ikke på mobilnettet.</p>

<table>
<thead><tr><th>Typisk brug</th><th>Anbefalet datamængde</th><th>Bemærkning</th></tr></thead>
<tbody>
<tr><td>Kun opkald og sms</td><td>0–2 GB</td><td>Overvej et abonnement uden data</td></tr>
<tr><td>Plus vejr, kort og nyheder</td><td>5 GB</td><td>Dækker langt de fleste</td></tr>
<tr><td>Plus videoopkald med familien</td><td>10 GB</td><td>Videoopkald fylder mest</td></tr>
<tr><td>Plus streaming af tv og radio</td><td>20–30 GB</td><td>Kun hvis det sker uden for wi-fi</td></tr>
</tbody>
</table>

<p>Vær opmærksom på videoopkald. Det er den ene ting, der for alvor bruger data i denne
gruppe, og den bliver mere almindelig. En times videoopkald koster op mod 1,5 GB. Ringer I
sammen en time om ugen, er 10 GB en fornuftig bund.</p>

<h2>Undgå de tre almindelige regningsproblemer</h2>

<ol class="trin">
<li><strong>Spærring for overtakserede numre</strong>
Servicenumre, sms-tjenester og konkurrencenumre kan koste meget. Bed udbyderen spærre for
dem — det er gratis og kan gøres over telefonen.</li>
<li><strong>Datastop</strong>
Forhindrer at der købes ekstra data automatisk, hvis pakken løber tør. Det er den
indstilling, der oftest forhindrer en chokregning.</li>
<li><strong>Spærring for udlandsopkald</strong>
Beskytter mod svindelopkald, hvor man lokkes til at ringe tilbage til et dyrt
udlandsnummer. Ringer man aldrig til udlandet, er der ingen ulempe ved at slå det fra.
Læs mere om <a href="/hvem-ringer-til-mig/">svindelopkald og hvordan du genkender dem</a>.</li>
</ol>

<h2>Telefonen betyder mere end abonnementet</h2>

<p>Et abonnement er bare et simkort. Oplevelsen afhænger langt mere af telefonen, og det er
værd at bruge sin opmærksomhed der.</p>

<p>Der findes telefoner bygget specifikt til ældre brugere med store taster, høj lyd,
kraftig vibration, høreapparatkompatibilitet og en nødopkaldsknap på bagsiden. De er ofte
billigere end en almindelig smartphone og markant lettere at bruge.</p>

<p>Køb telefonen for sig og abonnementet for sig. Køber du dem samlet på afbetaling, binder
du dig typisk i 24 eller 36 måneder, og så kan du ikke skifte, hvis behovet ændrer sig.
Se <a href="/mobilabonnement-med-telefon/">vores gennemgang af telefon på afbetaling</a>.</p>

<div class="advarsel">
<p><strong>Nødopkald virker altid.</strong> 112 kan ringes uanset abonnement, uanset om
taletiden er brugt op, og uanset om der er dækning fra netop dit selskab — telefonen bruger
det net, der er stærkest. Det gælder også uden simkort i telefonen.</p>
</div>

<h2>Hjælp til at skifte</h2>

<p>Selve skiftet er nemt, men kræver at nogen sidder med. Den nye udbyder klarer
nummerflytningen, og det gamle abonnement lukkes automatisk. Det eneste praktiske er at
skifte simkortet på den aftalte dag — eller aktivere et eSIM, hvis telefonen er ny nok.</p>

<p>Sæt en halv time af, gør det sammen, og gem den nye udbyders telefonnummer i telefonen
med det samme. Se hele fremgangsmåden i vores guide til
<a href="/guides/skift-mobilselskab/">at skifte mobilselskab</a>.</p>
</section>
"""


def telefon(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Køb telefonen og abonnementet hver for sig. Et samlet tilbud
ser billigere ud, men binder dig i typisk 24–36 måneder til ét selskab, og restgælden skal
indfries, hvis du vil skifte. Regner du hele perioden igennem, er kontantkøb plus et
discountabonnement næsten altid billigere. Abonnementer uden binding starter ved
{kr(D['min_pris'])} kr. om måneden.</p>
</div>

<h2>Regnestykket der afgør det</h2>

<p>Et telefontilbud med abonnement består af to ting: en månedlig ydelse på telefonen og et
abonnement. Problemet er, at de præsenteres som ét tal, og at abonnementsdelen næsten altid
er dyrere end markedets alternativ.</p>

<p>Sådan regner du det ud på fem minutter:</p>

<ol class="trin">
<li><strong>Gang den samlede månedspris med antal måneder i bindingen</strong>
Er det 399 kr. i 24 måneder, er det 9.576 kr.</li>
<li><strong>Læg udbetaling og oprettelse til</strong>
Nogle tilbud har en engangsbetaling, som ikke fremgår af månedsprisen.</li>
<li><strong>Find telefonens kontantpris</strong>
Søg på modellen. Brug den laveste reelle pris hos en forhandler, du ville handle hos.</li>
<li><strong>Læg prisen på et discountabonnement til, ganget med samme antal måneder</strong>
Et abonnement til 89 kr. i 24 måneder er 2.136 kr.</li>
<li><strong>Sammenlign de to totaler</strong>
Forskellen er den reelle pris for bekvemmeligheden ved at samle det.</li>
</ol>

<div class="tip">
<h3>Et typisk eksempel</h3>
<p>Telefon plus abonnement til 399 kr. i 24 måneder giver 9.576 kr. Samme telefon kontant
til 5.500 kr. plus et abonnement til 89 kr. i 24 måneder giver 7.636 kr. Forskellen er
knap 2.000 kr. — og i den frie løsning kan du desuden skifte abonnement undervejs, hvis
priserne falder.</p>
</div>

<h2>Hvad binding reelt koster dig</h2>

<p>Ud over renten på afbetalingen er der en skjult omkostning, som ikke står nogen steder:
du mister muligheden for at reagere på markedet.</p>

<p>Mobilpriser falder år for år, og de bedste tilbud går til nye kunder. Er du bundet i to
år, kan du ikke tage imod dem. Vores erfaring med markedet er, at prisen på et tilsvarende
abonnement typisk falder mærkbart i løbet af en toårig periode — og den besparelse går din
næse forbi.</p>

<p>Dertil kommer det praktiske: går telefonen i stykker, bliver stjålet eller skal skiftes,
løber afbetalingen videre. Restgælden forsvinder ikke, fordi telefonen gør.</p>

<h2>Hvornår kan det så betale sig?</h2>

<p>Der er to situationer, hvor et samlet køb giver mening, og de er værd at nævne, fordi vi
ikke mener, svaret altid er nej.</p>

<ul>
<li><strong>Du kan ikke lægge pengene ud.</strong> Skal du bruge en telefon nu og har ikke
5.000 kr., er afbetaling en reel finansieringsform. Sammenlign den effektive rente med et
almindeligt forbrugslån, før du beslutter dig — nogle gange er den faktisk lavere.</li>
<li><strong>Der er en ægte hardwarerabat.</strong> Sker det, at telefonen sælges markant
under kontantpris som del af pakken, kan totalen falde ud til pakkens fordel. Det er
sjældent, men det findes. Regnestykket ovenfor afslører det på fem minutter.</li>
</ul>

<h2>Brugt telefon er det oversete alternativ</h2>

<p>Den billigste vej til en god telefon er en brugt eller renoveret model, der er et par år
gammel. Forskellen i hverdagsbrug mellem en toppmodel fra i år og en fra for tre år siden
er lille for de fleste — kameraet er lidt bedre, og batteriet er nyere.</p>

<p>Køber du brugt, sparer du typisk halvdelen, du undgår binding helt, og du kan lægge
forskellen i et bedre abonnement eller bare beholde den. Tjek at telefonen ikke er
simlåst, at den understøtter <a href="/guides/esim/">eSIM</a>, hvis du vil have det, og at
batteriets tilstand er oplyst.</p>

<div class="advarsel">
<p><strong>Tjek restgælden, før du skifter.</strong> Har du allerede telefon på afbetaling
gennem dit nuværende selskab, skal restgælden typisk indfries på én gang, når du skifter.
Ring og få beløbet oplyst, før du bestiller noget nyt — det er den hyppigste ubehagelige
overraskelse ved selskabsskifte.</p>
</div>

<h2>Forsikring: læs det med småt</h2>

<p>Mobilforsikring sælges ofte med i pakken. Den kan være pengene værd, men tjek tre ting:
selvrisikoen ved skade, om tyveri er dækket, og om du allerede er dækket gennem din
indboforsikring. Mange er dækket i forvejen uden at vide det, og så betaler man dobbelt.</p>
</section>
"""


def taletid(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et taletidskort er forudbetalt — du fylder penge på, og når
de er brugt, stopper det. Det gør en overraskelsesregning umulig, og det er derfor
taletid er det tryggeste valg til børn og til en telefon, der bruges sjældent. Ulempen er,
at prisen pr. gigabyte er højere end på et abonnement, og at du selv skal huske at fylde
op.</p>
</div>

<h2>Taletid mod abonnement</h2>

<table>
<thead><tr><th></th><th>Taletidskort</th><th>Abonnement</th></tr></thead>
<tbody>
<tr><td><strong>Betaling</strong></td><td>Forud — du fylder på</td><td>Bagud — regning hver måned</td></tr>
<tr><td><strong>Kan overskrides?</strong></td><td>Nej, aldrig</td><td>Ja, ved overforbrug</td></tr>
<tr><td><strong>Pris pr. GB</strong></td><td>Højere</td><td>Lavere</td></tr>
<tr><td><strong>Kræver kreditvurdering</strong></td><td>Nej</td><td>Som regel ja</td></tr>
<tr><td><strong>Binding</strong></td><td>Aldrig</td><td>Oftest ingen, men findes</td></tr>
<tr><td><strong>Vedligehold</strong></td><td>Du skal huske at fylde op</td><td>Kører af sig selv</td></tr>
</tbody>
</table>

<p>Den afgørende linje er den anden. Alt andet er en afvejning — men umuligheden af at
overskride er en egenskab, intet abonnement kan give dig, uanset hvor mange spærringer du
slår til.</p>

<h2>Fire situationer hvor taletid er det rigtige</h2>

<ul>
<li><strong>Barnets første telefon.</strong> Ingen regning kan komme bag på jer, og barnet
lærer at forholde sig til et forbrug, der er synligt. Se vores side om
<a href="/mobilabonnement-til-boern/">mobilabonnement til børn</a>.</li>
<li><strong>Telefon nummer to.</strong> En telefon i bilen, i sommerhuset eller i skuffen
til nødstilfælde. Du betaler kun, når den bruges.</li>
<li><strong>Uden kreditvurdering.</strong> Taletid kræver normalt ingen kreditvurdering,
fordi du betaler forud. Det gør det til en mulighed for folk, der ikke kan få et
almindeligt abonnement.</li>
<li><strong>Kort ophold i Danmark.</strong> Er du her midlertidigt, giver et abonnement med
opsigelsesvarsel sjældent mening.</li>
</ul>

<h2>Sådan regner du på, om det kan betale sig</h2>

<p>Taletid afregnes typisk pr. minut og pr. sms, plus en pris for data. Regnestykket vender
hurtigere, end folk tror.</p>

<table>
<thead><tr><th>Månedligt forbrug</th><th>Taletid koster ca.</th><th>Bedre valg</th></tr></thead>
<tbody>
<tr><td>Under 30 min., næsten ingen data</td><td>Under 25 kr.</td><td>Taletid, klart</td></tr>
<tr><td>60 min. og 1 GB</td><td>50–80 kr.</td><td>Tæt løb</td></tr>
<tr><td>120 min. og 3 GB</td><td>100–150 kr.</td><td>Abonnement</td></tr>
<tr><td>Daglig brug med data</td><td>Over 150 kr.</td><td>Abonnement, uden tvivl</td></tr>
</tbody>
</table>

<p>Taksterne varierer mellem udbydere, og nogle har en opkaldsafgift oveni minutprisen.
Tjek altid de aktuelle takster, og vær særligt opmærksom på prisen pr. megabyte, hvis der
overhovedet bruges data — det er der, taletid bliver dyrt.</p>

<div class="tip">
<h3>Datapakker på taletid</h3>
<p>De fleste udbydere sælger datapakker, du kan købe oven på taletiden — for eksempel 5 GB
med en måneds gyldighed. Det giver ofte en langt bedre pris pr. gigabyte end den løbende
takst, og det bevarer trygheden ved at kunne se, hvad der er tilbage. Bruges telefonen til
data overhovedet, så køb en pakke frem for at betale løbende.</p>
</div>

<h2>Det du skal være opmærksom på</h2>

<h3>Udløb af saldo</h3>
<p>Taletid har typisk en gyldighedsperiode. Bruges kortet ikke i en længere periode, kan
saldoen eller selve nummeret bortfalde. Det rammer især reservetelefoner, der ligger i en
skuffe. Fyld et lille beløb på med jævne mellemrum for at holde nummeret aktivt, eller
tjek udbyderens regler for, hvor længe der må gå.</p>

<h3>Nummeret er dit</h3>
<p>Du kan flytte dit nummer fra taletid til abonnement og den anden vej. Nummerportering
gælder begge veje, og den nye udbyder klarer det. Du mister altså ikke nummeret ved at
starte på taletid.</p>

<h3>Automatisk optankning</h3>
<p>Flere udbydere tilbyder automatisk optankning, når saldoen er lav. Det er praktisk — men
det fjerner samtidig hele pointen med taletid, nemlig at forbruget ikke kan løbe løbsk.
Slår du det til på et barns telefon, har du reelt lavet et abonnement uden loft.</p>

<h2>Nødopkald virker altid</h2>

<p>Uanset saldo kan der ringes 112 fra et taletidskort. Det gælder også, hvis taletiden er
brugt op, og hvis der ikke er dækning fra netop det selskab — telefonen bruger det net, der
er stærkest tilgængeligt. Det er værd at vide, hvis taletid overvejes til et barn eller en
ældre pårørende.</p>
</section>
"""


BLACK_FRIDAY = """
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort svar:</strong> Black Friday er sjældent den bedste tid at købe
mobilabonnement. Markedet kører intropriser hele året, og november-tilbuddene er som regel
den samme mekanik med en anden overskrift. Det, der derimod bliver markant billigere, er
telefoner. Vores råd: køb telefonen på Black Friday og abonnementet, når du har brug for
det.</p>
</div>

<h2>Derfor er mobilabonnement en dårlig Black Friday-vare</h2>

<p>Black Friday virker på varer med en fast normalpris, som kan sættes ned. Et
mobilabonnement har ikke rigtig en fast pris — det har en intropris og en normalpris, og
introprisen kører i forvejen året rundt.</p>

<p>Det betyder, at et Black Friday-tilbud på mobilabonnement typisk er det samme som et
tilbud i marts: lav pris i to til seks måneder, derefter normalprisen. Overskriften er
anderledes, mekanikken er den samme. Sammenlign derfor altid på gennemsnitsprisen over
tolv måneder — det er kolonnen, vi viser i alle vores tabeller.</p>

<div class="tip">
<h3>Sådan tjekker du om et Black Friday-tilbud er ægte</h3>
<p>Find normalprisen, ikke tilbudsprisen. Gang tilbudsprisen med antal tilbudsmåneder, læg
normalprisen ganget med de resterende måneder til, og divider med tolv. Er det tal lavere
end markedets gennemsnit uden for november, er tilbuddet ægte. Er det ikke, er det
markedsføring.</p>
</div>

<h2>Det der faktisk bliver billigere</h2>

<ul>
<li><strong>Telefoner.</strong> Her er der ægte lagerrydning, især på sidste års
topmodeller. Det er den vare, hvor Black Friday reelt flytter prisen.</li>
<li><strong>Tilbehør.</strong> Høretelefoner, powerbanks og covers falder mærkbart.</li>
<li><strong>Oprettelsesgebyrer.</strong> Enkelte udbydere dropper oprettelse i kampagnen.
Det er reelle penge, men det er sjældent mere end et par hundrede kroner.</li>
</ul>

<h2>Sådan forbereder du dig</h2>

<ol class="trin">
<li><strong>Find dit dataforbrug nu</strong>
Så du ikke træffer beslutningen på en fredag under tidspres. Se vores
<a href="/guides/hvor-meget-data/">guide til dataforbrug</a>.</li>
<li><strong>Notér hvad du betaler i dag</strong>
Både månedspris og hvornår en eventuel intropris udløber. Uden det tal kan du ikke vurdere
noget som helst.</li>
<li><strong>Beslut om du skal bruge en ny telefon</strong>
Det er der, pengene er. Find modellen og dens normale pris, så du kan genkende et rigtigt
tilbud.</li>
<li><strong>Undgå binding i farten</strong>
Det er her, folk laver de dyre fejl. En pakke med telefon og abonnement på 36 måneders
binding er ikke et tilbud — det er et lån.</li>
</ol>

<h2>Hvad vi gør i november</h2>

<p>Vi opdaterer vores sammenligning som resten af året og markerer de tilbud, der reelt
ligger under markedsprisen målt på gennemsnittet over tolv måneder. Vi laver ikke en
separat liste med "Black Friday-tilbud", fordi det ville betyde, at vi fremhævede noget på
grund af datoen frem for prisen.</p>

<p>Se den løbende sammenligning på
<a href="/billigste-mobilabonnement/">billigste mobilabonnement</a>, og brug
<a href="/bedste-mobilabonnement/">vores kriterier</a>, hvis du er i tvivl om, hvad der er
et godt køb for netop dig.</p>
</section>
"""
