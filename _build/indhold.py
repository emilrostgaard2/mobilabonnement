# -*- coding: utf-8 -*-
"""Langt redaktionelt indhold. Adskilt fra skabelonlaget, så tekst kan rettes
uden at røre koden."""

from skabelon import e, kr, gb_tekst

# ============================================================================
#  BILLIGSTE MOBILABONNEMENT — hovedsiden
# ============================================================================

def billigste_brodtekst(d):
    """d = dict med afledte tal fra data."""
    return f"""
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort svar:</strong> Det billigste mobilabonnement i Danmark koster
{kr(d['min_pris'])} kr. om måneden — det er et taleabonnement uden data. Vil du have
mobildata med, starter priserne ved {kr(d['min_pris_data'])} kr. for {d['min_data_gb']} GB
med fri tale og fri sms uden binding. Skal du bruge over 50 GB, starter priserne omkring
{kr(d['pris_stor'])} kr., og fri data fås fra {kr(d['pris_fri'])} kr. om måneden.
Prisforskellen mellem billigste og dyreste abonnement med samme indhold er ofte over
100 kr. om måneden — altså mere end 1.200 kr. om året for præcis det samme.</p>
</div>

<h2>Hvad koster et mobilabonnement i Danmark i dag?</h2>

<p>Det danske mobilmarked er et af Europas billigste, og det skyldes en usædvanlig hård
konkurrence mellem tre netværksejere og et stort antal selskaber, der lejer sig ind på
deres master. Resultatet er, at prisen for det samme produkt varierer voldsomt afhængigt
af, hvilket brand der står på regningen — ikke af hvilken kvalitet du får.</p>

<p>For at give et realistisk billede har vi delt markedet op i fire prisniveauer. Langt de
fleste danskere befinder sig i de to midterste, men betaler priser fra det øverste, fordi
de aldrig har skiftet.</p>

<table>
<thead><tr><th>Niveau</th><th>Pris pr. md.</th><th>Typisk indhold</th><th>Passer til</th></tr></thead>
<tbody>
<tr><td><strong>Discount</strong></td><td>{kr(d['min_pris_data'])}–99 kr.</td><td>Fri tale og sms, 5–20 GB</td><td>Let bruger, wi-fi det meste af dagen</td></tr>
<tr><td><strong>Mellem</strong></td><td>100–149 kr.</td><td>Fri tale og sms, 25–60 GB</td><td>Almindelig bruger med daglig pendling</td></tr>
<tr><td><strong>Stor</strong></td><td>150–199 kr.</td><td>80–150 GB eller fri data</td><td>Streaming på farten, hotspot til laptop</td></tr>
<tr><td><strong>Premium</strong></td><td>200–350 kr.</td><td>Fri data, streaming, bedste dækning</td><td>Landdistrikter, erhverv, samlet husstand</td></tr>
</tbody>
</table>

<p>Den vigtigste erkendelse er, at niveauerne ikke afspejler kvalitetsforskelle i selve
mobilforbindelsen. Et abonnement til {kr(d['min_pris_data'])} kr. og et til 300 kr. kan køre på
nøjagtig det samme netværk, med den samme dækning, de samme master og den samme hastighed.
Det, du betaler ekstra for i toppen, er tillægsydelser, kundeservice og i visse tilfælde
adgang til det mest udbyggede net — ikke bedre mobilnet i sig selv.</p>

<h2>Sådan finder du det billigste mobilabonnement, der passer til dig</h2>

<p>Det billigste abonnement på markedet er sjældent det billigste abonnement <em>for dig</em>.
Vælger du for lidt data, betaler du for overforbrug eller står uden internet den 27. i
måneden. Vælger du for meget, betaler du hver måned for gigabyte, du aldrig rører. Her er
den rækkefølge, vi anbefaler at gøre det i.</p>

<ol class="trin">
<li><strong>Find dit faktiske dataforbrug</strong>
På iPhone: Indstillinger → Mobildata. På Android: Indstillinger → Netværk og internet →
Dataforbrug. Kig på de <em>seneste tre måneder</em>, ikke den seneste uge, og notér det
højeste tal. Læg 20 procent til som buffer. Det er dit reelle behov, og for de fleste
danskere er tallet markant lavere, end de tror.</li>

<li><strong>Tjek dækningen på din adresse</strong>
Alle tre netværksejere har dækningskort på deres hjemmesider. Tjek din bopæl, din
arbejdsplads og din pendlerrute. Bor du centralt i en større by, kan du reelt vælge frit.
Bor du på landet, i et sommerhusområde eller ved kysten, kan forskellen mellem nettene
være afgørende, og så bør dækning veje tungere end de 30 kr., du kan spare.</li>

<li><strong>Sammenlign på pris pr. GB — ikke på månedspris</strong>
Et abonnement til 79 kr. med 5 GB koster 15,80 kr. pr. GB. Et abonnement til 129 kr. med
50 GB koster 2,58 kr. pr. GB. Det dyreste abonnement er altså seks gange billigere pr.
gigabyte. Vores tabeller viser tallet direkte, så du kan sortere efter det.</li>

<li><strong>Læs det med småt om kampagneprisen</strong>
Rigtig mange lave priser gælder i seks måneder, hvorefter prisen stiger. Det er ikke
nødvendigvis en dårlig aftale — men det er en aftale, du skal sætte en kalenderpåmindelse
på. Se altid, hvad prisen bliver <em>efter</em> kampagnen, og gang op over tolv måneder.</li>

<li><strong>Bestil og lad dem flytte nummeret</strong>
Du skal ikke opsige noget selv. Den nye udbyder henter dit nummer fra den gamle, typisk
inden for et par hverdage, og du har normalt højst få minutters afbrydelse. Din gamle
aftale lukkes automatisk.</li>
</ol>

<div class="tip">
<h3>Det ene råd der sparer flest penge</h3>
<p>Slå datastop til i din udbyders app, så snart abonnementet er oprettet. Uden datastop
kan overforbrug koste flere hundrede kroner på en enkelt regning, særligt hvis telefonen
bruges som hotspot. Med datastop kan regningen ganske enkelt ikke løbe løbsk. Det tager
under et minut at aktivere og er den mest oversete indstilling på hele markedet.</p>
</div>

<h2>De tre netværk — og hvorfor de afgør, hvad du bør betale</h2>

<p>Der findes kun tre mobilnetværk i Danmark: TDC NET, Telenor og 3. Alle andre selskaber
lejer sig ind hos en af dem. Det betyder, at et discountselskab bruger de samme master som
et premiumselskab, og at spørgsmålet aldrig er, om nettet er "rigtigt" — kun hvilket net
udbyderen lejer sig ind på, og på hvilke vilkår.</p>

<table>
<thead><tr><th>Netværk</th><th>Styrke</th><th>Svaghed</th><th>Kendte brands på nettet</th></tr></thead>
<tbody>
<tr><td><strong>TDC NET</strong></td><td>Landets mest udbyggede net. Bedst i landdistrikter, sommerhusområder, tog og indendørs.</td><td>Brands på nettet ligger typisk højere i pris.</td><td>YouSee, Telmore</td></tr>
<tr><td><strong>Telenor</strong></td><td>Bred dækning og stærk balance mellem pris og kvalitet.</td><td>Enkelte huller i tyndt befolkede områder.</td><td>CBB Mobil</td></tr>
<tr><td><strong>3</strong></td><td>Høje hastigheder og stor kapacitet i byerne. Tidligt ude med 5G.</td><td>Mere varierende i landdistrikter og langs kysten.</td><td>Oister</td></tr>
</tbody>
</table>

<p>Der er en detalje, som få sammenligningssider nævner, men som er værd at kende. Nogle
aftaler mellem netværksejere og de selskaber, der lejer sig ind, indeholder begrænsninger
— for eksempel et loft over hastigheden eller lavere prioritet, når nettet er belastet i
myldretiden. Det er ikke svindel, og det mærkes sjældent i praksis for almindelig brug,
men det er forklaringen på, at to abonnementer på "samme net" ikke altid opfører sig ens.
Står der ikke noget om det i vilkårene, kan du regne med fuld hastighed.</p>

<div class="advarsel">
<p><strong>Vær opmærksom:</strong> Netværksaftaler ændrer sig. Et selskab kan skifte fra ét
net til et andet, og det sker uden større opmærksomhed. Tjek altid netværksangivelsen på
udbyderens egen side, hvis dækning er afgørende for dig — vores oplysninger opdateres
løbende, men udbyderen er altid den primære kilde.</p>
</div>

<h2>Billigst efter hvor meget data du bruger</h2>

<p>Nedenfor har vi delt markedet op efter, hvad folk rent faktisk søger efter. Tallene er
de laveste, vi har fundet i hver kategori på tværs af alle udbydere i vores sammenligning.</p>

<table>
<thead><tr><th>Behov</th><th>Datamængde</th><th>Billigste pris fundet</th><th>Hvem passer det til</th></tr></thead>
<tbody>
<tr><td>Minimal bruger</td><td>Op til 10 GB</td><td>fra {kr(d['pris_lille'])} kr.</td><td>Wi-fi hjemme og på arbejde, lidt musik i bilen</td></tr>
<tr><td>Almindelig bruger</td><td>15–30 GB</td><td>fra {kr(d['pris_mellem'])} kr.</td><td>Sociale medier, podcasts, navigation, lidt video</td></tr>
<tr><td>Storforbruger</td><td>50–100 GB</td><td>fra {kr(d['pris_stor'])} kr.</td><td>Video på farten, hotspot til laptop, pendling</td></tr>
<tr><td>Ubegrænset</td><td>Fri data</td><td>fra {kr(d['pris_fri'])} kr.</td><td>Ingen wi-fi hjemme, streaming hele dagen, deling</td></tr>
</tbody>
</table>

<p>Læg mærke til springet mellem kategorierne. Fra den mindste til den mellemste kategori
er prisforskellen typisk 20–30 kr. om måneden, mens datamængden tredobles. Det er
grunden til, at vi sjældent anbefaler det allermindste abonnement til andre end dem, der
virkelig kun bruger telefonen til opkald. For en tyver mere får du så meget mere plads, at
risikoen for overforbrug forsvinder helt.</p>

<h2>De skjulte omkostninger, folk overser</h2>

<h3>Oprettelsesgebyr</h3>
<p>De fleste danske selskaber er gået væk fra oprettelsesgebyr, men det findes stadig, og
det kan løbe op i et par hundrede kroner. Et gebyr betyder ikke automatisk, at aftalen er
dårlig — regn det ud over den periode, du forventer at blive: 199 kr. i oprettelse svarer
til godt 16 kr. om måneden på et år, og det æder en billig pris hurtigt op, hvis du
alligevel skifter igen efter et halvt år.</p>

<h3>Prisstigning efter kampagne</h3>
<p>Det er den dyreste fælde på markedet. Et abonnement, der annonceres til 49 kr., kan
koste 149 kr. fra måned syv. Over tolv måneder betaler du så i gennemsnit 99 kr. — ikke 49.
Vores tabeller viser normalprisen, hvor den findes, men tjek altid vilkårene på
udbyderens side før bestilling.</p>

<h3>Overforbrug af data</h3>
<p>Uden datastop koster ekstra data typisk et fast beløb pr. påbegyndt enhed, og det kan
blive dyrt overraskende hurtigt. Slå datastop til. Har du børn på abonnementet, er det ikke
til diskussion.</p>

<h3>Brug uden for EU</h3>
<p>Inden for EU gælder roamingreglerne, og dit danske abonnement virker som herhjemme
inden for de grænser, der står i vilkårene. Uden for EU — herunder Storbritannien, Schweiz,
Tyrkiet og USA — gælder helt andre takster, og det er her, de virkelig store regninger
opstår. Skal du rejse, så tjek altid taksterne for netop det land, og overvej at slå
dataroaming fra og bruge et lokalt eSIM i stedet.</p>

<h2>Hvilket abonnement passer til din situation?</h2>

<div class="kortgitter kg-2" style="margin:1.8rem 0">
  <div class="kort">
    <h3>Studerende</h3>
    <p>Du er meget på farten, streamer musik og video, og har sjældent wi-fi mellem
    forelæsninger. Gå efter 30–50 GB til under 130 kr. uden binding, så du kan skifte, når
    du flytter. Undgå lange bindinger på telefonabonnement med afdrag.</p>
  </div>
  <div class="kort">
    <h3>Familie med børn</h3>
    <p>Flere abonnementer hos samme udbyder giver ofte rabat, men regn efter — fire
    separate discountabonnementer er tit billigere end en familiepakke. Datastop på
    børnenes numre er vigtigere end prisen.</p>
  </div>
  <div class="kort">
    <h3>Pendler</h3>
    <p>Du bruger telefonen i tog og bil dagligt, hvor dækningen svinger. Her betaler
    netværket sig: TDC NET har historisk den bedste dækning langs jernbanen. Vælg 50 GB
    eller derover.</p>
  </div>
  <div class="kort">
    <h3>Senior eller let bruger</h3>
    <p>Ringer, sender sms, bruger lidt internet. 5–10 GB rækker langt. Til gengæld er
    telefonisk kundeservice ofte mere værd end de 40 kr., der kan spares hos en rent
    digital udbyder.</p>
  </div>
  <div class="kort">
    <h3>Dig med familie i udlandet</h3>
    <p>Ringer du fast til udlandet fra Danmark, er det ikke roaming — det er
    udlandsopkald, og prisen varierer enormt. Specialiserede udbydere kan spare dig
    hundredvis af kroner om måneden. Tjek at netop dit land og nummertype er med.</p>
  </div>
  <div class="kort">
    <h3>Hjemmearbejdende uden fastnet</h3>
    <p>Bruger du mobilen som hotspot til laptop, skal du op i fri data eller mindst 100 GB.
    Regn med at et hotspot-tungt hjemmekontor sagtens kan bruge 150 GB om måneden.</p>
  </div>
</div>

<h2>Sådan skifter du mobilselskab — trin for trin</h2>

<p>At skifte mobilselskab i Danmark er blandt de nemmeste forbrugerhandlinger, der findes.
Det er lovmæssigt sikret, at du kan tage dit nummer med, og hele processen håndteres af den
nye udbyder.</p>

<ol class="trin">
<li><strong>Bestil hos den nye udbyder</strong>
Du oplyser dit nuværende mobilnummer og angiver, at du vil beholde det. Du skal ikke
kontakte dit gamle selskab overhovedet.</li>
<li><strong>Vent på simkort eller aktivér eSIM</strong>
Fysisk simkort tager typisk 1–3 hverdage med posten. Vælger du eSIM, får du en kode med
det samme og kan være i gang inden for få minutter.</li>
<li><strong>Nummeret flyttes</strong>
Flytningen sker normalt inden for få hverdage. Selve overgangen tager sjældent mere end
nogle minutter, og du får typisk besked om, hvornår det sker.</li>
<li><strong>Din gamle aftale lukkes automatisk</strong>
Den gamle udbyder afslutter abonnementet, når nummeret er flyttet. Vær opmærksom på
eventuel binding eller restgæld på en telefon, købt på afbetaling — det følger ikke med.</li>
</ol>

<div class="tip">
<h3>Har du binding?</h3>
<p>Har du købt telefon på afbetaling, hænger den ofte sammen med abonnementet. Du kan
stadig skifte, men du skal typisk indfri restgælden på telefonen. Ring til dit nuværende
selskab og bed om at få oplyst restgæld og bindingsperiode, før du bestiller nyt. Det
tager fem minutter og forhindrer en ubehagelig slutregning.</p>
</div>

<h2>Vores metode</h2>

<p>Vi mener, at en sammenligningsside kun er noget værd, hvis man kan se, hvordan tallene
er fremkommet. Derfor lægger vi metoden åbent frem.</p>

<ul>
<li><strong>Datagrundlag.</strong> Priser og vilkår hentes fra udbydernes egne offentlige
prislister og kontrolleres manuelt. Vi bruger normalpriser, hvor en kampagnepris udløber
inden for tolv måneder, og oplyser begge dele, hvor det er relevant.</li>
<li><strong>Sortering.</strong> Alle tabeller sorteres som udgangspunkt efter laveste
månedspris. Provision påvirker ikke rækkefølgen, og udbydere kan ikke købe sig til en
placering.</li>
<li><strong>Pris pr. GB</strong> beregnes som månedspris divideret med inkluderet
datamængde. Abonnementer med fri data indgår ikke i den beregning, da tallet ikke er
meningsfuldt.</li>
<li><strong>Hvad vi ikke gør.</strong> Vi tester ikke hastigheder selv. Til dækning og
hastighed henviser vi til netværksejernes egne dækningskort og til uafhængige målinger,
fordi de bygger på langt større datamængder, end vi kan producere.</li>
<li><strong>Fejl.</strong> Finder du en pris, der ikke stemmer, så skriv til os. Vi retter
og noterer datoen.</li>
</ul>

<p>Læs mere om <a href="/metode/">metoden bag vores anbefalinger</a> og om
<a href="/saadan-tjener-vi-penge/">hvordan vi tjener penge</a>.</p>

</section>
"""


# ============================================================================
#  FRI DATA
# ============================================================================

def fridata_brodtekst(d):
    return f"""
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort svar:</strong> Mobilabonnement med fri data koster fra
{kr(d['pris_fri'])} kr. om måneden i Danmark. Men "fri data" er ikke altid helt frit —
de fleste abonnementer har begrænsninger på brug i udlandet, og nogle har vilkår om
rimeligt forbrug. For de fleste danskere er 50–100 GB både billigere og rigeligt.</p>
</div>

<h2>Har du overhovedet brug for fri data?</h2>

<p>Det korte svar er: sandsynligvis ikke. Fri data er markedets bedste eksempel på et
produkt, folk køber af tryghed frem for behov. Langt de fleste danskere bruger under
30 GB om måneden, og selv storforbrugere lander sjældent over 100 GB. Betaler du for fri
data og bruger 25 GB, betaler du typisk 70–100 kr. om måneden for ingenting — knap
1.000 kr. om året.</p>

<p>Der er dog fire situationer, hvor fri data reelt er det rigtige valg, og hvor vi
anbefaler det uden forbehold:</p>

<ul>
<li><strong>Du har ikke fastnetinternet.</strong> Bruger du mobilen som eneste
internetforbindelse i hjemmet via hotspot, ryger forbruget hurtigt over 150 GB.</li>
<li><strong>Du deler forbindelsen.</strong> Hotspot til laptop, tablet og eventuelt
familiemedlemmer får forbruget til at eksplodere.</li>
<li><strong>Du streamer video på farten dagligt.</strong> En time video i høj kvalitet
kan koste flere gigabyte. Ser du to timer om dagen i toget, er 100 GB hurtigt brugt.</li>
<li><strong>Dit forbrug svinger voldsomt.</strong> Har du måneder med 20 GB og måneder
med 120 GB, er fri data ofte billigere end at betale for overforbrug i spidsmånederne.</li>
</ul>

<h2>Hvad "fri data" betyder i praksis</h2>

<p>Der er tre ting, du skal læse efter i vilkårene, før du bestiller et abonnement med
fri data. De er sjældent skjulte, men de står heller ikke med store bogstaver.</p>

<table>
<thead><tr><th>Begrænsning</th><th>Hvad det betyder</th><th>Hvornår det rammer dig</th></tr></thead>
<tbody>
<tr><td>Loft i EU</td><td>Fri data gælder i Danmark. I EU er der typisk et loft i gigabyte.</td><td>På ferie eller ved længere ophold i udlandet</td></tr>
<tr><td>Rimeligt forbrug</td><td>Vilkår mod ekstremt eller erhvervsmæssigt forbrug.</td><td>Ved forbrug langt over det normale, fx flere hundrede GB</td></tr>
<tr><td>Hastighed</td><td>Nogle abonnementer har hastighedsloft eller lavere prioritet i myldretid.</td><td>Ved streaming i høj opløsning på belastede tidspunkter</td></tr>
</tbody>
</table>

<p>Bemærk især EU-loftet. Det er den begrænsning, flest støder ind i, fordi den rammer
netop når man er på ferie og bruger telefonen til kort, oversættelse og billeder. Et
abonnement med fri data i Danmark, men 30 GB i EU, er stadig et fremragende produkt — du
skal bare vide det på forhånd.</p>

<div class="tip">
<h3>Regn det efter, før du vælger fri data</h3>
<p>Tag dit højeste dataforbrug de seneste seks måneder. Læg 30 procent til. Er tallet
under 80 GB, er et abonnement med fast datamængde næsten altid billigere — også når du
regner en enkelt overforbrugsmåned med. Er tallet over 120 GB, vælg fri data.</p>
</div>

<h2>Fri data mod stort abonnement — hvad kan bedst betale sig?</h2>

<p>Lad os regne på det med konkrete tal fra vores sammenligning. Et abonnement med fri
data koster fra {kr(d['pris_fri'])} kr. Et abonnement med 100 GB koster fra
{kr(d['pris_stor'])} kr. Forskellen er {kr(max(0, d['pris_fri'] - d['pris_stor']))} kr. om
måneden, altså {kr(max(0, d['pris_fri'] - d['pris_stor']) * 12)} kr. om året.</p>

<p>Spørgsmålet er derfor ikke, om fri data er dyrere — det er, om du overskrider 100 GB
ofte nok til, at det kan betale sig. Overskrider du i to måneder om året, er det stort set
altid billigere at have det store abonnement og acceptere en enkelt ekstra regning eller
en periode med nedsat hastighed. Overskrider du hver måned, er fri data det rigtige.</p>

<h2>Hvad bruger man egentlig data på?</h2>

<p>Det er svært at vurdere sit behov uden at vide, hvad tingene koster. Her er
tommelfingertal for typisk forbrug pr. time — de svinger med kvalitet og app, men giver
et brugbart udgangspunkt.</p>

<table>
<thead><tr><th>Aktivitet</th><th>Cirka forbrug</th><th>10 GB rækker til</th></tr></thead>
<tbody>
<tr><td>Musikstreaming</td><td>ca. 70–150 MB pr. time</td><td>ca. 80–140 timer</td></tr>
<tr><td>Sociale medier</td><td>ca. 100–350 MB pr. time</td><td>ca. 30–100 timer</td></tr>
<tr><td>Video i standardkvalitet</td><td>ca. 0,7–1 GB pr. time</td><td>ca. 10–14 timer</td></tr>
<tr><td>Video i HD</td><td>ca. 2–3 GB pr. time</td><td>ca. 3–5 timer</td></tr>
<tr><td>Videoopkald</td><td>ca. 0,5–1,5 GB pr. time</td><td>ca. 7–20 timer</td></tr>
<tr><td>Navigation og kort</td><td>ca. 5–20 MB pr. time</td><td>meget længe</td></tr>
</tbody>
</table>

<p>Det springende punkt er video. Alt andet end video er stort set gratis i den store
sammenhæng. Er du i tvivl om, hvorvidt du har brug for fri data, handler spørgsmålet reelt
kun om, hvor mange timers video du ser uden for wi-fi.</p>

<div class="advarsel">
<p><strong>Et konkret sparetip:</strong> Slå automatisk afspilning af video fra i dine
sociale medier, og sæt streamingtjenester til kun at hente i høj kvalitet på wi-fi. De to
indstillinger halverer typisk dataforbruget og kan i praksis rykke dig ned i en billigere
abonnementskategori.</p>
</div>

</section>
"""


# ============================================================================
#  GUIDES
# ============================================================================

GUIDE_SKIFT = """
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort svar:</strong> Du skifter mobilselskab ved at bestille hos den nye udbyder
og oplyse dit nuværende nummer. Den nye udbyder klarer resten. Du skal ikke opsige noget
selv, du beholder dit nummer, og afbrydelsen varer typisk få minutter. Hele processen tager
normalt 1–5 hverdage.</p>
</div>

<h2>Derfor er det nemmere, end du tror</h2>

<p>Nummerportering er en rettighed i Danmark, og udbyderne er forpligtet til at hjælpe dig
med at flytte. Det betyder i praksis, at det selskab, du forlader, ikke kan forhindre eller
forsinke skiftet, og at du ikke skal igennem en opsigelsessamtale, hvor nogen forsøger at
holde på dig. Du bestiller nyt, og systemet ordner resten.</p>

<p>Alligevel udskyder rigtig mange danskere skiftet i årevis, og det er dyrt. Har du haft
samme abonnement i tre år, er sandsynligheden stor for, at du betaler mere end nye kunder
for det samme produkt. Det er ikke ond vilje fra udbyderne — det er bare sådan markedet
fungerer: konkurrencen om nye kunder er hård, og de bedste priser går til dem, der skifter.</p>

<h2>Trin for trin</h2>

<ol class="trin">
<li><strong>Find dit nuværende forbrug og din binding</strong>
Log ind hos dit nuværende selskab og notér tre ting: dit dataforbrug de seneste tre
måneder, om du har binding, og om der er restgæld på en telefon købt på afbetaling.</li>
<li><strong>Vælg det nye abonnement</strong>
Sammenlign på pris pr. GB, ikke kun på månedspris, og tjek dækningen på din adresse, hvis
du skifter til et andet netværk.</li>
<li><strong>Bestil og oplys dit nummer</strong>
Under bestillingen vælger du, at du vil beholde dit nummer, og indtaster det. Nogle
udbydere beder om dit CPR-nummer til identifikation — det er normalt.</li>
<li><strong>Vælg eSIM eller fysisk simkort</strong>
eSIM er hurtigst, hvis din telefon understøtter det. Ellers kommer et fysisk kort med
posten inden for et par hverdage.</li>
<li><strong>Afvent flytningen</strong>
Du får typisk besked om, hvornår nummeret flyttes. Hold den gamle telefon tændt indtil da.
Selve skiftet tager sjældent mere end nogle minutter.</li>
<li><strong>Tjek at alt virker</strong>
Ring et opkald, send en sms, og tjek at mobildata virker. Slå datastop til med det samme.
Har du tofaktorgodkendelse på sms til bank eller MitID, så bekræft at det stadig kommer
igennem.</li>
</ol>

<h2>De fem ting der oftest går galt</h2>

<table>
<thead><tr><th>Problem</th><th>Hvad du gør</th></tr></thead>
<tbody>
<tr><td>Restgæld på telefonen dukker op som en stor regning</td><td>Spørg om restgælden <em>før</em> du bestiller. Den følger ikke med til det nye selskab.</td></tr>
<tr><td>Du opsagde selv det gamle abonnement</td><td>Gør det ikke. Opsiger du selv, kan nummeret nå at blive lukket, før det kan flyttes.</td></tr>
<tr><td>Sms med koder fra banken kommer ikke frem</td><td>Vent til porteringen er helt gennemført, genstart telefonen, og kontakt derefter udbyderen.</td></tr>
<tr><td>eSIM aktiveres ikke</td><td>Kræver ofte wi-fi og en telefon, der ikke er simlåst. Genstart, og prøv igen.</td></tr>
<tr><td>Voicemail og indstillinger er væk</td><td>Nogle indstillinger følger ikke med. De sættes op igen i den nye udbyders app.</td></tr>
</tbody>
</table>

<h2>Hvornår bør du skifte?</h2>

<p>Vores anbefaling er at kigge på abonnementet en gang om året — sæt en påmindelse samme
dag hvert år. Tjek tre ting: hvad du betaler, hvad du reelt bruger, og hvad tilsvarende
abonnementer koster i dag. I langt de fleste tilfælde kan der spares penge, enten ved at
skifte selskab eller ved at flytte ned i datamængde hos det, du allerede har.</p>

</section>
"""

GUIDE_DATA = """
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort svar:</strong> De fleste danskere har brug for 15–30 GB om måneden. Bruger
du primært wi-fi hjemme og på arbejde, rækker 5–10 GB. Streamer du video på farten eller
bruger hotspot til laptop, skal du op i 50–100 GB. Under 5 procent har reelt brug for
fri data.</p>
</div>

<h2>Find dit faktiske forbrug på to minutter</h2>

<p>Alt andet end dit eget måledata er gætværk. Sådan finder du det:</p>

<ul>
<li><strong>iPhone:</strong> Indstillinger → Mobildata. Rul ned til statistik. Bemærk at
tallet kan dække en lang periode — nulstil det ved månedsskifte for et rent tal.</li>
<li><strong>Android:</strong> Indstillinger → Netværk og internet → Dataforbrug. Her kan du
se forbrug pr. måned og pr. app.</li>
<li><strong>Din udbyders app:</strong> Den mest præcise kilde, fordi den viser præcis det,
du faktisk faktureres for, opgjort pr. afregningsperiode.</li>
</ul>

<p>Kig på tre måneder, ikke én. Én måned med ferie eller sygdom giver et misvisende
billede. Tag det højeste af de tre og læg 20 procent til.</p>

<h2>Sådan oversætter du forbrug til abonnement</h2>

<table>
<thead><tr><th>Dit forbrug</th><th>Vælg</th><th>Hvorfor</th></tr></thead>
<tbody>
<tr><td>Under 4 GB</td><td>5–10 GB</td><td>Marginalprisen for at gå op er så lav, at bufferen er gratis tryghed</td></tr>
<tr><td>4–12 GB</td><td>15–20 GB</td><td>Plads til en travl måned uden at skulle tænke over det</td></tr>
<tr><td>12–25 GB</td><td>30–50 GB</td><td>Prisspringet er lille, og du undgår overforbrug helt</td></tr>
<tr><td>25–60 GB</td><td>100 GB</td><td>Her er pris pr. GB typisk lavest på hele markedet</td></tr>
<tr><td>Over 80 GB</td><td>Fri data</td><td>Nu bliver det billigere end at betale for overforbrug</td></tr>
</tbody>
</table>

<p>Mønsteret er værd at lægge mærke til: vi anbefaler næsten altid ét trin højere end dit
målte forbrug. Det skyldes prisstrukturen på det danske marked, hvor springet mellem
kategorier ofte kun er 20–30 kr., mens datamængden fordobles eller tredobles. Den ekstra
tyver køber dig fuldstændig frihed fra at tænke over sagen — og det er sjældent en dårlig
handel.</p>

<h2>Fem måder at bruge mindre data på</h2>

<ol class="trin">
<li><strong>Slå automatisk videoafspilning fra</strong>
I sociale medier afspilles video automatisk, mens du scroller. Det er den enkeltstørste
skjulte dataforbruger på de fleste telefoner.</li>
<li><strong>Hent musik og podcasts på wi-fi</strong>
Offline-download koster nul data på farten. Sæt det op til automatisk download om natten.</li>
<li><strong>Begræns streaming til standardkvalitet på mobil</strong>
Forskellen mellem HD og standard på en telefonskærm er lille. Dataforbruget er tre gange
så stort.</li>
<li><strong>Slå baggrundsopdatering fra for apps du sjældent bruger</strong>
Mange apps henter data i baggrunden hele dagen uden at give dig noget.</li>
<li><strong>Hent kort til offline brug</strong>
Kortapps kan gemme hele områder lokalt. Praktisk på rejser og gratis i data.</li>
</ol>

</section>
"""


# ============================================================================
#  OM-SIDER — E-E-A-T
# ============================================================================

OM_OS = """
<section class="sektion baand-smal artikel">

<h2>Hvorfor Telemobil findes</h2>

<p>Det danske mobilmarked har omkring tredive selskaber og flere hundrede abonnementer.
De sælger stort set det samme — data, tale og sms på et af tre netværk — til priser, der
varierer med flere hundrede procent. Det er ikke et marked, der er svært at gennemskue,
fordi produktet er kompliceret. Det er svært at gennemskue, fordi det er indrettet sådan.</p>

<p>Telemobil er bygget for at gøre det simpelt igen. Vi samler priserne, regner dem om til
tal, der kan sammenlignes, og skriver ærligt om, hvad forskellene reelt betyder. Vi tror
på, at en god sammenligningsside skal kunne fortælle dig, at du ikke behøver det dyre
produkt — også når vi tjener mere på det dyre.</p>

<h2>Sådan arbejder vi</h2>

<ul>
<li><strong>Vi henter priser fra kilden.</strong> Alle priser stammer fra udbydernes egne
offentlige prislister og kontrolleres manuelt ved hver opdatering.</li>
<li><strong>Vi sorterer efter pris — altid.</strong> Provision påvirker ikke rækkefølgen.
Ingen udbyder kan købe sig til en placering eller en anbefaling.</li>
<li><strong>Vi skriver også ulemperne.</strong> Hver udbyderomtale indeholder en liste over,
hvad der taler imod. Findes der ingen ulemper, har vi ikke kigget godt nok efter.</li>
<li><strong>Vi daterer alt.</strong> Priser ændrer sig. Derfor står opdateringsdatoen
øverst på hver side, så du selv kan vurdere, hvor friske tallene er.</li>
<li><strong>Vi retter fejl offentligt.</strong> Finder du en forkert pris eller oplysning,
retter vi den og noterer datoen.</li>
</ul>

<h2>Det vi ikke gør</h2>

<p>Vi laver ikke egne hastighedsmålinger, og vi udgiver ikke dækningskort. Netværksejerne
og de uafhængige måleinstitutter har adgang til datamængder, vi ikke kan matche, og vi
mener, det ville være uredeligt at foregive andet. Hvor dækning og hastighed er relevant,
henviser vi til dem.</p>

<p>Vi sælger heller ikke dine oplysninger, og vi kræver ikke, at du opretter en bruger for
at se priser. Der er ingen formular mellem dig og tallene.</p>

<h2>Kontakt og rettelser</h2>

<p>Har du fundet en fejl, mangler du en udbyder i sammenligningen, eller vil du bare stille
et spørgsmål, kan du skrive til os via <a href="/kontakt/">kontaktsiden</a>. Vi svarer på
alle henvendelser om faktuelle fejl.</p>

</section>
"""

TJENER_PENGE = """
<section class="sektion baand-smal artikel">

<div class="udtag">
<p><strong>Kort fortalt:</strong> Telemobil er gratis for dig at bruge. Vi tjener penge på
provision fra udvalgte udbydere, når du klikker videre og bestiller. Det koster dig ikke
mere, og det påvirker ikke, hvordan vi sorterer eller vurderer abonnementer.</p>
</div>

<h2>Hvordan provisionen fungerer</h2>

<p>Når du klikker på et link til en udbyder på Telemobil, registreres det, at du kom fra
os. Bestiller du et abonnement, modtager vi et beløb fra udbyderen. Beløbet betales af
udbyderen som en del af deres markedsføringsbudget — det lægges ikke oven i din pris, og
du betaler nøjagtig det samme, som hvis du var gået direkte til deres hjemmeside.</p>

<h2>Hvad provisionen ikke påvirker</h2>

<ul>
<li><strong>Rækkefølgen i tabellerne.</strong> Alle sammenligningstabeller sorteres efter
laveste pris. Sorteringen beregnes ud fra data, ikke ud fra hvad vi tjener.</li>
<li><strong>Hvem der er med.</strong> Vi medtager også udbydere, vi ikke har en
provisionsaftale med, når de er relevante for dig. De er markeret på samme måde som alle
andre, og deres links er almindelige links uden sporing.</li>
<li><strong>Hvad vi skriver.</strong> Ulemper står i vores omtaler, uanset om vi tjener på
udbyderen. En udbyder kan ikke få en kritisk formulering fjernet.</li>
</ul>

<h2>Hvorfor vi fortæller det så tydeligt</h2>

<p>Efter markedsføringsloven skal kommerciel påvirkning fremgå klart. Vi mener desuden, at
det er en forudsætning for, at du kan bruge siden fornuftigt: du skal vide, hvad vores
interesse er, så du selv kan vurdere vores anbefalinger. Derfor står afsløringen både
øverst på sammenligningssiderne, ved hver tabel og i bunden af alle sider — ikke gemt på
en underside, ingen finder.</p>

<h2>Vores interessekonflikt, sagt ligeud</h2>

<p>Der findes én reel interessekonflikt, og vi vil hellere skrive den frem end lade som om,
den ikke findes: vi tjener typisk mere på dyre abonnementer end på billige. Vores svar på
det er metoden — sortering efter pris, faste kriterier og en redaktionel linje, hvor vi
konsekvent skriver, at de fleste danskere ikke har brug for fri data. Du er velkommen til
at holde os op på det.</p>

</section>
"""

METODE = """
<section class="sektion baand-smal artikel">

<h2>Datagrundlag</h2>

<p>Vores priser stammer fra udbydernes egne offentligt tilgængelige prislister. Hver
opdatering kontrolleres manuelt mod udbyderens produktside, og opdateringsdatoen fremgår
øverst på hver side.</p>

<p>Hvor en udbyder markedsfører en tidsbegrænset kampagnepris, viser vi både kampagneprisen
og normalprisen, når begge er oplyst. Er kampagneperioden kortere end tolv måneder,
regner vi med normalprisen i vores sammenligninger, fordi det er den pris, du kommer til at
betale i det meste af året.</p>

<h2>Beregninger</h2>

<ul>
<li><strong>Pris pr. GB</strong> = månedspris divideret med inkluderet datamængde.
Abonnementer med fri data indgår ikke, da tallet ikke er meningsfuldt.</li>
<li><strong>Årsomkostning</strong> = tolv måneders pris plus eventuelt oprettelsesgebyr,
inklusive prisstigning efter kampagneperiode.</li>
<li><strong>Datamængde</strong> opgøres som den mængde, der kan bruges i Danmark. EU-loft
angives særskilt, hvor det afviger.</li>
</ul>

<h2>Vurderingskriterier</h2>

<table>
<thead><tr><th>Kriterium</th><th>Vægt</th><th>Hvordan vi vurderer</th></tr></thead>
<tbody>
<tr><td>Pris</td><td>Høj</td><td>Månedspris og pris pr. GB sammenlignet med markedet</td></tr>
<tr><td>Vilkår</td><td>Høj</td><td>Binding, oprettelse, opsigelsesvarsel, prisgaranti</td></tr>
<tr><td>Netværk</td><td>Middel</td><td>Hvilket net udbyderen kører på og eventuelle begrænsninger</td></tr>
<tr><td>Gennemsigtighed</td><td>Middel</td><td>Hvor let det er at finde de faktiske vilkår</td></tr>
<tr><td>Kundeservice</td><td>Lav</td><td>Kanaler og tilgængelighed, ikke egne målinger</td></tr>
</tbody>
</table>

<h2>Uafhængighed</h2>

<p>Udbydere har ingen indflydelse på vores indhold og ser det ikke før udgivelse.
Provisionsaftaler påvirker hverken sortering, vurdering eller ordvalg. Læs mere om
<a href="/saadan-tjener-vi-penge/">vores forretningsmodel</a>.</p>

<h2>Rettelser</h2>

<p>Vi retter faktuelle fejl hurtigst muligt og noterer datoen for rettelsen. Har du fundet
en fejl, så <a href="/kontakt/">skriv til os</a>.</p>

</section>
"""
