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
    var opdaterSkygge = function () {
      hoved.classList.toggle("skygget", window.scrollY > 8);
    };
    opdaterSkygge();
    window.addEventListener("scroll", opdaterSkygge, { passive: true });
  }

  /* ---- Scroll-afsløring ---- */
  var maal = document.querySelectorAll(".afslør");
  if (maal.length) {
    if (roligt || !("IntersectionObserver" in window)) {
      maal.forEach(function (el) { el.classList.add("vist"); });
    } else {
      var obs = new IntersectionObserver(function (poster) {
        poster.forEach(function (post) {
          if (post.isIntersecting) {
            post.target.classList.add("vist");
            obs.unobserve(post.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      maal.forEach(function (el) { obs.observe(el); });
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

  /* ---- Tabel: vis flere ad gangen ---- */
  document.querySelectorAll(".listeramme").forEach(function (ramme) {
    var knap = ramme.querySelector("[data-vis-flere]");
    if (!knap) return;
    var tael = ramme.querySelector("[data-resterende]");
    var krop = ramme.querySelector(".planliste");
    var PORTION = 10;

    knap.addEventListener("click", function () {
      var skjulte = Array.prototype.filter.call(
        krop.querySelectorAll(".plan"),
        function (r) { return r.hidden && r.getAttribute("data-filtreret") !== "ja"; }
      );
      skjulte.slice(0, PORTION).forEach(function (r) { r.hidden = false; });
      var tilbage = skjulte.length - Math.min(PORTION, skjulte.length);
      if (tilbage > 0) {
        tael.textContent = tilbage + " abonnementer tilbage";
      } else {
        knap.closest(".vis-flere").remove();
      }
    });
  });

  /* ---- Tabel: filtrering ---- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  var tabel = document.querySelector(".planliste");
  if (chips.length && tabel) {
    var raekker = Array.prototype.slice.call(tabel.querySelectorAll(".plan"));
    var visTaeller = document.querySelector("[data-antal-vist]");
    var visFlereBoks = document.querySelector(".vis-flere");

    function anvend(filter) {
      var vist = 0;
      raekker.forEach(function (r) {
        var gb = parseInt(r.getAttribute("data-gb"), 10);
        var ok = true;
        if (filter === "lille") ok = gb <= 15;
        else if (filter === "mellem") ok = gb > 15 && gb <= 50;
        else if (filter === "stor") ok = gb > 50 && gb < 900;
        else if (filter === "fri") ok = gb >= 900;
        r.setAttribute("data-filtreret", ok ? "nej" : "ja");
        r.hidden = !ok;
        if (ok) vist++;
      });
      if (visTaeller) visTaeller.textContent = vist;
      // Ved aktivt filter vises alle match; knappen giver ikke mening
      if (visFlereBoks) visFlereBoks.hidden = (filter !== "alle");
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        c.setAttribute("aria-pressed", "true");
        anvend(c.getAttribute("data-filter"));
      });
    });
  }

  /* ---- Liste: sortering ---- */
  document.querySelectorAll(".listeramme").forEach(function (ramme) {
    var knapper = Array.prototype.slice.call(ramme.querySelectorAll("[data-sorter]"));
    var krop = ramme.querySelector(".planliste");
    if (!knapper.length || !krop) return;

    knapper.forEach(function (k) {
      k.addEventListener("click", function () {
        var noegle = k.getAttribute("data-sorter");
        var faldende = noegle === "gb";
        knapper.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        k.setAttribute("aria-pressed", "true");

        var planer = Array.prototype.slice.call(krop.querySelectorAll(".plan"));
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
    });
  });

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
          '<img src="/assets/img/logoer/' + p.logo + '" alt="" height="20">' +
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
