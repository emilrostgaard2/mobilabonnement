# -*- coding: utf-8 -*-
"""Indhold til fire nye guides: simkort, fejlfinding, forbrugskontrol og køb af telefon."""


def simkort(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Der findes tre fysiske simkortstørrelser — standard, micro og
nano — plus eSIM, som er digitalt. Alle nyere telefoner bruger nano eller eSIM. Får du et
kort i den forkerte størrelse, kan du som regel brække det ud af rammen, fordi kortene
leveres i en form, hvor alle tre størrelser sidder i hinanden.</p>
</div>

<h2>De fire typer</h2>

<table>
<thead><tr><th>Type</th><th>Størrelse</th><th>Bruges i</th><th>Kan skiftes fysisk?</th></tr></thead>
<tbody>
<tr><td><strong>Standard (mini)</strong></td><td>25 × 15 mm</td><td>Telefoner fra før ca. 2010</td><td>Ja</td></tr>
<tr><td><strong>Micro</strong></td><td>15 × 12 mm</td><td>Telefoner ca. 2010–2014</td><td>Ja</td></tr>
<tr><td><strong>Nano</strong></td><td>12,3 × 8,8 mm</td><td>Stort set alle nyere telefoner</td><td>Ja</td></tr>
<tr><td><strong>eSIM</strong></td><td>Indbygget chip</td><td>Nyere telefoner og ure</td><td>Nej — aktiveres digitalt</td></tr>
</tbody>
</table>

<p>Bestiller du et nyt simkort i dag, får du næsten altid et kombikort, hvor nano sidder
inde i micro, som sidder inde i standard. Du brækker bare den størrelse ud, du har brug for.
Har du brækket forkert, kan du sætte den lille del tilbage i rammen — men det sidder løst, og
mange telefoner får kontaktproblemer af det.</p>

<div class="tip">
<h3>Er du i tvivl om størrelsen?</h3>
<p>Kig i telefonens manual eller søg på modelnavnet plus "simkort størrelse". Er telefonen
købt efter 2015, er svaret nano med meget stor sandsynlighed. Understøtter den eSIM, er det
næsten altid den nemmeste vej — du er i gang på få minutter uden at vente på posten.
<a href="/guides/esim/">Se hvordan eSIM virker</a>.</p>
</div>

<h2>Sådan skifter du simkort</h2>

<ol class="trin">
<li><strong>Sluk telefonen</strong>
Ikke strengt nødvendigt på moderne telefoner, men det undgår fejl i netværksregistreringen.</li>
<li><strong>Find simbakken</strong>
På de fleste telefoner sidder den i siden og åbnes med den lille nål, der fulgte med. En
udrettet papirclips virker lige så godt.</li>
<li><strong>Læg kortet i med hjørnet rigtigt</strong>
Kortet har et afskåret hjørne, der passer med bakken. Det kan kun ligge én vej.</li>
<li><strong>Tænd og indtast PIN</strong>
Koden fulgte med kortet. Har du glemt den, skal du bruge PUK — se
<a href="/pin-og-puk-kode/">vores guide</a>.</li>
<li><strong>Tjek at der er signal</strong>
Kommer der ikke signal inden for et par minutter, så genstart. Hjælper det ikke, kan
APN-indstillingerne mangle — se afsnittet nedenfor.</li>
</ol>

<h2>Hvis der ikke kommer signal</h2>

<p>Det skyldes næsten altid én af fire ting, og de er alle lette at udelukke:</p>

<ul>
<li><strong>Kortet er ikke aktiveret endnu.</strong> Nye kort aktiveres af udbyderen, ofte
med nogle timers forsinkelse. Tjek beskeden fra udbyderen.</li>
<li><strong>Telefonen er simlåst.</strong> Købt hos et selskab med binding kan telefonen
være låst til det selskab. Udbyderen kan låse den op.</li>
<li><strong>APN mangler.</strong> Indstillingen der forbinder telefonen til udbyderens
datanet. Opkald virker, men data gør ikke. Findes på udbyderens hjemmeside.</li>
<li><strong>Kortet sidder skævt.</strong> Særligt hvis du har brækket et kombikort ud og sat
det tilbage. Tag det ud og i igen.</li>
</ul>

<h2>Skal du bestille et nyt simkort?</h2>

<p>Du har brug for et nyt kort i tre situationer: du skifter udbyder, du har mistet
telefonen, eller kortet er fysisk beskadiget. Ved udbyderskifte følger kortet automatisk med
bestillingen — du skal ikke bestille særskilt.</p>

<p>Er kortet væk eller stjålet, så spær det med det samme hos udbyderen. Et simkort i en
fremmed telefon kan modtage dine sms'er, herunder koder fra bank og MitID. Det er den
egentlige risiko, ikke taletiden.</p>

<h2>Ekstra simkort til samme abonnement</h2>

<p>Flere udbydere sælger et ekstra kort, der deler abonnementets data med et ur, en tablet
eller en bil. Tjek to ting: om det deler datapuljen eller har sin egen, og om der er et
månedligt gebyr. Deler det puljen, er det samme datamængde, der nu skal dække flere
enheder.</p>

<p>Se hvordan det spiller ind i en husstand på vores side om
<a href="/mobilabonnement-til-familie/">mobilabonnement til familien</a>.</p>
</section>
"""


def fejlfinding(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Virker mobilen ikke, så tag de fem ting i rækkefølge:
genstart telefonen, slå flytilstand til og fra, tjek om andre i nærheden har samme problem,
tjek din datamængde, og slå wi-fi-opkald til. Fire ud af fem problemer løses af de to
første.</p>
</div>

<h2>Start her — uanset problemet</h2>

<ol class="trin">
<li><strong>Genstart telefonen</strong>
Det lyder banalt, men det løser flest problemer. Telefonens forbindelse til nettet kan
hænge fast i en fejltilstand, som kun en genstart rydder op i.</li>
<li><strong>Slå flytilstand til og fra</strong>
Tvinger telefonen til at registrere sig på nettet igen. Tag ti sekunder imellem.</li>
<li><strong>Tjek om det kun er dig</strong>
Har andre i husstanden samme udbyder og samme problem, er det nettet. Har de det ikke, er
det din telefon eller dit abonnement.</li>
<li><strong>Tjek datamængden</strong>
Mange udbydere sætter hastigheden drastisk ned frem for at stoppe forbindelsen. Er alt
pludselig meget langsomt sidst på måneden, er det typisk forklaringen.</li>
<li><strong>Test forbindelsen</strong>
Mål hastigheden, så du ved, om det er langsomt eller helt væk. Det er to forskellige
problemer. <a href="/speedtest/">Test din hastighed</a>.</li>
</ol>

<h2>Ingen dækning</h2>

<p>Er der slet intet signal, så tjek først om telefonen er registreret på nettet: står der
"Ingen service" eller "Søger", er det forbindelsen. Står der et udbydernavn, men intet
virker, er det abonnementet.</p>

<table>
<thead><tr><th>Symptom</th><th>Sandsynlig årsag</th><th>Løsning</th></tr></thead>
<tbody>
<tr><td>Ingen service overalt</td><td>Simkort eller registrering</td><td>Genstart, tjek kortet sidder rigtigt</td></tr>
<tr><td>Ingen service ét sted</td><td>Dækningshul</td><td>Tjek nettets dækningskort på adressen</td></tr>
<tr><td>Dårligt signal indendørs</td><td>Bygningens mure</td><td>Slå wi-fi-opkald til</td></tr>
<tr><td>Signal men ingen data</td><td>APN-indstilling eller datastop</td><td>Tjek APN og om datastop er aktivt</td></tr>
<tr><td>Langsomt sidst på måneden</td><td>Datamængden er brugt</td><td>Køb ekstra eller gå op i pakke</td></tr>
</tbody>
</table>

<div class="tip">
<h3>Wi-fi-opkald løser de fleste indendørsproblemer</h3>
<p>Telefonen fører opkaldet over dit hjemmenet i stedet for mobilnettet, og samtalen bliver
typisk bedre end på et svagt signal. Slås til i telefonens indstillinger under opkald.
De fleste danske udbydere understøtter det uden ekstra betaling.</p>
</div>

<h2>Langsom forbindelse</h2>

<p>Hastighed svinger af flere grunde, og de fleste har intet med din udbyder at gøre:
afstand til masten, hvor mange der er på nettet samtidig, bygningens materialer og din
telefons modem.</p>

<p>Før du klager, så mål hastigheden tre gange på forskellige tidspunkter. Én måling siger
ikke meget. Ligger du konsekvent under 3 Mbit på et sted med god dækning ifølge kortet, er
der noget galt — så er det værd at kontakte udbyderen med tallene i hånden.</p>

<p>Husk også, at du sjældent har brug for meget. 5-10 Mbit rækker til video i HD, og 2 Mbit
til almindelig browsing. <a href="/speedtest/">Se hvad dine tal betyder</a>.</p>

<h2>Kan ikke ringe eller sende sms</h2>

<ul>
<li><strong>Tjek om nummeret er spærret</strong> i telefonens blokeringsliste.</li>
<li><strong>Tjek om abonnementet er spærret</strong> — ubetalte regninger kan udløse
spærring for udgående trafik, mens indgående stadig virker.</li>
<li><strong>Prøv med og uden landekode.</strong> Nogle numre kræver +45 foran.
<a href="/landekoder/">Se alle landekoder</a>.</li>
<li><strong>Tjek at der ikke er spærret for overtakserede numre</strong>, hvis det er et
servicenummer, du forsøger at ringe til.</li>
</ul>

<h2>Problemer i udlandet</h2>

<p>Virker telefonen ikke på rejsen, er årsagen næsten altid, at dataroaming er slået fra —
hvilket ofte er en indstilling, man selv har lavet med god grund. Slå den til, mens du er i
EU, hvor det er dækket af dit abonnement.</p>

<p>Uden for EU bør du derimod lade den være slået fra, medmindre du kender taksten. Se
<a href="/guides/mobilabonnement-i-udlandet/">vores guide til mobil i udlandet</a>.</p>

<h2>Hvornår skal du kontakte udbyderen?</h2>

<p>Når du har udelukket telefonen. Det har du, hvis: et andet simkort virker i din telefon,
eller dit simkort virker i en anden telefon. Den test tager fem minutter og afgør, om det er
hardware eller abonnement.</p>

<p>Ring med konkrete oplysninger: hvornår problemet startede, om det er ét sted eller
overalt, hvad hastighedsmålingen viser, og hvad du allerede har prøvet. Det halverer
samtalen.</p>

<p>Får du ikke løst problemet, kan du klage skriftligt og derefter til Teleankenævnet. Se
<a href="/guides/prisstigning-mobilabonnement/">dine rettigheder</a>.</p>
</section>
"""


def forbrugskontrol(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Slå datastop til. Det er den ene indstilling, der forhindrer,
at din udbyder køber ekstra data på dine vegne, når pakken er brugt op. Den er gratis, tager
under et minut, og den findes hos stort set alle udbydere. Bed derudover om spærring for
overtakserede numre.</p>
</div>

<h2>De tre spærringer alle bør have</h2>

<table>
<thead><tr><th>Spærring</th><th>Beskytter mod</th><th>Koster</th><th>Ulempe</th></tr></thead>
<tbody>
<tr><td><strong>Datastop</strong></td><td>Automatisk køb af ekstra data</td><td>Gratis</td><td>Du står uden data resten af måneden</td></tr>
<tr><td><strong>Overtakserede numre</strong></td><td>Dyre service- og sms-tjenester</td><td>Gratis</td><td>Du kan ikke bruge dem, hvis du vil</td></tr>
<tr><td><strong>Udgående udlandsopkald</strong></td><td>Svindelopkald og tilbagekald</td><td>Gratis</td><td>Du kan ikke selv ringe til udlandet</td></tr>
</tbody>
</table>

<p>De to første bør stå til på ethvert abonnement. Den tredje er relevant, hvis du aldrig
ringer til udlandet — så lukker den den vej, hvor de dyreste svindelregninger opstår. Se
<a href="/hvem-ringer-til-mig/">hvordan svindelopkald fungerer</a>.</p>

<h2>Hvad sker der, når datamængden er brugt?</h2>

<p>Der findes tre modeller, og forskellen er stor for din regning:</p>

<ul>
<li><strong>Nedsat hastighed.</strong> Forbindelsen fortsætter, men langsomt. Ingen ekstra
regning. Beskeder og kort virker, video gør ikke.</li>
<li><strong>Automatisk køb.</strong> Udbyderen køber ekstra datapakker på dine vegne. Det er
her, de store overraskelsesregninger opstår.</li>
<li><strong>Fuld spærring.</strong> Data stopper indtil næste periode. Kan ikke koste
ekstra.</li>
</ul>

<p>Datastop gør spørgsmålet irrelevant, fordi forbindelsen aldrig kan udløse et køb. Det er
derfor, vi anbefaler det uanset udbyder — også hvis du er sikker på, at din udbyder
throttler frem for at købe.</p>

<div class="advarsel">
<p><strong>Automatisk optankning på taletid er den skjulte version.</strong> Slår du den til
på et barns telefon, har du reelt lavet et abonnement uden loft — og fjernet hele pointen
med taletid. <a href="/taletidskort/">Læs mere om taletid</a>.</p>
</div>

<h2>Sådan finder du dit faktiske forbrug</h2>

<ol class="trin">
<li><strong>Åbn udbyderens app</strong>
Der står forbruget for indeværende periode og typisk også de foregående måneder.</li>
<li><strong>Kig på tre måneder, ikke én</strong>
En enkelt måned kan være atypisk — en ferie, en flytning, en periode uden wi-fi.</li>
<li><strong>Tag den højeste, ikke gennemsnittet</strong>
Du skal kunne klare din værste måned uden at købe ekstra.</li>
<li><strong>Læg 20 % til</strong>
Forbruget stiger over tid, fordi apps og indhold bliver tungere.</li>
</ol>

<p>Telefonen har også sin egen tæller under indstillinger, men den nulstilles ikke
nødvendigvis samtidig med din regningsperiode. Udbyderens app er den præcise kilde. Se
<a href="/guides/hvor-meget-data/">hele guiden til dataforbrug</a>.</p>

<h2>Hvad koster det at løbe tør?</h2>

<p>Ekstra datapakker er dyre målt pr. gigabyte sammenlignet med at have den rigtige pakke
fra start. Køber du ekstra tre måneder i træk, har du typisk betalt mere, end et abonnement
et trin højere ville have kostet hele året.</p>

<p>Det er hovedgrunden til, at vi anbefaler ét trin over dit målte forbrug: springet mellem
kategorierne er 20-40 kr. om måneden, mens prisen for at ramme forkert er langt højere.</p>

<h2>Tjek regningen én gang om året</h2>

<p>Sæt en fast dato i kalenderen. Kig efter tre ting: er der poster, du ikke kan forklare,
er en intropris udløbet uden at du opdagede det, og betaler du for tillægsydelser, du ikke
bruger?</p>

<p>Med {D['antal_uden_binding']} ud af {D['antal']} abonnementer uden binding i vores
sammenligning kan du reagere med det samme, hvis svaret ikke er tilfredsstillende.
<a href="/billigste-mobilabonnement/">Se hvad markedet koster i dag</a>.</p>

<h2>Til børn og unge</h2>

<p>Datastop er ikke til diskussion her. Den hyppigste chokregning i danske husstande opstår,
når et barn bruger telefonen som hotspot til en tablet i en ferie, og abonnementet køber
data automatisk uden loft.</p>

<p>Overvej også taletid, hvor forbruget er synligt og ikke kan overskrides. Se
<a href="/mobilabonnement-til-boern/">mobilabonnement til børn</a>.</p>
</section>
"""


def koeb_telefon(D, t):
    return f"""
<section class="sektion baand-smal artikel">
{t['gennemgang']}

<div class="udtag">
<p><strong>Kort svar:</strong> Køb telefonen kontant eller brugt, og abonnementet separat.
Et samlet tilbud binder dig typisk i 24-36 måneder, og restgælden skal indfries, hvis du vil
skifte. Regner du hele perioden igennem, er kontantkøb plus et discountabonnement næsten
altid billigere.</p>
</div>

<h2>Ny, brugt eller renoveret?</h2>

<table>
<thead><tr><th></th><th>Ny</th><th>Renoveret</th><th>Brugt privat</th></tr></thead>
<tbody>
<tr><td><strong>Pris</strong></td><td>Fuld</td><td>30-50 % under ny</td><td>Lavest</td></tr>
<tr><td><strong>Reklamationsret</strong></td><td>2 år</td><td>Typisk 1-2 år</td><td>Ingen</td></tr>
<tr><td><strong>Batteritilstand</strong></td><td>100 %</td><td>Oplyses ofte</td><td>Ukendt</td></tr>
<tr><td><strong>Risiko</strong></td><td>Ingen</td><td>Lav</td><td>Størst</td></tr>
<tr><td><strong>Bedst til</strong></td><td>Nyeste funktioner</td><td>De fleste</td><td>Den prisbevidste</td></tr>
</tbody>
</table>

<p>Renoveret er for de fleste det bedste kompromis. Du sparer typisk en tredjedel til
halvdelen, du får reklamationsret, og batteritilstanden er oplyst. Forskellen i
hverdagsbrug mellem en topmodel fra i år og en fra for tre år siden er lille.</p>

<h2>Det du skal tjekke ved brugt køb</h2>

<ol class="trin">
<li><strong>Er telefonen simlåst?</strong>
En låst telefon virker kun med ét selskabs simkort. Bed sælger bekræfte, at den er åben —
eller test med dit eget kort inden køb.</li>
<li><strong>Er den meldt stjålet?</strong>
Bed om IMEI-nummeret og tjek det, før du betaler. Er telefonen spærret, kan den ikke bruges
på noget net i Danmark.</li>
<li><strong>Er kontoen logget ud?</strong>
En iPhone med aktiv Find min iPhone eller en Android med aktiv Google-konto kan ikke
nulstilles. Den er reelt en mursten. Tjek det, før pengene skifter hænder.</li>
<li><strong>Hvad er batteritilstanden?</strong>
Under 80 % betyder, at et batteriskift snart er nødvendigt. Læg prisen på det oveni.</li>
<li><strong>Understøtter den eSIM?</strong>
Vil du undgå at vente på et fysisk kort, er det værd at tjekke.
<a href="/guides/esim/">Se hvad eSIM kræver</a>.</li>
</ol>

<div class="advarsel">
<p><strong>Køber du af en privatperson, har du ingen reklamationsret.</strong> Går telefonen
i stykker en uge efter, er det dit problem. Handler du hos en forhandler — også af
renoverede telefoner — har du de almindelige forbrugerrettigheder.</p>
</div>

<h2>Regnestykket mod afbetaling</h2>

<p>Sådan finder du ud af, om et samlet tilbud kan betale sig:</p>

<ol class="trin">
<li><strong>Gang den samlede månedspris med bindingsperioden</strong>
399 kr. i 24 måneder er 9.576 kr.</li>
<li><strong>Læg udbetaling og oprettelse til</strong></li>
<li><strong>Find telefonens kontantpris</strong>
Brug den laveste reelle pris hos en forhandler, du ville handle hos.</li>
<li><strong>Læg et discountabonnement til, ganget med samme antal måneder</strong>
89 kr. i 24 måneder er 2.136 kr.</li>
<li><strong>Sammenlign de to totaler</strong>
Forskellen er prisen for bekvemmeligheden.</li>
</ol>

<p>I et typisk eksempel er forskellen omkring 2.000 kr. — og i den frie løsning kan du
desuden skifte abonnement undervejs, hvis priserne falder. Se hele gennemgangen på
<a href="/mobilabonnement-med-telefon/">telefon på afbetaling</a>.</p>

<h2>Hvornår giver afbetaling alligevel mening?</h2>

<ul>
<li><strong>Du kan ikke lægge pengene ud.</strong> Skal du bruge en telefon nu, er
afbetaling en reel finansieringsform. Sammenlign den effektive rente med et almindeligt
forbrugslån.</li>
<li><strong>Der er en ægte hardwarerabat.</strong> Sælges telefonen markant under
kontantpris som del af pakken, kan totalen falde ud til pakkens fordel. Regnestykket
ovenfor afslører det på fem minutter.</li>
</ul>

<h2>Forsikring — tjek om du er dækket i forvejen</h2>

<p>Mobilforsikring sælges ofte med i pakken. Før du siger ja, så tjek tre ting:
selvrisikoen ved skade, om tyveri overhovedet er dækket, og om du allerede er dækket
gennem din indboforsikring. Mange er dækket i forvejen uden at vide det og betaler dobbelt.</p>

<h2>Når telefonen er købt</h2>

<p>Så mangler du kun abonnementet — og der har du fri hånd, netop fordi du ikke er bundet.
Find dit dataforbrug først, og vælg derefter.</p>

<p>Se <a href="/billigste-mobilabonnement/">billigste mobilabonnement</a>,
<a href="/mobilabonnement-uden-binding/">abonnementer uden binding</a> eller
<a href="/mobilabonnement-under-100-kr/">abonnementer under 100 kr.</a></p>
</section>
"""
