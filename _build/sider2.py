# -*- coding: utf-8 -*-
"""Langt indhold til de seks kategorisider (del 2)."""

from skabelon import kr


def streaming(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Mobilabonnement med streaming koster fra
{kr(D['pris_streaming'])} kr. om måneden. Om det kan betale sig afhænger udelukkende af én
ting: hvor mange af de inkluderede tjenester du <em>allerede</em> betaler for. Bruger du
to eller flere af dem, er det som regel en klar besparelse. Bruger du ingen af dem,
betaler du et stort tillæg for noget, du ikke får glæde af.</p>
</div>

<h2>Sådan regner du på det — før du bestiller</h2>

<p>Det her er den eneste udregning, der betyder noget, og den tager to minutter. Alt andet
på siden er baggrund.</p>

<ol class="trin">
<li><strong>Skriv ned, hvad du betaler for streaming i dag</strong>
Kig i din netbank eller i abonnementsoversigten på din telefon. Tag alle tjenester med,
også dem du har glemt.</li>
<li><strong>Streg de tjenester, der indgår i abonnementet</strong>
Kun dem du faktisk bruger. En tjeneste, du ville have opsagt alligevel, er ikke en
besparelse.</li>
<li><strong>Læg det tal sammen med prisen på et billigt mobilabonnement</strong>
Brug prisen på et discountabonnement med den datamængde, du har brug for.</li>
<li><strong>Sammenlign med streamingabonnementets samlede pris</strong>
Er det lavere, har du fundet en besparelse. Er det højere, betaler du for luft.</li>
</ol>

<div class="tip">
<h3>Et konkret eksempel</h3>
<p>Betaler du 129 kr. for to streamingtjenester og 89 kr. for et abonnement med 30 GB, er
din samlede udgift 218 kr. Koster et abonnement med de samme to tjenester og tilsvarende
data 199 kr., sparer du 19 kr. om måneden — 228 kr. om året. Bruger du kun den ene
tjeneste, vender regnestykket, og du betaler over.</p>
</div>

<h2>De tre ting folk regner forkert</h2>

<h3>De tæller tjenester, de ikke bruger</h3>
<p>Den mest almindelige fejl. En pakke med fem tjenester lyder af mere værdi end en med to,
men værdien er kun de tjenester, du reelt ser. Fire ubrugte tjenester er nul kroner værd,
uanset hvad de koster hver for sig.</p>

<h3>De glemmer, at de deler med familien</h3>
<p>Mange streamingtjenester deles i husstanden. Får du en tjeneste med i dit
mobilabonnement, som din partner allerede betaler for, sparer husstanden ingenting — I har
bare to abonnementer på samme tjeneste. Tal sammen, før I bestiller.</p>

<h3>De sammenligner mod den forkerte pris</h3>
<p>Sammenligningen skal være mod et <em>billigt</em> mobilabonnement plus separate
streamingabonnementer — ikke mod et dyrt mobilabonnement. Ellers ser streamingpakken bedre
ud, end den er.</p>

<h2>Hvad der typisk indgår</h2>

<p>Indholdet varierer mellem udbydere og ændrer sig løbende, men der er tre kategorier, du
typisk møder på det danske marked:</p>

<table>
<thead><tr><th>Kategori</th><th>Eksempler på indhold</th><th>Værd at vide</th></tr></thead>
<tbody>
<tr><td><strong>Film og serier</strong></td><td>Store internationale og danske streamingtjenester</td><td>Ofte den mest værdifulde del, hvis du ser meget</td></tr>
<tr><td><strong>Musik og lyd</strong></td><td>Musikstreaming, podcast- og lydbogstjenester</td><td>God værdi hvis du pendler eller træner meget</td></tr>
<tr><td><strong>Sport og live-tv</strong></td><td>Sportspakker og tv-kanaler</td><td>Dyrest at købe separat — størst besparelse hvis du bruger det</td></tr>
</tbody>
</table>

<div class="advarsel">
<p><strong>Vigtigt:</strong> Indholdet i streamingpakker kan ændre sig. En tjeneste kan
ryge ud, når en aftale mellem udbyderen og indholdsleverandøren udløber, og så står du med
et abonnement, du valgte af én grund, som ikke længere gælder. Sæt en påmindelse i
kalenderen én gang om året og genberegn. Tjek også vilkårene for, hvad der sker med
prisen, hvis en tjeneste fjernes.</p>
</div>

<h2>Fordele og ulemper ved at samle det</h2>

<div class="plusminus">
  <div class="pm pm-plus"><h3>Det taler for</h3><ul>
    <li>Én regning i stedet for fire-fem forskellige</li>
    <li>Reel besparelse hvis du bruger to eller flere tjenester</li>
    <li>Ingen selvstændige prisstigninger på hver enkelt tjeneste</li>
    <li>Ofte stærkt netværk, da streamingprodukter typisk sælges af de store selskaber</li>
    <li>Nemt at opsige samlet, hvis du vil ud af det hele</li>
  </ul></div>
  <div class="pm pm-minus"><h3>Det taler imod</h3><ul>
    <li>Svært at prissammenligne direkte med rene mobilabonnementer</li>
    <li>Indholdet kan ændre sig i abonnementsperioden</li>
    <li>Du binder din streaming til dit valg af mobilselskab</li>
    <li>Dyrt hvis du ikke bruger tjenesterne — ofte 100 kr. eller mere om måneden</li>
    <li>Skifter du mobilselskab, mister du streamingen samtidig</li>
  </ul></div>
</div>

<h2>Hvem passer det til?</h2>

<div class="kortgitter kg-2" style="margin:1.8rem 0">
  <div class="kort">
    <h3>Vælg streaming i abonnementet hvis…</h3>
    <p>Du allerede betaler for to eller flere af de tjenester, der indgår, du gerne vil have
    færre regninger, og du ikke deler abonnementerne med andre i forvejen. Særligt stærkt
    hvis en sportspakke indgår, da de er dyre at købe separat.</p>
  </div>
  <div class="kort">
    <h3>Vælg noget andet hvis…</h3>
    <p>Du kun ser én tjeneste, deler streaming med familien, eller bare vil have data og
    tale til laveste pris. Så får du mere for pengene med et discountabonnement og de
    streamingtjenester, du selv vælger.</p>
  </div>
</div>

<h2>Data og streaming hænger sammen</h2>

<p>Der er en detalje, som let overses: streaming bruger data, og hvis abonnementet har en
lille datapakke, kan du reelt ikke bruge de tjenester, du betaler for, når du er ude af
huset.</p>

<p>Video i standardkvalitet koster cirka 0,7–1 GB i timen, i HD nærmere 2–3 GB. Ser du en
time video om dagen uden for wi-fi, bruger du 20–90 GB om måneden alene på det. Et
streamingabonnement med 20 GB er derfor i praksis et abonnement, du kun kan bruge hjemme.</p>

<p>Vælger du streaming, så vælg samtidig rigelig data — mindst 50 GB, og gerne fri data,
hvis du ser meget på farten. Se
<a href="/mobilabonnement-med-fri-data/">vores side om fri data</a> for prisniveauet.</p>

<div class="tip">
<h3>Spar data på streaming</h3>
<p>Sæt streamingtjenester til kun at hente i høj kvalitet på wi-fi, og download serier og
podcasts hjemmefra i stedet for at streame på farten. De to indstillinger halverer typisk
dataforbruget og kan flytte dig ned i en billigere abonnementskategori — hvilket ofte
sparer mere, end streamingpakken gør.</p>
</div>

<h2>Sådan opsiger du, hvis regnestykket ændrer sig</h2>

<p>De fleste danske abonnementer med streaming er uden binding, så du kan opsige med
løbende måned plus varsel. Husk dog, at streamingen forsvinder samtidig med
mobilabonnementet — så tegn de tjenester, du vil beholde, separat <em>før</em> du skifter,
så du ikke står uden midt i en serie.</p>

<p>Se den fulde fremgangsmåde i vores guide til
<a href="/guides/skift-mobilselskab/">at skifte mobilselskab</a>.</p>

</section>
"""


def boern(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Til et barn er det vigtigste ikke prisen, men at regningen
ikke kan løbe løbsk. Vælg et abonnement uden binding med en lille datapakke, og slå
datastop til med det samme. Priserne starter omkring {kr(D['pris_boern'])} kr. om måneden.
Til de yngste børn er taletid eller et abonnement uden data ofte det tryggeste valg, fordi
udgiften er låst på forhånd.</p>
</div>

<h2>Det vigtigste først: fjern risikoen for store regninger</h2>

<p>Der findes tre måder, en børnetelefon kan producere en ubehagelig regning på, og alle
tre kan lukkes på under fem minutter. Gør det, inden telefonen bliver afleveret.</p>

<ol class="trin">
<li><strong>Slå datastop til</strong>
Det er den vigtigste enkeltindstilling. Med datastop stopper forbindelsen, når pakken er
brugt, i stedet for at der købes ekstra data automatisk. Findes i udbyderens app under
forbrug eller indstillinger.</li>
<li><strong>Spær for overtakserede numre og indholdstjenester</strong>
Sms-afstemninger, spil, donationsnumre og servicenumre kan koste mange penge meget
hurtigt. De fleste udbydere kan spærre for dem helt — ring og bed om det.</li>
<li><strong>Slå dataroaming fra</strong>
Uden for EU kan data koste ekstremt meget. Slå det fra i telefonen, og bed eventuelt
udbyderen om at spærre for roaming uden for EU.</li>
</ol>

<div class="advarsel">
<p><strong>Køb i app-butikker er en fjerde kilde til regninger</strong>, og den håndteres
ikke af mobilselskabet. Sæt en aldersgrænse og krav om kode ved køb op i telefonens
familieindstillinger. Det er en separat opgave fra abonnementet, men det er ofte den, der
koster mest.</p>
</div>

<h2>Abonnement, taletid eller uden data?</h2>

<p>Der er tre modeller, og valget afhænger mest af barnets alder og af, hvor meget I vil
kunne styre.</p>

<table>
<thead><tr><th>Model</th><th>Sådan virker det</th><th>Passer typisk til</th></tr></thead>
<tbody>
<tr><td><strong>Taletid</strong></td><td>Forudbetalt. Når pengene er brugt, stopper det. Ingen regning kan overraske.</td><td>De yngste, cirka 7–11 år</td></tr>
<tr><td><strong>Abonnement uden data</strong></td><td>Fast lav pris, tale og sms, intet mobilt internet uden for wi-fi</td><td>Cirka 9–12 år, eller hvor skærmtid skal begrænses</td></tr>
<tr><td><strong>Lille dataabonnement</strong></td><td>Fast pris med 5–15 GB og datastop slået til</td><td>Cirka 11 år og opefter</td></tr>
</tbody>
</table>

<p>Vores anbefaling til den yngste gruppe er taletid, fordi den fjerner risikoen helt. Til
mellemgruppen er et abonnement uden data en god mellemvej: barnet kan altid ringe og skrive
til jer, men telefonen bliver ikke en underholdningsmaskine i skolegården. Fra teenagealderen
er et lille dataabonnement med datastop som regel den mest realistiske løsning — og det er
også her, prisen begynder at kunne betale sig i forhold til taletid.</p>

<h2>Hvor meget data har et barn brug for?</h2>

<p>Mindre end de fleste tror, fordi børn har wi-fi hjemme, hos vennerne og ofte på skolen.
Det, der bruger data, er video og musik på farten.</p>

<table>
<thead><tr><th>Alder</th><th>Typisk behov</th><th>Bemærkning</th></tr></thead>
<tbody>
<tr><td>7–10 år</td><td>0–2 GB</td><td>Telefonen bruges primært til at ringe hjem</td></tr>
<tr><td>10–12 år</td><td>2–5 GB</td><td>Beskeder, lidt musik, enkelte videoer</td></tr>
<tr><td>12–15 år</td><td>5–15 GB</td><td>Sociale medier og musik fylder mest</td></tr>
<tr><td>15+ år</td><td>15–30 GB</td><td>Video på farten begynder at fylde for alvor</td></tr>
</tbody>
</table>

<p>Start hellere lavt og gå op, hvis pakken løber tør. Med datastop slået til sker der
ikke andet, end at mobildata holder op med at virke indtil næste periode — og det er en
langt bedre læreproces end en overraskelsesregning.</p>

<h2>Skal barnet stå på abonnementet?</h2>

<p>Nej. Mindreårige kan som udgangspunkt ikke selv indgå bindende aftaler, og abonnementet
oprettes derfor i en forælders navn. Det betyder også, at det er dig, der hæfter for
regningen, og at det er dig, der kan ændre indstillinger, spærre og opsige.</p>

<p>Nogle udbydere har familieløsninger, hvor flere numre samles under én konto med fælles
oversigt. Det kan være praktisk, men regn efter: flere separate discountabonnementer er
ofte billigere end en familiepakke, selv med rabat. Sammenlign den samlede månedspris, ikke
rabattens størrelse.</p>

<div class="tip">
<h3>Tal om det, inden telefonen udleveres</h3>
<p>De fleste problemer med børns mobilforbrug er ikke tekniske. Aftal på forhånd, hvad
telefonen må bruges til, hvornår den er slukket, og hvad der sker, hvis dataen er brugt
den 20. i måneden. Datastop er den tekniske sikring — aftalen er den vigtige del.</p>
</div>

<h2>Binding, telefon og den samlede regning</h2>

<p>Køb ikke telefon på afbetaling sammen med barnets abonnement. Det binder jer i typisk
24 eller 36 måneder til et selskab, og restgælden skal indfries, hvis I vil skifte. Børns
telefoner går i stykker, bliver væk og skal skiftes, og en bindingsperiode gør alle de
situationer dyrere.</p>

<p>Køb i stedet en billig eller brugt telefon kontant og vælg et abonnement uden binding.
Så kan I skifte, når behovet ændrer sig — og det gør det hurtigt i den alder.</p>

<h2>Sikkerhed og tryghed ud over regningen</h2>

<ul>
<li><strong>Gem vigtige numre</strong> i telefonen, ikke kun i en app, så barnet kan ringe
til jer, selvom telefonen er uden data.</li>
<li><strong>Slå positionsdeling til</strong>, hvis I bruger det — men aftal det med barnet
frem for at gøre det i skjul.</li>
<li><strong>Sæt kode på telefonen</strong> og sørg for, at I som forældre kender den, mens
barnet er lille.</li>
<li><strong>Tjek at nødopkald virker.</strong> Nødopkald til 112 fungerer uanset
abonnement, også hvis taletiden er brugt op.</li>
</ul>

<h2>Sådan sætter I det op på en aften</h2>

<ol class="trin">
<li><strong>Vælg abonnement uden binding</strong>
Taletid eller lille datapakke, afhængigt af alder.</li>
<li><strong>Bestil i din egen NemID/MitID</strong>
Abonnementet skal stå i en voksens navn.</li>
<li><strong>Slå datastop og spærringer til med det samme</strong>
Datastop, spærring for overtakserede numre, dataroaming fra.</li>
<li><strong>Sæt familieindstillinger op i telefonen</strong>
Kode ved køb, aldersgrænser, skærmtid.</li>
<li><strong>Gennemgå aftalen med barnet</strong>
Hvad telefonen er til, og hvad der sker, når dataen er brugt.</li>
</ol>

</section>
"""


def esim(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Et eSIM er et digitalt simkort, der er indbygget i
telefonen og aktiveres med en QR-kode i stedet for et fysisk kort. Du kan være i gang få
minutter efter bestilling i stedet for at vente på posten. Stort set alle danske udbydere
tilbyder eSIM, som regel uden ekstra betaling, og priserne er de samme som med fysisk
simkort — abonnementer med eSIM starter fra {kr(D['pris_esim'])} kr. om måneden.</p>
</div>

<h2>Hvad et eSIM er, og hvad det ikke er</h2>

<p>Et eSIM er ikke et løst kort, du sætter i telefonen. Det er en chip, der sidder fast i
telefonen fra fabrikken, og som kan programmeres med en abonnementsprofil. Når du bestiller
et abonnement med eSIM, får du en QR-kode, du scanner — og så er profilen hentet ned på
telefonen.</p>

<p>Funktionelt er der ingen forskel på et eSIM og et fysisk simkort. Samme dækning, samme
hastighed, samme nummer, samme pris. Forskellen ligger udelukkende i, hvordan abonnementet
kommer ind i telefonen, og i hvad det gør muligt bagefter.</p>

<table>
<thead><tr><th></th><th>eSIM</th><th>Fysisk simkort</th></tr></thead>
<tbody>
<tr><td><strong>Klar til brug</strong></td><td>Få minutter efter bestilling</td><td>1–3 hverdage med posten</td></tr>
<tr><td><strong>Flere numre</strong></td><td>Flere profiler på samme telefon</td><td>Kun ét kort ad gangen (eller to i dual-sim)</td></tr>
<tr><td><strong>Skift af telefon</strong></td><td>Kræver overførsel eller ny kode</td><td>Flyt kortet fysisk</td></tr>
<tr><td><strong>Kan blive væk</strong></td><td>Nej</td><td>Ja</td></tr>
<tr><td><strong>Understøttelse</strong></td><td>Telefoner fra de senere år</td><td>Stort set alle telefoner</td></tr>
</tbody>
</table>

<h2>De tre situationer hvor eSIM virkelig betaler sig</h2>

<h3>1. Du skifter selskab og vil ikke vente</h3>
<p>Det er den mest almindelige grund. Bestiller du om formiddagen, kan du være kunde hos
det nye selskab samme eftermiddag. Med fysisk kort venter du på posten, og for mange er
netop den ventetid grunden til, at skiftet aldrig bliver til noget.</p>

<h3>2. Du vil have arbejde og privat på samme telefon</h3>
<p>De fleste moderne telefoner kan have flere eSIM-profiler installeret og to aktive
samtidig. Det betyder to numre i én telefon, hvor du selv bestemmer, hvilket nummer der
bruges til opkald, sms og data. Du kan slå arbejdsnummeret fra om aftenen uden at skulle
skifte kort.</p>

<h3>3. Du rejser uden for EU</h3>
<p>Det er her, eSIM sparer flest penge. Uden for EU gælder roamingreglerne ikke, og data
kan være meget dyrt. Med eSIM kan du købe et lokalt data-eSIM til destinationen, samtidig
med at du beholder dit danske nummer aktivt til opkald og sms. Du behøver ikke skifte kort
og risikerer ikke at tabe det danske kort på en strand i Thailand.</p>

<div class="tip">
<h3>Rejsetip der virker</h3>
<p>Sæt det danske abonnement til kun at håndtere opkald og sms, og lad rejse-eSIM'et stå
for data. Så kan folk stadig ringe til dit danske nummer, mens dit dataforbrug kører på en
billig lokal pakke. Husk at slå dataroaming fra på den danske linje, så telefonen ikke
falder tilbage på den.</p>
</div>

<h2>Understøtter min telefon eSIM?</h2>

<p>Telefoner fra de senere år gør det stort set alle sammen. Sådan tjekker du:</p>

<ul>
<li><strong>iPhone:</strong> Indstillinger → Generelt → Om. Er der en linje med eSIM eller
tilgængelig SIM, understøtter telefonen det. Nyere modeller solgt i visse lande har
udelukkende eSIM og ingen kortplads.</li>
<li><strong>Android:</strong> Indstillinger → Om telefonen, eller Indstillinger → Netværk
og internet → SIM. Understøttelsen varierer mere mellem producenter og modeller end på
iPhone, så tjek din konkrete model.</li>
<li><strong>Simlås:</strong> Er telefonen købt gennem et selskab i udlandet, kan den være
simlåst. Så kan et eSIM fra en anden udbyder ikke aktiveres, før låsen er fjernet.</li>
</ul>

<h2>Sådan kommer du i gang — trin for trin</h2>

<ol class="trin">
<li><strong>Vælg eSIM ved bestillingen</strong>
Du vælger det i stedet for fysisk simkort. Har du eksisterende nummer, angiver du det, så
det flyttes med.</li>
<li><strong>Sørg for at være på wi-fi</strong>
Aktiveringen kræver internetforbindelse, og den kan du ikke få via det abonnement, du er
ved at oprette.</li>
<li><strong>Scan QR-koden</strong>
Du får den på mail eller i udbyderens app. Telefonens kamera genkender den, og du bliver
ledt gennem installationen.</li>
<li><strong>Navngiv linjen</strong>
Kald den for eksempel Privat og Arbejde. Det gør det langt nemmere at holde styr på, hvis
du har flere.</li>
<li><strong>Vælg hvad der bruges til hvad</strong>
Hvilken linje der er standard til opkald, sms og mobildata. Kan ændres når som helst.</li>
<li><strong>Test det</strong>
Ring et opkald, send en sms, og slå wi-fi fra for at tjekke, at mobildata virker.</li>
</ol>

<h2>Det du skal være opmærksom på</h2>

<div class="plusminus">
  <div class="pm pm-plus"><h3>Fordele</h3><ul>
    <li>I gang få minutter efter bestilling</li>
    <li>Kan ikke tabes eller blive væk</li>
    <li>Flere numre i samme telefon</li>
    <li>Billig data i udlandet uden at skifte kort</li>
    <li>Hos de fleste danske udbydere uden ekstra betaling</li>
  </ul></div>
  <div class="pm pm-minus"><h3>Ulemper</h3><ul>
    <li>Kan ikke bare flyttes fysisk til en ny telefon</li>
    <li>Kræver wi-fi ved aktivering</li>
    <li>Ældre telefoner understøtter det ikke</li>
    <li>Simlåste telefoner kan give problemer</li>
    <li>Låner du en telefon ud, kan du ikke bare give dit kort med</li>
  </ul></div>
</div>

<div class="advarsel">
<p><strong>Ved telefonskift:</strong> Et eSIM kan ikke flyttes fysisk. Nyere telefoner har
en overførselsfunktion, der kan flytte profilen direkte mellem to enheder. Virker den ikke,
skal du bede udbyderen om en ny QR-kode. Det er gratis hos de fleste, men gør det
<em>inden</em> du nulstiller den gamle telefon — ellers kan du stå uden forbindelse.</p>
</div>

<h2>eSIM og sikkerhed</h2>

<p>Et eSIM er som udgangspunkt sikrere end et fysisk kort, netop fordi det ikke kan tages
ud af telefonen. Ved tyveri kan en tyv ikke flytte dit nummer til en anden telefon ved at
tage kortet — og det er faktisk relevant, fordi mange bekræftelseskoder fra bank og MitID
sendes på sms til dit nummer.</p>

<p>Bliver telefonen stjålet, skal du stadig kontakte din udbyder og få nummeret spærret.
Det er den samme fremgangsmåde som ved et fysisk kort.</p>

<h2>Koster eSIM ekstra?</h2>

<p>Hos hovedparten af de danske udbydere er eSIM gratis, og prisen på abonnementet er
nøjagtig den samme, uanset om du vælger eSIM eller fysisk kort. Enkelte tager et mindre
gebyr for at udstede en ny profil, hvis du får brug for det flere gange — for eksempel ved
telefonskift. Tjek vilkårene, hvis du regner med at skifte telefon ofte.</p>

</section>
"""
