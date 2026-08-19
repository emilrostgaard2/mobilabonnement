# -*- coding: utf-8 -*-
"""Unikt indhold pr. udbyder, så udbydersiderne ikke bliver skabelontekst med
udskiftet navn. Hver udbyder har egne H2'er, egne vinkler og egne afsnit.
"""

UNIK = {
    "cbb-mobil": {
        "h2_vurdering": "CBB Mobil i praksis: hvad du får for prisen",
        "h2_net": "Telenors net — det du reelt køber hos CBB",
        "h2_hvem": "Er CBB Mobil det rigtige valg for dig?",
        "h2_sammenlign": "CBB Mobil mod de andre discountselskaber",
        "h2_skift": "Fra dit nuværende selskab til CBB Mobil",
        "net_note": ("CBB Mobil er ejet af Telenor og kører på Telenors eget net. Det er "
                     "en anden situation end de fleste discountselskaber, fordi der ikke er "
                     "tale om en lejeaftale mellem to uafhængige parter, men om et prisbrand "
                     "inden for samme koncern. I praksis betyder det, at CBB-kunder ikke "
                     "risikerer at blive nedprioriteret til fordel for moderselskabets kunder "
                     "på samme måde, som man teoretisk kan hos en ekstern MVNO."),
        "skift_note": ("CBB kræver ikke, at du opsiger noget selv. Har du i forvejen Telenor, "
                       "er skiftet internt i koncernen, men det er stadig et almindeligt "
                       "selskabsskifte med nummerportering — du får ikke automatisk overført "
                       "dine indstillinger eller din historik."),
        "sektioner": [
            ("Prisstabilitet: CBB's stærkeste kort",
             "<p>Det, der gør CBB interessant i en kategori fuld af discountselskaber, er "
             "ikke den laveste pris. Det er, at prisen holder. Store dele af markedet kører "
             "på kampagnepriser, der gælder tre eller seks måneder, hvorefter de stiger "
             "markant. CBB har historisk holdt sig fra den model.</p>"
             "<p>Forskellen er større, end den lyder. Et abonnement til 39 kr. i seks "
             "måneder og 99 kr. derefter koster i gennemsnit 69 kr. over et år. Et CBB-"
             "abonnement til 69 kr. hele vejen koster 69 kr. Prisen er den samme — men den "
             "ene kræver, at du husker at genforhandle, og den anden gør ikke. For de fleste "
             "danskere er det forskellen mellem at spare pengene og at tro, man sparede dem.</p>"
             "<p>Vores anbefaling er derfor, at du sammenligner CBB på normalpris mod andres "
             "normalpris, ikke mod deres kampagnepris. Gør du det, ligger CBB konkurrencedygtigt "
             "i næsten alle datakategorier.</p>"),
            ("CBB-appen og datastop",
             "<p>Appen er et reelt konkurrenceparameter i den billige ende, hvor kundeservice "
             "ellers er skåret ind til benet. Hos CBB kan du se dit forbrug løbende, skifte "
             "abonnement op og ned fra måned til måned, og slå datastop til uden at kontakte "
             "nogen.</p>"
             "<p>Datastop fortjener særlig omtale, fordi det er den enkeltindstilling, der "
             "sparer flest danskere for flest penge. Uden datastop kan overforbrug løbe op på "
             "en enkelt regning, særligt hvis telefonen bruges som hotspot til en laptop. Med "
             "datastop stopper forbindelsen, når pakken er brugt, og der kan ganske enkelt "
             "ikke komme en overraskelse.</p>"
             "<p>Muligheden for at skifte abonnement månedsvis er også værd at bruge aktivt. "
             "Opdager du, at du konsekvent bruger 8 GB af en 15 GB-pakke, tager det under et "
             "minut at flytte ned og spare pengene resten af året.</p>"),
        ],
    },
    "yousee": {
        "h2_vurdering": "YouSee vurderet: hvad premiumprisen dækker over",
        "h2_net": "TDC NET — hvorfor dækningen er YouSees hele argument",
        "h2_hvem": "Hvornår er YouSee pengene værd?",
        "h2_sammenlign": "YouSee mod billigere abonnementer på samme net",
        "h2_skift": "Sådan bliver du YouSee-kunde",
        "net_note": ("YouSee er en del af Nuuday og kører på TDC NET, som gennem en årrække "
                     "har klaret sig bedst i uafhængige målinger af dansk netkvalitet. Nettet "
                     "er det mest finmaskede i landet, og forskellen mærkes særligt i "
                     "landdistrikter, sommerhusområder, langs jernbanen og indendørs i ældre "
                     "bygninger. I byerne er forskellen til de to andre net lille."),
        "skift_note": ("YouSee har fysiske butikker, og det er den ene situation, hvor vi "
                       "anbefaler at skifte i en butik frem for online: er du utryg ved "
                       "simkort og opsætning, kan du få hjælp på stedet. Bemærk dog, at "
                       "fortrydelsesretten fungerer forskelligt ved køb i butik og online."),
        "sektioner": [
            ("Det vigtigste spørgsmål: bor du et sted, hvor nettet gør en forskel?",
             "<p>Hele argumentet for YouSee står og falder med dette. Betaler du et tillæg på "
             "80-120 kr. om måneden for landets bedste dækning, og bor du et sted, hvor alle "
             "tre net leverer fuld styrke, har du købt noget, du ikke får glæde af. Det er "
             "cirka 1.200 kr. om året for en forskel, du ikke kan mærke.</p>"
             "<p>Omvendt: bor du i et sommerhusområde, på en ø, i et tyndtbefolket område "
             "eller pendler du dagligt gennem strækninger med svingende dækning, kan de samme "
             "penge være blandt de bedst brugte i dit budget. Et abonnement, der ikke virker, "
             "når du har brug for det, er ikke billigt — det er spildt.</p>"
             "<p>Den eneste måde at afgøre det på er at tjekke dækningskortene for alle tre "
             "net på din faktiske adresse, din arbejdsplads og din rute imellem. Det tager to "
             "minutter. Er alle tre grønne, så vælg efter pris.</p>"),
            ("Prisregulering: tjek din regning en gang om året",
             "<p>Der er et mønster hos de store danske selskaber, som er værd at kende: "
             "eksisterende kunder betaler over tid mere end nye kunder for det samme produkt. "
             "Det sker gennem løbende prisreguleringer, som varsles korrekt, men som de "
             "færreste reagerer på.</p>"
             "<p>Har du haft samme YouSee-abonnement i tre år uden at kigge på det, er der god "
             "sandsynlighed for, at du betaler mere end den pris, YouSee tilbyder nye kunder i "
             "dag. Det er ikke ulovligt og ikke usædvanligt — det er sådan markedet fungerer, "
             "og det gælder også de andre store selskaber.</p>"
             "<p>Løsningen er enkel og tager ti minutter: find din nuværende månedspris, slå "
             "op hvad det tilsvarende abonnement koster for nye kunder, og ring hvis der er "
             "forskel. Sæt en påmindelse i kalenderen samme dato hvert år.</p>"),
        ],
    },
    "telmore": {
        "h2_vurdering": "Telmore vurderet: et abonnement du skal regne på",
        "h2_net": "Telmore kører på TDC NET",
        "h2_hvem": "Hvem får noget ud af Telmore Play?",
        "h2_sammenlign": "Telmore mod et billigt abonnement plus egne streamingtjenester",
        "h2_skift": "Sådan skifter du til Telmore",
        "net_note": ("Telmore er som YouSee en del af Nuuday og kører på TDC NET. Dækningen "
                     "er derfor identisk med YouSees — det er præcis det samme net og de "
                     "samme master. Vælger du mellem Telmore og YouSee, vælger du altså ikke "
                     "mellem to netværk, men mellem to produktpakker og to kundeserviceoplevelser."),
        "skift_note": ("Har du streamingtjenester, du beholder ved siden af, så opsig dem "
                       "først når Telmore-abonnementet er aktivt og du har bekræftet, at "
                       "tjenesten faktisk indgår. Ellers risikerer du at stå uden midt i en serie."),
        "sektioner": [
            ("Regnestykket der afgør, om Telmore er billigt eller dyrt",
             "<p>Telmore kan ikke prissammenlignes direkte med andre mobilabonnementer, og "
             "det er både selskabets styrke og den mest almindelige kilde til fejlkøb. Et "
             "abonnement til 199 kr. lyder dyrt ved siden af et discountabonnement til 89 kr. "
             "— men det er ikke den relevante sammenligning.</p>"
             "<p>Den relevante sammenligning er: hvad betaler du i dag for et billigt "
             "mobilabonnement <em>plus</em> de streamingtjenester, du faktisk bruger? Betaler "
             "du 89 kr. for mobilen og 130 kr. for to tjenester, er din reelle udgift 219 kr. "
             "Og så er Telmore til 199 kr. pludselig en besparelse.</p>"
             "<p>Vender du regnestykket om og kun bruger én af de inkluderede tjenester, "
             "betaler du markant over. Det er derfor, vi anbefaler at lave udregningen på "
             "papir før bestilling — ikke efter. Tag kun de tjenester med, du reelt ser, og "
             "husk at trække fra, hvis du deler et abonnement med din husstand i forvejen.</p>"),
            ("Pakkens indhold kan ændre sig — sæt en påmindelse",
             "<p>Streamingpakker bygger på aftaler mellem udbyderen og indholdsleverandørerne, "
             "og de aftaler udløber. En tjeneste, der var hele grunden til, at du valgte "
             "abonnementet, kan forsvinde ud af pakken, og prisen falder ikke nødvendigvis "
             "tilsvarende.</p>"
             "<p>Det er ikke unikt for Telmore — det gælder alle streamingbundles på markedet "
             "— men det er en reel risiko, som sjældent nævnes i markedsføringen. Læs "
             "vilkårene for, hvad der sker med prisen, hvis en tjeneste fjernes, og hvilket "
             "varsel du har krav på.</p>"
             "<p>Praktisk råd: sæt en kalenderpåmindelse en gang om året, hvor du tjekker "
             "hvad der stadig indgår, og laver regnestykket forfra. Et abonnement, der var "
             "det rigtige valg for to år siden, er ikke nødvendigvis det i dag.</p>"),
        ],
    },
    "oister": {
        "h2_vurdering": "Oister vurderet: mange gigabyte, ét forbehold",
        "h2_net": "3's net — stærkt i byen, svagere på landet",
        "h2_hvem": "Passer Oister til din adresse?",
        "h2_sammenlign": "Oister mod de øvrige storforbrugerabonnementer",
        "h2_skift": "Sådan kommer du i gang hos Oister",
        "net_note": ("Oister er ejet af Hi3G og kører på 3's netværk. Det net har en anden "
                     "profil end de to andre: høj kapacitet og høje hastigheder i byer og "
                     "tætbefolkede områder, tidlig 5G-udrulning, men historisk mindre "
                     "finmasket i landdistrikter, langs kysten og i visse indendørsmiljøer."),
        "skift_note": ("Fordi 3's net varierer mere geografisk end de to andre, er "
                       "fortrydelsesretten særligt relevant her. Test dækningen grundigt de "
                       "første dage — hjemme, på arbejdet, i kælderen og på din pendlerrute — "
                       "mens du stadig kan fortryde."),
        "sektioner": [
            ("Tjek dækningen før du bestiller — det er ikke en formalitet",
             "<p>Ved de fleste udbydere er dækningstjek et godt råd. Ved Oister er det "
             "afgørende, og det er den ene ting, vi vil have dig til at gøre, før du "
             "bestiller.</p>"
             "<p>3's net er bygget med en anden prioritering end TDC NET: fokus på kapacitet "
             "og hastighed der, hvor der er mange mennesker, frem for maksimal geografisk "
             "udbredelse. For en storbybruger er det ofte en fordel — du får høje hastigheder, "
             "også når mange er på nettet samtidig. For en bruger i et tyndtbefolket område "
             "kan det være en mærkbar ulempe.</p>"
             "<p>Konkret: slå dækningskortet op på din bopælsadresse, din arbejdsplads og "
             "gerne et par steder på din daglige rute. Spørg eventuelt en nabo, der allerede "
             "er på 3's net. Er billedet godt, er Oister blandt markedets stærkeste køb på "
             "data pr. krone. Er det blandet, så vælg et abonnement på et andet net, selvom "
             "det koster tredive kroner mere.</p>"),
            ("Derfor er Oister ofte billigst i den store ende",
             "<p>Der er et mønster i Oisters prissætning, som er værd at kende: selskabet er "
             "sjældent absolut billigst på de mindste pakker, men presser markedet hårdt fra "
             "omkring 20 GB og opefter. Det gør Oister til et af de mest interessante valg "
             "netop for dem, der bruger meget data.</p>"
             "<p>Regnet i pris pr. gigabyte er de store Oister-abonnementer typisk blandt de "
             "laveste på hele markedet. Bruger du 30-50 GB om måneden — altså streamer video "
             "på farten, bruger telefonen som hotspot til en laptop, eller har børn på "
             "abonnementet — er det her, du skal kigge først.</p>"
             "<p>Modsat gælder, at hvis du kun bruger 5 GB, findes der billigere veje til det "
             "hos flere af de mindre danske selskaber. Vælg efter din datakategori, ikke "
             "efter selskabets generelle ry.</p>"),
        ],
    },
    "lebara": {
        "h2_vurdering": "Lebara vurderet: én ting gør de bedre end alle andre",
        "h2_net": "Lebaras netværk i Danmark",
        "h2_hvem": "Ringer du til udlandet? Så start her",
        "h2_sammenlign": "Lebara mod andre udbydere til internationale opkald",
        "h2_skift": "Sådan skifter du til Lebara",
        "net_note": ("Lebara er en international MVNO, der lejer sig ind på et af de danske "
                     "netværk. Netværksaftaler for MVNO'er kan blive genforhandlet, og derfor "
                     "bør du tjekke den aktuelle netværksangivelse på Lebaras egen side, hvis "
                     "dækning er afgørende for dit valg."),
        "skift_note": ("Skifter du til Lebara på grund af udlandsopkald, så tjek landelisten "
                       "for netop dine numre <em>før</em> du opsiger noget. Det er den "
                       "hyppigste kilde til skuffelse: abonnementet dækker landet, men kun "
                       "fastnetnumre, mens du ringer til mobil."),
        "sektioner": [
            ("Roaming og udlandsopkald er to forskellige ting",
             "<p>Det er den vigtigste skelnen på hele Lebaras produktområde, og den bliver "
             "blandet sammen konstant — også af folk, der har haft mobilabonnement i tyve år.</p>"
             "<p><strong>Roaming</strong> er, når du selv befinder dig i udlandet og bruger dit "
             "danske abonnement. Inden for EU er det reguleret, så dit abonnement virker "
             "stort set som herhjemme, dog typisk med et loft på datamængden. Det er ikke "
             "det, Lebara er specialiseret i — det får du hos alle danske selskaber.</p>"
             "<p><strong>Opkald til udlandet</strong> er, når du sidder i Danmark og ringer til "
             "et nummer i et andet land. Det er ikke reguleret, det er ikke inkluderet i "
             "almindelig fri tale, og priserne varierer med flere hundrede procent mellem "
             "selskaberne. Det er her, Lebara er bygget, og det er her, forskellen kan løbe op "
             "i hundredvis af kroner om måneden for en familie med bånd til udlandet.</p>"),
            ("Sådan læser du landelisten rigtigt",
             "<p>To abonnementer med 1.000 udlandsminutter kan være vidt forskellige "
             "produkter. Forskellen ligger i tre detaljer, som står i vilkårene, men sjældent "
             "i annoncen.</p>"
             "<p><strong>Hvilke lande?</strong> Listen kan dække ti lande eller halvtreds. "
             "Tjek at netop dit land er med — ikke bare regionen.</p>"
             "<p><strong>Mobil eller fastnet?</strong> Mange lande prissættes forskelligt for "
             "opkald til mobilnumre og fastnetnumre, og et abonnement kan dække det ene og "
             "ikke det andet. I lande hvor familien primært bruger mobil, er fastnetdækning "
             "ikke meget værd.</p>"
             "<p><strong>Hvad koster minutter ud over de inkluderede?</strong> Overskrider du "
             "pakken, træder en minuttakst i kraft, og den kan være høj. Kig på den, før du "
             "vælger, særligt hvis dit forbrug svinger fra måned til måned.</p>"),
        ],
    },
    "greentel": {
        "h2_vurdering": "Greentel vurderet: enkelhed som produkt",
        "h2_net": "Greentel er en MVNO — hvad det betyder for din dækning",
        "h2_hvem": "Hvem passer Greentel til?",
        "h2_sammenlign": "Greentel mod de øvrige danske discountselskaber",
        "h2_skift": "Sådan skifter du til Greentel",
        "net_note": ("Greentel er en MVNO — et selskab uden eget mobilnet, der lejer kapacitet "
                     "hos en af de tre danske netværksejere. Vi angiver ikke et net her uden "
                     "at have verificeret det, fordi MVNO-aftaler bliver genforhandlet. Tjek "
                     "den aktuelle angivelse hos Greentel, hvis dækning er afgørende."),
        "skift_note": ("Hos en lille udbyder som Greentel er kundeservice digital og "
                       "begrænset. Sørg for at have adgang til din mail og dit MitID, når du "
                       "bestiller, så du kan klare oprettelsen uden at skulle vente på svar."),
        "sektioner": [
            ("Forbrugsafregning: den oversete løsning til meget lavt forbrug",
             "<p>Greentel er blandt de danske selskaber, der tilbyder forbrugsafregnede "
             "abonnementer — altså ingen fast månedspris, men betaling pr. minut og pr. sms. "
             "Det er en produkttype, de fleste sammenligningssider springer over, fordi den "
             "ikke passer ind i en pristabel med månedspriser.</p>"
             "<p>For den rigtige bruger er det dog den billigste løsning på hele markedet. "
             "Har du en telefon nummer to, en sommerhustelefon, en telefon i bilen eller et "
             "nummer, du bare vil holde i live, betaler du reelt ingenting i de måneder, hvor "
             "den ikke bruges.</p>"
             "<p>Regnestykket vender omkring 100 minutter om måneden. Derover bliver et "
             "almindeligt abonnement med fri tale billigere. Se vores gennemgang af "
             "<a href=\"/mobilabonnement-uden-data/\">abonnementer uden data</a> for den "
             "fulde udregning.</p>"),
            ("Hvad du opgiver ved at vælge en lille udbyder",
             "<p>Vi mener, det er mere nyttigt at være konkret om, hvad du <em>ikke</em> får, "
             "end at gentage at prisen er lav. Hos et lille dansk discountselskab opgiver du "
             "typisk fire ting.</p>"
             "<p>Der er ingen fysisk butik, du kan gå ind i. Kundeservice er digital og "
             "bemandet af få mennesker, så svartiden er længere end hos de store. Der følger "
             "ingen streaming, forsikring eller fordelsklub med. Og du bør selv tjekke, om "
             "MVNO-aftalen indeholder hastighedsloft eller lavere prioritet i myldretiden — "
             "det står i vilkårene, men sjældent med store bogstaver.</p>"
             "<p>For en digitalt tryg bruger med et almindeligt forbrug er ingen af de fire "
             "ting reelle ulemper. For en, der har brug for hjælp til opsætning eller vil "
             "kunne ringe til et menneske samme dag, er de det.</p>"),
        ],
    },
    "duka": {
        "h2_vurdering": "Duka vurderet: kort prisliste, få overraskelser",
        "h2_net": "Dukas netværk",
        "h2_hvem": "Er Duka det rigtige for dig?",
        "h2_sammenlign": "Duka mod de øvrige enkle abonnementer",
        "h2_skift": "Sådan skifter du til Duka",
        "net_note": ("Duka er en MVNO uden eget mobilnet og lejer kapacitet hos en af de tre "
                     "danske netværksejere. Vi angiver ikke et net uden at have verificeret "
                     "det. Tjek den aktuelle netværksangivelse hos Duka, hvis dækning vejer "
                     "tungt i dit valg."),
        "skift_note": ("Duka markedsfører abonnementer uden binding og uden oprettelsesgebyr. "
                       "Tjek dog altid de aktuelle vilkår på det konkrete produkt ved "
                       "bestilling, da det kan variere mellem produkterne."),
        "sektioner": [
            ("EU-data: det Duka gør anderledes",
             "<p>Et punkt, der er værd at fremhæve ved Duka, er behandlingen af EU-data. Hos "
             "mange danske udbydere er datamængden i EU markant lavere end i Danmark — du kan "
             "have 100 GB herhjemme og 15 GB på rejsen. Det opdager folk typisk på tredjedagen "
             "af ferien.</p>"
             "<p>Flere af Dukas abonnementer har den samme datamængde i EU som i Danmark, "
             "hvilket i praksis fjerner hele problemstillingen. Rejser du regelmæssigt i "
             "Europa, eller har du sommerhus eller familie i et andet EU-land, er det en reel "
             "og målbar fordel, som ikke fremgår af en almindelig pristabel med månedspriser.</p>"
             "<p>Sammenlign derfor ikke kun på pris og datamængde, men også på EU-kolonnen i "
             "vores tabeller. For en rejsende kan et abonnement, der er ti kroner dyrere om "
             "måneden, være det klart billigere valg over et år.</p>"),
            ("Et kort udvalg er en fordel, ikke en mangel",
             "<p>Duka har bevidst en stram produktpalette, og det er værd at forsvare som et "
             "designvalg frem for en begrænsning. På et marked med flere hundrede "
             "abonnementer er den største barriere for forbrugerne ikke mangel på muligheder — "
             "det er, at der er for mange.</p>"
             "<p>Forskning i forbrugeradfærd peger konsekvent på, at flere valgmuligheder "
             "fører til dårligere beslutninger og til, at folk helt undlader at vælge. Det er "
             "netop derfor, så mange danskere sidder på et abonnement, de valgte for fem år "
             "siden: det er nemmere at lade være.</p>"
             "<p>En prisliste, du kan overskue på et halvt minut, løser det problem. Du kan "
             "ikke sammensætte alt, men du kan træffe en beslutning — og en truffet "
             "beslutning til 89 kr. slår en udskudt beslutning til 179 kr. hver gang.</p>"),
        ],
    },
    "lyca-mobile": {
        "h2_vurdering": "Lyca Mobile vurderet: taletid og udland",
        "h2_net": "Lyca Mobiles netværk i Danmark",
        "h2_hvem": "Hvem skal vælge Lyca Mobile?",
        "h2_sammenlign": "Lyca Mobile mod de øvrige internationale udbydere",
        "h2_skift": "Sådan kommer du i gang hos Lyca Mobile",
        "net_note": ("Lyca Mobile er en international MVNO uden eget net i Danmark og lejer "
                     "kapacitet hos en af de tre netværksejere. Tjek den aktuelle "
                     "netværksangivelse på Lycas egen side, da MVNO-aftaler kan ændre sig."),
        "skift_note": ("Skifter du fra taletid til abonnement hos Lyca, kan du beholde dit "
                       "nummer. Det samme gælder den anden vej. Kontakt udbyderen, eller "
                       "bestil det nye produkt med nummerflytning."),
        "sektioner": [
            ("Taletid: den mest oversete løsning på det danske marked",
             "<p>Lyca er stor i taletidssegmentet, og taletid fortjener mere opmærksomhed, end "
             "det får. Med taletid betaler du forud, og du kan ikke overskride. Det lyder "
             "banalt, men det er en egenskab, ingen abonnementer kan matche.</p>"
             "<p>Det gør taletid til det tryggeste valg i tre situationer: til børn, hvor en "
             "uventet regning både er dyr og en dårlig start; til pårørende, der ikke skal "
             "kunne komme til at bruge for meget; og til dig selv, hvis du kun bruger "
             "telefonen sporadisk og ikke vil betale for en måned, hvor den lå i en skuffe.</p>"
             "<p>Ulempen er prisen pr. gigabyte, som typisk er højere end på et abonnement, og "
             "at du selv skal huske at fylde op. Bruger du telefonen dagligt, er et "
             "abonnement næsten altid billigere. Bruger du den sjældent, er taletid svær at slå.</p>"),
            ("Sammenlign ikke på antal minutter alene",
             "<p>Det er den fejl, vi ser oftest, når folk vælger abonnement til "
             "udlandsopkald. Antallet af inkluderede minutter er det tal, der står med store "
             "bogstaver, og det er også det mindst informative.</p>"
             "<p>Det, der afgør, om abonnementet er godt for dig, er hvilke lande der er "
             "dækket, og om dækningen gælder mobilnumre eller kun fastnet. Ringer du til et "
             "land, hvor familien udelukkende bruger mobil, er et abonnement med "
             "fastnetdækning i halvtreds lande værdiløst for dig, mens et med mobildækning i "
             "ti lande kan være perfekt.</p>"
             "<p>Fremgangsmåden er enkel: skriv de fem numre ned, du ringer mest til, og find "
             "dem i landelisten, før du bestiller. Det tager fem minutter og er den eneste "
             "måde at undgå at betale for en pakke, der ikke dækker dine faktiske opkald.</p>"),
        ],
    },
    "eesy": {
        "h2_vurdering": "eesy vurderet: digital model, lavere pris",
        "h2_net": "eesys netværk",
        "h2_hvem": "Passer en rent digital udbyder til dig?",
        "h2_sammenlign": "eesy mod de øvrige digitale udbydere",
        "h2_skift": "Sådan opretter du dig hos eesy",
        "net_note": ("eesy er en MVNO uden eget mobilnet og lejer kapacitet hos en af de tre "
                     "danske netværksejere. Vi angiver ikke et net uden at have verificeret "
                     "det. Tjek eesys egen side for den aktuelle angivelse."),
        "skift_note": ("Hos en rent digital udbyder foregår alt i app og selvbetjening. Vælg "
                       "eSIM, hvis din telefon understøtter det — så kan du være oppe at køre "
                       "få minutter efter bestilling i stedet for at vente på posten."),
        "sektioner": [
            ("Hvad den digitale model reelt betyder i hverdagen",
             "<p>At en udbyder er digital er ikke bare en besparelse, der sendes videre til "
             "dig. Det ændrer, hvordan du bruger abonnementet — og for de fleste til det bedre.</p>"
             "<p>Fordi alt ligger i appen, kan du skifte abonnement, slå datastop til, "
             "bestille et eSIM og se dit forbrug uden at tale med nogen. Ingen telefonkø, "
             "ingen åbningstider. Det gør det også markant nemmere at optimere løbende, og det "
             "er værd at bruge aktivt: den største enkeltbesparelse på mobilabonnement er "
             "stadig at flytte ned i datamængde, når man opdager, at man ikke bruger den, man "
             "betaler for.</p>"
             "<p>Bagsiden er reel og skal siges klart: har du brug for at ringe til et "
             "menneske, når noget driller, får du det ikke her. For teknisk usikre brugere er "
             "prisforskellen over et år sjældent stor nok til at retfærdiggøre en uge uden "
             "fungerende telefon.</p>"),
            ("eSIM gør skiftet til et spørgsmål om minutter",
             "<p>eesy er blandt de udbydere, hvor eSIM giver mest mening, fordi hele "
             "oprettelsesflowet er bygget digitalt. Du bestiller, får en QR-kode, scanner den "
             "— og så er du kunde.</p>"
             "<p>Det lyder som en detalje, men det er faktisk en af de vigtigste grunde til, "
             "at folk aldrig får skiftet selskab. Ventetiden på et fysisk simkort er den "
             "friktion, der får en god beslutning til at blive udskudt, og udskudte "
             "beslutninger koster i gennemsnit danskerne flere hundrede kroner om året.</p>"
             "<p>Tjek at din telefon understøtter eSIM, før du bestiller — de fleste modeller "
             "fra de senere år gør. Se vores <a href=\"/guides/esim/\">guide til eSIM</a> for "
             "fremgangsmåden trin for trin.</p>"),
        ],
    },
    "flexii": {
        "h2_vurdering": "Flexii vurderet: du sammensætter selv",
        "h2_net": "Flexiis netværk",
        "h2_hvem": "Hvornår er en byg-selv-model en fordel?",
        "h2_sammenlign": "Flexii mod færdige pakker fra andre udbydere",
        "h2_skift": "Sådan sætter du dit Flexii-abonnement sammen",
        "net_note": ("Flexii er en MVNO uden eget mobilnet og lejer kapacitet hos en af de tre "
                     "danske netværksejere. Vi angiver ikke et net uden at have verificeret "
                     "det. Tjek Flexiis egen side for den aktuelle angivelse."),
        "skift_note": ("Fordi du selv sammensætter abonnementet, er det værd at bruge fem "
                       "minutter på at finde dit faktiske forbrug først. Ellers ender du "
                       "typisk med at vælge rigeligt af alt — og så er en færdig pakke "
                       "billigere."),
        "sektioner": [
            ("Byg-selv-modellens indbyggede fælde",
             "<p>Idéen bag Flexii er god og løser et reelt problem: på et marked med færdige "
             "pakker betaler mange for noget, de ikke bruger. Har du brug for meget data og "
             "næsten ingen taletid, eller omvendt, betaler du hos de fleste andre selskaber "
             "for begge dele.</p>"
             "<p>Men modellen har en indbygget fælde, som er værd at kende, før du går i gang. "
             "Når man selv sammensætter, vælger man af sikkerhedshensyn for meget. Man tænker "
             "ikke på, hvad man brugte sidste måned, men på hvad man <em>kunne komme</em> til "
             "at bruge — og så ender totalprisen over en færdig pakke, man kunne have købt "
             "billigere.</p>"
             "<p>Den disciplinerede fremgangsmåde er at finde dit faktiske forbrug de seneste "
             "tre måneder i telefonens indstillinger, lægge tyve procent til, og vælge "
             "derefter. Se <a href=\"/guides/hvor-meget-data/\">vores guide</a> til hvordan du "
             "finder tallet.</p>"),
            ("Derfor er Flexii svær at sammenligne i en pristabel",
             "<p>Det er værd at være åben om en begrænsning ved vores egne tabeller: Flexii "
             "har ikke én pris. Fordi du selv sammensætter abonnementet, findes der ikke et "
             "fast produkt, vi kan stille op ved siden af en færdig pakke fra en anden udbyder.</p>"
             "<p>De priser, vi viser for Flexii, tager derfor udgangspunkt i en typisk "
             "sammensætning med fri tale og den angivne datamængde. Din egen konfiguration kan "
             "blive både billigere og dyrere, afhængigt af hvad du vælger til og fra.</p>"
             "<p>Brug tallene som et udgangspunkt for at vurdere, om Flexii ligger i det "
             "rigtige prisleje for dig — og lav derefter den præcise beregning på Flexiis "
             "egen side med netop din sammensætning. Det er den eneste måde at få et retvisende "
             "tal ved en byg-selv-model.</p>"),
        ],
    },
}
