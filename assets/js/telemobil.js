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

  /* ---- Abonnementsliste: filtre, sortering, detaljer ---- */
  (function () {
    var krop = document.querySelector(".planliste");
    if (!krop) return;

    var planer = Array.prototype.slice.call(krop.querySelectorAll(".plan"));
    var bar = document.querySelector(".filterbar");
    var visFlereBoks = document.querySelector(".vis-flere");
    var visFlereKnap = document.querySelector("[data-vis-flere]");
    var resterendeTekst = document.querySelector("[data-resterende]");
    var antalVist = document.querySelector("[data-antal-vist]");
    var tomBesked = document.querySelector("[data-tom]");
    var PORTION = 10;

    var valgt = { data: [], pris: [], binding: [], slug: [], net: [], ekstra: [] };
    var kunTilbud = false;
    var grænse = PORTION;

    function tal(el, navn) { return parseFloat(el.getAttribute("data-" + navn)); }

    /* Hver gruppe er et ELLER internt, og et OG på tværs af grupper —
       det er sådan folk forventer at filtre opfører sig. */
    function iData(p, v) {
      var gb = tal(p, "gb");
      if (v === "lille") return gb > 0 && gb <= 15;
      if (v === "mellem") return gb > 15 && gb <= 50;
      if (v === "stor") return gb > 50 && gb <= 100;
      if (v === "xl") return gb > 100 && gb < 900;
      if (v === "fri") return gb >= 900;
      return true;
    }
    function iPris(p, v) {
      var k = tal(p, "pris");
      if (v === "u50") return k > 0 && k < 50;
      if (v === "50-99") return k >= 50 && k <= 99;
      if (v === "100-149") return k >= 100 && k <= 149;
      if (v === "150-199") return k >= 150 && k <= 199;
      if (v === "o200") return k >= 200;
      return true;
    }
    function iBinding(p, v) {
      var b = tal(p, "binding");
      if (v === "0") return b === 0;
      if (v === "1-6") return b > 0 && b <= 6;
      if (v === "o6") return b > 6;
      return true;
    }

    function passer(p) {
      if (kunTilbud && p.getAttribute("data-tilbud") !== "1") return false;
      if (valgt.data.length && !valgt.data.some(function (v) { return iData(p, v); })) return false;
      if (valgt.pris.length && !valgt.pris.some(function (v) { return iPris(p, v); })) return false;
      if (valgt.binding.length && !valgt.binding.some(function (v) { return iBinding(p, v); })) return false;
      if (valgt.slug.length && valgt.slug.indexOf(p.getAttribute("data-slug")) === -1) return false;
      if (valgt.net.length && valgt.net.indexOf(p.getAttribute("data-net")) === -1) return false;
      if (valgt.ekstra.length) {
        var flag = (p.getAttribute("data-ekstra") || "").split(" ");
        for (var i = 0; i < valgt.ekstra.length; i++) {
          if (flag.indexOf(valgt.ekstra[i]) === -1) return false;
        }
      }
      return true;
    }

    function opdaterKnapper() {
      var noget = kunTilbud;
      Object.keys(valgt).forEach(function (n) {
        var grp = bar && bar.querySelector('.fb-grp[data-gruppe="' + n + '"]');
        if (!grp) return;
        var knap = grp.querySelector(".fb-knap");
        var antal = valgt[n].length;
        if (antal) noget = true;
        var maerke = knap.querySelector(".fb-tal");
        if (antal) {
          knap.setAttribute("data-aktiv", "1");
          if (!maerke) {
            maerke = document.createElement("span");
            maerke.className = "fb-tal";
            knap.insertBefore(maerke, knap.querySelector(".fb-pil"));
          }
          maerke.textContent = antal;
        } else {
          knap.removeAttribute("data-aktiv");
          if (maerke) maerke.remove();
        }
      });
      Array.prototype.forEach.call(document.querySelectorAll("[data-nulstil]"), function (k) {
        if (k.closest(".filterbar")) k.hidden = !noget;
      });
    }

    function opdater() {
      var matchende = 0;
      planer.forEach(function (p) {
        if (!passer(p)) { p.hidden = true; return; }
        matchende++;
        p.hidden = matchende > grænse;
      });
      if (antalVist) antalVist.textContent = matchende;
      if (tomBesked) tomBesked.hidden = matchende !== 0;
      var tilbage = Math.max(0, matchende - grænse);
      if (visFlereBoks) {
        visFlereBoks.hidden = tilbage === 0;
        if (resterendeTekst) {
          resterendeTekst.textContent = tilbage + " abonnement" +
            (tilbage === 1 ? "" : "er") + " tilbage";
        }
      }
      opdaterKnapper();
    }

    function sorter(noegle) {
      var faldende = noegle === "gb" || noegle === "tp";
      planer.sort(function (a, b) {
        var va = tal(a, noegle), vb = tal(b, noegle);
        if (isNaN(va)) va = faldende ? -Infinity : Infinity;
        if (isNaN(vb)) vb = faldende ? -Infinity : Infinity;
        // Abonnementer uden data hører nederst ved pris pr. GB
        if (noegle === "prgb") {
          if (va === 0) va = Infinity;
          if (vb === 0) vb = Infinity;
        }
        // Udbydere uden anmeldelsesscore hører nederst, ikke øverst
        if (noegle === "tp") {
          if (va === 0) va = -Infinity;
          if (vb === 0) vb = -Infinity;
        }
        return faldende ? vb - va : va - vb;
      });
      planer.forEach(function (p) { krop.appendChild(p); });
    }

    /* ---- Foldemenuer ---- */
    function lukAlle(undtagen) {
      Array.prototype.forEach.call(document.querySelectorAll(".fb-grp"), function (g) {
        if (g === undtagen) return;
        var k = g.querySelector(".fb-knap"), m = g.querySelector(".fb-menu");
        if (k) k.setAttribute("aria-expanded", "false");
        if (m) m.hidden = true;
      });
    }

    if (bar) {
      Array.prototype.forEach.call(bar.querySelectorAll(".fb-grp[data-gruppe]"), function (grp) {
        var knap = grp.querySelector(".fb-knap");
        var menu = grp.querySelector(".fb-menu");
        knap.addEventListener("click", function (ev) {
          ev.stopPropagation();
          var aaben = knap.getAttribute("aria-expanded") === "true";
          lukAlle(grp);
          knap.setAttribute("aria-expanded", aaben ? "false" : "true");
          menu.hidden = aaben;
        });
        menu.addEventListener("click", function (ev) { ev.stopPropagation(); });
      });

      Array.prototype.forEach.call(bar.querySelectorAll(".fb-menu input[data-f]"), function (inp) {
        inp.addEventListener("change", function () {
          var n = inp.getAttribute("data-f"), v = inp.value;
          var i = valgt[n].indexOf(v);
          if (inp.checked && i === -1) valgt[n].push(v);
          if (!inp.checked && i > -1) valgt[n].splice(i, 1);
          grænse = PORTION;
          opdater();
        });
      });

      Array.prototype.forEach.call(bar.querySelectorAll("[data-ryd]"), function (k) {
        k.addEventListener("click", function () {
          var n = k.getAttribute("data-ryd");
          valgt[n] = [];
          Array.prototype.forEach.call(
            bar.querySelectorAll('input[data-f="' + n + '"]'),
            function (i) { i.checked = false; });
          grænse = PORTION;
          opdater();
        });
      });

      var tilbudKnap = bar.querySelector("[data-kun-tilbud]");
      if (tilbudKnap) {
        tilbudKnap.addEventListener("click", function () {
          kunTilbud = !kunTilbud;
          tilbudKnap.setAttribute("aria-pressed", kunTilbud ? "true" : "false");
          grænse = PORTION;
          opdater();
        });
      }

      var sortVaelger = bar.querySelector("[data-sorter]");
      if (sortVaelger) {
        sortVaelger.addEventListener("change", function () {
          sorter(sortVaelger.value);
          grænse = PORTION;
          opdater();
        });
      }

      document.addEventListener("click", function () { lukAlle(null); });
      document.addEventListener("keydown", function (ev) {
        if (ev.key === "Escape") lukAlle(null);
      });
    }

    Array.prototype.forEach.call(document.querySelectorAll("[data-nulstil]"), function (k) {
      k.addEventListener("click", function () {
        Object.keys(valgt).forEach(function (n) { valgt[n] = []; });
        kunTilbud = false;
        if (bar) {
          Array.prototype.forEach.call(bar.querySelectorAll("input[data-f]"),
            function (i) { i.checked = false; });
          var t = bar.querySelector("[data-kun-tilbud]");
          if (t) t.setAttribute("aria-pressed", "false");
        }
        grænse = PORTION;
        opdater();
      });
    });

    if (visFlereKnap) {
      visFlereKnap.addEventListener("click", function () {
        grænse += PORTION;
        opdater();
      });
    }

    /* ---- Se detaljer ---- */
    krop.addEventListener("click", function (ev) {
      var k = ev.target.closest && ev.target.closest(".pk-detaljer");
      if (!k) return;
      var panel = document.getElementById(k.getAttribute("aria-controls"));
      if (!panel) return;
      var aaben = k.getAttribute("aria-expanded") === "true";
      k.setAttribute("aria-expanded", aaben ? "false" : "true");
      k.textContent = aaben ? "Se detaljer" : "Skjul detaljer";
      panel.hidden = aaben;
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

/* ---- Regningstjek i heroen ---- */
(function () {
  "use strict";
  var boks = document.querySelector("[data-regningstjek]");
  if (!boks) return;

  var data;
  try {
    data = JSON.parse(boks.querySelector("[data-rt-data]").textContent);
  } catch (e) { return; }

  var felt = boks.querySelector("#rt-belob");
  var knap = boks.querySelector("[data-rt-beregn]");
  var overlay = document.querySelector("[data-rt-overlay]");
  // Flyt overlayet ud af heroen. Ellers fanger heroens stakkontekst det under
  // den faste header, og krydset kan ikke klikkes.
  if (overlay && overlay.parentElement !== document.body) {
    document.body.appendChild(overlay);
  }
  var svar = overlay ? overlay.querySelector("[data-rt-svar]") : null;
  var sidstFokus = null;

  function aabn() {
    sidstFokus = document.activeElement;
    overlay.hidden = false;
    document.body.style.overflow = "hidden";
    requestAnimationFrame(function () {
      overlay.classList.add("vist");
      var f = overlay.querySelector("[data-rt-luk]");
      if (f) f.focus();
    });
  }

  function luk() {
    overlay.classList.remove("vist");
    document.body.style.overflow = "";
    setTimeout(function () { overlay.hidden = true; }, 240);
    if (sidstFokus) sidstFokus.focus();
  }

  function kr(n) { return Math.round(n).toLocaleString("da-DK"); }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // Ét forslagskort med rigtig pris, besparelse og direkte link
  function kort(f, belob) {
    var spar = belob - f.gns12;
    var sparlinje = spar > 0
      ? '<span class="rf-spar">Spar ' + kr(spar * 12) + ' kr./år</span>'
      : '';
    var intro = f.intro_mdr
      ? '<span class="rf-intro">' + f.intro_mdr + ' mdr. tilbud · derefter ' +
        kr(f.normalpris) + ' kr.</span>'
      : '<span class="rf-intro">Fast pris</span>';

    return '<div class="rf-kort">' +
      '<div class="rf-hoved">' +
        '<img src="' + f.logo + '" alt="' + esc(f.udbyder) + '" width="' + f.logo_w +
          '" height="22" loading="lazy">' +
        '<span class="rf-hvorfor">' + esc(f.hvorfor) + '</span>' +
      '</div>' +
      '<div class="rf-navn">' + esc(f.navn) + '</div>' +
      '<div class="rf-fakta">' + esc(f.data) + ' · ' + esc(f.net) + '</div>' +
      '<div class="rf-pris"><b>' + kr(f.pris) + '</b><span>kr./md.</span>' + sparlinje + '</div>' +
      intro +
      '<div class="rf-knapper">' +
        '<a class="knap knap-primaer rf-cta" href="' + f.link +
          '" rel="sponsored nofollow noopener" target="_blank" data-udgaaende="hero">' +
          'Se tilbud →</a>' +
        '<a class="rf-laes" href="' + f.side + '">Læs om ' + esc(f.udbyder) + '</a>' +
      '</div>' +
    '</div>';
  }

  function beregn() {
    var belob = parseInt(felt.value, 10);
    if (!belob || belob < 1) {
      felt.focus();
      felt.classList.add("rt-fejl");
      setTimeout(function () { felt.classList.remove("rt-fejl"); }, 1200);
      return;
    }

    // Kun forslag der faktisk er billigere end det, brugeren betaler
    var relevante = data.forslag.filter(function (f) { return f.gns12 < belob; });
    var bedste = data.forslag.reduce(function (a, b) {
      return b.gns12 < a.gns12 ? b : a;
    });
    var spar = belob - bedste.gns12;
    var overMedian = belob - data.median;

    var html;
    if (spar <= 0) {
      html =
        '<p class="rt-overskrift" id="rt-dialog-titel">Du betaler allerede skarpt</p>' +
        '<p class="rt-brod">Din pris på <strong>' + kr(belob) + ' kr.</strong> ligger på ' +
        'niveau med markedets billigste. Der er ikke meget at hente — men tjek at du får ' +
        'den datamængde, du faktisk bruger.</p>' +
        '<div class="rf-gitter">' + data.forslag.map(function (f) {
          return kort(f, belob);
        }).join("") + '</div>';
    } else {
      html =
        '<p class="rt-overskrift" id="rt-dialog-titel">Du kan spare op til <span class="rt-tal">' +
        kr(spar * 12) + ' kr.</span> om året</p>' +
        '<p class="rt-brod">Du betaler <strong>' + kr(belob) + ' kr./md.</strong>' +
        (overMedian > 0
          ? ' — <strong>' + kr(overMedian) + ' kr. mere</strong> end medianen på det ' +
            'danske marked (' + kr(data.median) + ' kr.).'
          : '. Du ligger allerede under medianen, men der er stadig billigere valg.') +
        ' Her er tre, der passer til forskellige behov:</p>' +
        '<div class="rf-gitter">' +
          (relevante.length ? relevante : data.forslag).map(function (f) {
            return kort(f, belob);
          }).join("") +
        '</div>' +
        '<p class="rf-note">Priserne er den pris, du starter på. Tallet i parentes er ' +
        'gennemsnittet over 12 måneder. Annoncelinks — vi kan modtage provision.</p>';
    }

    html += '<div class="rf-bund">' +
      '<a class="rf-alle" href="/billigste-mobilabonnement/">Se alle ' + data.antal +
      ' abonnementer →</a>' +
      '<button type="button" class="rt-igen" data-rt-luk>Prøv et andet beløb</button>' +
      '</div>';

    svar.innerHTML = html;
    aabn();
  }

  knap.addEventListener("click", beregn);
  felt.addEventListener("keydown", function (e) {
    if (e.key === "Enter") beregn();
  });

  boks.querySelectorAll("[data-belob]").forEach(function (k) {
    k.addEventListener("click", function () {
      felt.value = k.getAttribute("data-belob");
      beregn();
    });
  });

  // Luk: kryds, knap, klik på baggrund eller Esc
  overlay.addEventListener("click", function (e) {
    if (e.target.closest("[data-rt-luk]") || !e.target.closest(".rt-dialog")) luk();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !overlay.hidden) luk();
  });
})();
