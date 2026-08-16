/* telemobil.dk — interaktion. Ingen afhængigheder. */
(function () {
  "use strict";
  var roligt = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Dropdown-menuer ---- */
  var grupper = Array.prototype.slice.call(document.querySelectorAll(".nav-gruppe"));
  grupper.forEach(function (g) {
    var knap = g.querySelector(".nav-knap");
    var menu = g.querySelector(".nav-menu");
    if (!knap || !menu) return;

    knap.addEventListener("click", function (e) {
      e.stopPropagation();
      var aaben = menu.classList.contains("aaben");
      grupper.forEach(function (anden) {
        anden.querySelector(".nav-menu").classList.remove("aaben");
        anden.querySelector(".nav-knap").setAttribute("aria-expanded", "false");
      });
      if (!aaben) {
        menu.classList.add("aaben");
        knap.setAttribute("aria-expanded", "true");
      }
    });

    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        menu.classList.remove("aaben");
        knap.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("click", function () {
    grupper.forEach(function (g) {
      g.querySelector(".nav-menu").classList.remove("aaben");
      g.querySelector(".nav-knap").setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    grupper.forEach(function (g) {
      if (g.querySelector(".nav-menu").classList.contains("aaben")) {
        g.querySelector(".nav-menu").classList.remove("aaben");
        g.querySelector(".nav-knap").setAttribute("aria-expanded", "false");
        g.querySelector(".nav-knap").focus();
      }
    });
  });

  /* ---- Mobilmenu ---- */
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var aaben = nav.classList.toggle("aaben");
      burger.setAttribute("aria-expanded", aaben ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("aaben");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---- Skygge under sticky header ---- */
  var hoved = document.querySelector(".hoved");
  if (hoved) {
    var skygget = false;
    var venter = false;
    var opdaterSkygge = function () {
      venter = false;
      var skalHave = window.scrollY > 8;
      if (skalHave !== skygget) {
        skygget = skalHave;
        hoved.classList.toggle("skygget", skalHave);
      }
    };
    opdaterSkygge();
    window.addEventListener("scroll", function () {
      if (!venter) { venter = true; requestAnimationFrame(opdaterSkygge); }
    }, { passive: true });
  }

  /* ---- Scroll-afsløring ---- */
  var maal = document.querySelectorAll(".afslør");
  if (maal.length) {
    if (roligt || !("IntersectionObserver" in window)) {
      maal.forEach(function (el) { el.classList.add("vist"); });
    } else {
      // threshold skal være 0: elementer højere end skærmen kan aldrig nå en
      // procentdel, og ville så aldrig blive vist. rootMargin styrer timingen.
      var obs = new IntersectionObserver(function (poster) {
        poster.forEach(function (post) {
          if (post.isIntersecting) {
            post.target.classList.add("vist");
            obs.unobserve(post.target);
          }
        });
      }, { threshold: 0, rootMargin: "0px 0px -60px 0px" });
      maal.forEach(function (el) { obs.observe(el); });

      // Sikkerhedsnet: uanset hvad må intet indhold stå usynligt
      setTimeout(function () {
        maal.forEach(function (el) { el.classList.add("vist"); });
      }, 2500);
    }
  }

  /* ---- Tælleeffekt på tal ---- */
  var taellere = document.querySelectorAll("[data-tael]");
  if (taellere.length && !roligt && "IntersectionObserver" in window) {
    var tObs = new IntersectionObserver(function (poster) {
      poster.forEach(function (post) {
        if (!post.isIntersecting) return;
        var el = post.target;
        tObs.unobserve(el);
        var slut = parseFloat(el.getAttribute("data-tael"));
        var suffiks = el.getAttribute("data-suffiks") || "";
        var start = null, varighed = 1100;
        function trin(tid) {
          if (!start) start = tid;
          var p = Math.min((tid - start) / varighed, 1);
          var lettet = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(slut * lettet).toLocaleString("da-DK") + suffiks;
          if (p < 1) requestAnimationFrame(trin);
        }
        requestAnimationFrame(trin);
      });
    }, { threshold: 0.5 });
    taellere.forEach(function (el) { tObs.observe(el); });
  }

  /* ---- Abonnementsliste: filter, sortering og visning ---- */
  (function () {
    var krop = document.querySelector(".planliste");
    if (!krop) return;

    var planer = Array.prototype.slice.call(krop.querySelectorAll(".plan"));
    var visFlereBoks = document.querySelector(".vis-flere");
    var visFlereKnap = document.querySelector("[data-vis-flere]");
    var resterendeTekst = document.querySelector("[data-resterende]");
    var antalVist = document.querySelector("[data-antal-vist]");
    var PORTION = 10;

    var dataFilter = "alle";
    var prisFilter = "alle";
    var grænse = PORTION;

    function passer(p) {
      var gb = parseInt(p.getAttribute("data-gb"), 10);
      var pris = parseFloat(p.getAttribute("data-pris"));
      if (dataFilter === "lille" && gb > 15) return false;
      if (dataFilter === "mellem" && !(gb > 15 && gb <= 50)) return false;
      if (dataFilter === "stor" && !(gb > 50 && gb < 900)) return false;
      if (dataFilter === "fri" && gb < 900) return false;
      if (prisFilter === "u50" && !(pris > 0 && pris < 50)) return false;
      if (prisFilter === "50-99" && !(pris >= 50 && pris <= 99)) return false;
      if (prisFilter === "100-199" && !(pris >= 100 && pris <= 199)) return false;
      if (prisFilter === "o200" && pris < 200) return false;
      return true;
    }

    // Én funktion styrer synlighed — så sortering altid viser de øverste
    function opdater() {
      var matchende = 0;
      planer.forEach(function (p) {
        if (!passer(p)) {
          p.hidden = true;
          return;
        }
        matchende++;
        p.hidden = matchende > grænse;
      });
      if (antalVist) antalVist.textContent = matchende;
      var tilbage = Math.max(0, matchende - grænse);
      if (visFlereBoks) {
        visFlereBoks.hidden = tilbage === 0;
        if (resterendeTekst) {
          resterendeTekst.textContent = tilbage + " abonnement" +
            (tilbage === 1 ? "" : "er") + " tilbage";
        }
      }
    }

    if (visFlereKnap) {
      visFlereKnap.addEventListener("click", function () {
        grænse += PORTION;
        opdater();
      });
    }

    function knapgruppe(vaelger, saet) {
      var knapper = Array.prototype.slice.call(document.querySelectorAll(vaelger));
      knapper.forEach(function (k) {
        k.addEventListener("click", function () {
          knapper.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
          k.setAttribute("aria-pressed", "true");
          saet(k);
          grænse = PORTION;
          opdater();
        });
      });
    }

    knapgruppe(".chip[data-filter]", function (k) {
      dataFilter = k.getAttribute("data-filter");
    });
    knapgruppe(".chip[data-pris]", function (k) {
      prisFilter = k.getAttribute("data-pris");
    });

    knapgruppe("[data-sorter]", function (k) {
      var noegle = k.getAttribute("data-sorter");
      var faldende = noegle === "gb";
      planer.sort(function (a, b) {
        var va = parseFloat(a.getAttribute("data-" + noegle));
        var vb = parseFloat(b.getAttribute("data-" + noegle));
        if (isNaN(va)) va = faldende ? -Infinity : Infinity;
        if (isNaN(vb)) vb = faldende ? -Infinity : Infinity;
        // Abonnementer uden data hører nederst ved pris pr. GB
        if (noegle === "prgb") {
          if (va === 0) va = Infinity;
          if (vb === 0) vb = Infinity;
        }
        return faldende ? vb - va : va - vb;
      });
      planer.forEach(function (p) { krop.appendChild(p); });
    });

    opdater();
  })();

  /* ---- Sporing af udgående affiliate-klik (klar til GA4) ---- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-udgaaende]");
    if (!a) return;
    if (typeof window.gtag === "function") {
      window.gtag("event", "klik_udbyder", {
        udbyder: a.getAttribute("data-udgaaende"),
        abonnement: a.getAttribute("data-abonnement") || ""
      });
    }
  });
})();

/* ---- Abonnementsfinder ---- */
(function () {
  "use strict";
  var boks = document.querySelector("[data-quiz]");
  var raa = document.querySelector("[data-quizdata]");
  if (!boks || !raa) return;

  var planer;
  try { planer = JSON.parse(raa.textContent); } catch (e) { return; }

  var trin = Array.prototype.slice.call(boks.querySelectorAll(".quiz-trin"));
  var svarboks = boks.querySelector("[data-svar]");
  var svar = {};

  function visTrin(i) {
    trin.forEach(function (t, n) { t.hidden = n !== i; });
    svarboks.hidden = true;
  }

  function gbBehov() {
    return { lav: 5, mellem: 20, hoej: 60, ekstrem: 999 }[svar.forbrug] || 20;
  }

  function beregn() {
    var maal = gbBehov();
    var kandidater = planer.filter(function (p) {
      if (svar.tale === "fri" && p.tale !== "fri") return false;
      if (svar.stream === "ja" && p.stream === 0) return false;
      if (svar.stream === "nej" && p.stream > 0) return false;
      if (svar.sted === "land" && p.net !== "TDC NET") return false;
      if (maal >= 999) return p.gb >= 900;
      return p.gb >= maal && p.gb < 900;
    });

    // Falder et filter helt ud, løsnes kravet om net frem for at vise ingenting
    if (!kandidater.length) {
      kandidater = planer.filter(function (p) {
        if (svar.tale === "fri" && p.tale !== "fri") return false;
        if (maal >= 999) return p.gb >= 900;
        return p.gb >= maal;
      });
    }
    kandidater.sort(function (a, b) { return a.gns - b.gns; });
    return kandidater.slice(0, 3);
  }

  function visSvar() {
    var top = beregn();
    trin.forEach(function (t) { t.hidden = true; });
    svarboks.hidden = false;

    if (!top.length) {
      svarboks.innerHTML = '<p>Vi fandt ingen match. <button type="button" class="knap knap-linje knap-lille" data-igen>Prøv igen</button></p>';
    } else {
      var maal = gbBehov();
      var html = '<div class="quiz-tael">Dit match</div><h3>' +
        (maal >= 999 ? "Fri data" : maal + " GB eller mere") +
        (svar.tale === "fri" ? " med fri tale" : "") +
        (svar.sted === "land" ? " på TDC NET" : "") + "</h3>" +
        '<p class="quiz-note">Sorteret efter gennemsnitspris over 12 måneder — ikke intropris.</p><div class="quiz-kort">';
      top.forEach(function (p, i) {
        html += '<a class="quiz-plan' + (i === 0 ? " bedst" : "") + '" href="/udbydere/' + p.slug + '/">' +
          (i === 0 ? '<span class="maerke maerke-puls">Bedste match</span>' : "") +
          '<img src="/assets/img/logoer/' + p.logo + '" alt="" width="' + (p.lw || 50) + '" height="22" loading="lazy">' +
          "<b>" + p.navn + "</b>" +
          "<small>" + (p.gb >= 900 ? "Fri data" : p.gb + " GB") + " · " + p.net + "</small>" +
          '<span class="quiz-pris">' + p.gns + " kr.<em>/md. i snit</em></span></a>";
      });
      html += '</div><button type="button" class="knap knap-linje knap-lille" data-igen>Start forfra</button>';
      svarboks.innerHTML = html;
    }
  }

  boks.addEventListener("click", function (e) {
    var knap = e.target.closest("button");
    if (!knap) return;

    if (knap.hasAttribute("data-igen")) {
      svar = {};
      visTrin(0);
      return;
    }
    if (!knap.hasAttribute("data-vaerdi")) return;

    var t = knap.closest(".quiz-trin");
    svar[t.getAttribute("data-noegle")] = knap.getAttribute("data-vaerdi");
    var i = parseInt(t.getAttribute("data-trin"), 10);
    if (i + 1 < trin.length) visTrin(i + 1); else visSvar();
  });
})();

/* ---- Landekodesøgning ---- */
(function () {
  "use strict";
  var soeg = document.querySelector("[data-landesoeg]");
  var tabel = document.querySelector(".landetabel");
  if (!soeg || !tabel) return;
  var raekker = Array.prototype.slice.call(tabel.querySelectorAll("tbody tr"));
  var tael = document.querySelector("[data-landeantal]");
  var tom = document.querySelector("[data-landetom]");
  var region = "alle";

  function anvend() {
    var q = soeg.value.trim().toLowerCase().replace(/^\+/, "");
    var vist = 0;
    raekker.forEach(function (r) {
      var okRegion = region === "alle" || r.getAttribute("data-region") === region;
      var okSoeg = !q ||
        r.getAttribute("data-land").indexOf(q) > -1 ||
        r.getAttribute("data-kode").indexOf(q) === 0;
      var ok = okRegion && okSoeg;
      r.hidden = !ok;
      if (ok) vist++;
    });
    if (tael) tael.textContent = vist;
    if (tom) tom.hidden = vist > 0;
  }

  soeg.addEventListener("input", anvend);
  document.querySelectorAll("[data-region]").forEach(function (k) {
    if (k.tagName !== "BUTTON") return;
    k.addEventListener("click", function () {
      document.querySelectorAll("button[data-region]").forEach(function (x) {
        x.setAttribute("aria-pressed", "false");
      });
      k.setAttribute("aria-pressed", "true");
      region = k.getAttribute("data-region");
      anvend();
    });
  });
})();

/* ---- Nummeropslag ---- */
(function () {
  "use strict";
  var felt = document.querySelector("[data-nummer]");
  var knap = document.querySelector("[data-slaa-op]");
  var svar = document.querySelector("[data-opslagsvar]");
  if (!felt || !knap || !svar) return;

  var lande = [];
  var kilde = document.querySelector("[data-landedata]");
  if (kilde) {
    try { lande = JSON.parse(kilde.textContent); } catch (e) { lande = []; }
  }
  if (!lande.length) {
    document.querySelectorAll(".landetabel tbody tr").forEach(function (r) {
      lande.push({ navn: r.cells[0].textContent.trim(), kode: r.getAttribute("data-kode"),
                   risiko: r.hasAttribute("data-risiko"), flag: "" });
    });
  }
  if (!lande.length) return;

  function slaaOp() {
    var raa = felt.value.replace(/[^\d+]/g, "");
    svar.hidden = false;

    if (!raa) {
      svar.className = "opslag-svar";
      svar.innerHTML = "<p>Indtast et nummer med landekode, fx +49 30 123456.</p>";
      return;
    }
    if (raa.indexOf("+") !== 0 && raa.indexOf("00") !== 0) {
      svar.className = "opslag-svar neutral";
      svar.innerHTML = "<h3>Ser ud til at være et dansk nummer</h3><p>Nummeret starter ikke " +
        "med + eller 00, så det er sandsynligvis nationalt. Danske numre er otte cifre uden " +
        "landekode. Er du i tvivl, så søg på nummeret, før du ringer tilbage.</p>";
      return;
    }
    var cifre = raa.replace(/^\+/, "").replace(/^00/, "");
    // Længste kode først, så +298 ikke forveksles med +29
    var fund = null;
    lande.slice().sort(function (a, b) { return b.kode.length - a.kode.length; })
      .some(function (l) {
        if (cifre.indexOf(l.kode) === 0) { fund = l; return true; }
        return false;
      });

    if (!fund) {
      svar.className = "opslag-svar advar";
      svar.innerHTML = "<h3>Landekoden er ikke i vores oversigt</h3><p>Vi dækker de mest " +
        "brugte landekoder. Kender du ingen i udlandet, så ring ikke tilbage — det koster " +
        "ikke noget at modtage opkaldet, kun at besvare det.</p>";
      return;
    }
    if (fund.risiko) {
      svar.className = "opslag-svar advar";
      svar.innerHTML = "<h3>" + (fund.flag || "") + " " + fund.navn + " — vær opmærksom</h3>" +
        "<p>Nummeret kommer fra <strong>" + fund.navn + "</strong> (+" + fund.kode + "). " +
        "Denne landekode optræder ofte i wangiri-svindel, hvor telefonen ringer én gang for " +
        "at lokke dig til at ringe tilbage til et dyrt nummer.</p>" +
        "<p><strong>Ring ikke tilbage</strong>, medmindre du forventede opkaldet. Bloker " +
        "nummeret, og overvej at bede din udbyder spærre for udgående udlandsopkald.</p>";
    } else {
      svar.className = "opslag-svar neutral";
      svar.innerHTML = "<h3>" + (fund.flag || "") + " " + fund.navn + "</h3>" +
        "<p>Nummeret kommer fra <strong>" + fund.navn + "</strong> (+" + fund.kode + "). " +
        "Vi har ikke markeret denne landekode som hyppig i svindelopkald.</p>" +
        "<p>Husk at det er gratis at modtage opkaldet. Ringer du tilbage til et udenlandsk " +
        "nummer, betaler du selv taksten — og nummervisning kan forfalskes.</p>";
    }
  }

  knap.addEventListener("click", slaaOp);
  felt.addEventListener("keydown", function (e) { if (e.key === "Enter") slaaOp(); });
})();

/* ---- Hastighedstest ---- */
(function () {
  "use strict";
  var knap = document.querySelector("[data-speedtest]");
  if (!knap) return;
  var boks = document.querySelector("[data-st-resultat]");
  var tal = document.querySelector("[data-st-mbit]");
  var vurdering = document.querySelector("[data-st-vurdering]");

  function beskriv(mbit) {
    if (mbit < 1) return "Meget lav. Er din datamængde brugt op? Mange udbydere sætter " +
      "hastigheden ned frem for at stoppe forbindelsen.";
    if (mbit < 3) return "Nok til beskeder, sociale medier og musik, men video vil " +
      "sandsynligvis buffe.";
    if (mbit < 10) return "Fint til video i standardkvalitet og videomøder. Dækker de " +
      "flestes hverdagsbrug.";
    if (mbit < 30) return "God forbindelse. Rækker til HD-video og hotspot til en laptop.";
    return "Meget god forbindelse. Du mærker ikke begrænsninger i almindelig brug.";
  }

  knap.addEventListener("click", function () {
    knap.disabled = true;
    knap.textContent = "Måler …";
    boks.hidden = false;
    tal.textContent = "—";
    vurdering.textContent = "";

    var url = "/assets/hastighedstest.bin?n=" + Date.now();
    var start = performance.now();

    fetch(url, { cache: "no-store" })
      .then(function (r) { return r.arrayBuffer(); })
      .then(function (buf) {
        var sek = (performance.now() - start) / 1000;
        var mbit = (buf.byteLength * 8) / sek / 1000000;
        tal.textContent = mbit < 10 ? mbit.toFixed(1).replace(".", ",") : Math.round(mbit);
        vurdering.textContent = beskriv(mbit);
        knap.disabled = false;
        knap.textContent = "Test igen";
      })
      .catch(function () {
        vurdering.textContent = "Testen kunne ikke gennemføres. Tjek din forbindelse og prøv igen.";
        knap.disabled = false;
        knap.textContent = "Prøv igen";
      });
  });
})();

/* ---- Cookiesamtykke ---- */
(function () {
  "use strict";
  var NOEGLE = "telemobil-samtykke";
  var GYLDIG_DAGE = 180;

  function laes() {
    try {
      var raa = document.cookie.split("; ").find(function (c) {
        return c.indexOf(NOEGLE + "=") === 0;
      });
      return raa ? JSON.parse(decodeURIComponent(raa.split("=")[1])) : null;
    } catch (e) { return null; }
  }

  function gem(valg) {
    var udloeb = new Date(Date.now() + GYLDIG_DAGE * 864e5).toUTCString();
    document.cookie = NOEGLE + "=" + encodeURIComponent(JSON.stringify(valg)) +
      ";expires=" + udloeb + ";path=/;SameSite=Lax";
    anvend(valg);
  }

  // Statistik aktiveres kun ved samtykke. Uden samtykke sættes intet.
  function anvend(valg) {
    if (valg && valg.statistik && typeof window.gtag === "function") {
      window.gtag("consent", "update", { analytics_storage: "granted" });
    }
    window.telemobilSamtykke = valg;
    document.dispatchEvent(new CustomEvent("samtykke", { detail: valg }));
  }

  function byg() {
    var b = document.createElement("div");
    b.className = "cookiebanner";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Samtykke til cookies");
    b.innerHTML =
      '<div class="cb-indhold">' +
        '<div class="cb-tekst">' +
          '<strong>Vi bruger cookies</strong>' +
          '<p>Nødvendige cookies får siden til at fungere. Statistikcookies hjælper os med ' +
          'at se, hvilke sider der bliver brugt — de sættes kun, hvis du siger ja. ' +
          '<a href="/cookiepolitik/">Læs cookiepolitikken</a>.</p>' +
        '</div>' +
        '<div class="cb-knapper">' +
          '<button type="button" class="knap knap-linje" data-cb="noedvendige">Kun nødvendige</button>' +
          '<button type="button" class="knap knap-primaer" data-cb="alle">Tillad alle</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(b);
    requestAnimationFrame(function () { b.classList.add("vist"); });

    b.querySelectorAll("[data-cb]").forEach(function (k) {
      k.addEventListener("click", function () {
        gem({ noedvendige: true, statistik: k.getAttribute("data-cb") === "alle",
              dato: new Date().toISOString() });
        b.classList.remove("vist");
        setTimeout(function () { b.remove(); }, 300);
      });
    });
  }

  var valg = laes();
  if (valg) {
    anvend(valg);
  } else {
    byg();
  }

  // Link i footeren så valget kan ændres bagefter
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-cookievalg]");
    if (!a) return;
    e.preventDefault();
    document.cookie = NOEGLE + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    byg();
  });
})();
