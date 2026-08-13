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
  document.querySelectorAll(".tabelramme").forEach(function (ramme) {
    var knap = ramme.querySelector("[data-vis-flere]");
    if (!knap) return;
    var tael = ramme.querySelector("[data-resterende]");
    var krop = ramme.querySelector("tbody");
    var PORTION = 10;

    knap.addEventListener("click", function () {
      var skjulte = Array.prototype.filter.call(
        krop.querySelectorAll("tr"),
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
  var tabel = document.querySelector("table.pris");
  if (chips.length && tabel) {
    var raekker = Array.prototype.slice.call(tabel.querySelectorAll("tbody tr"));
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

  /* ---- Tabel: sortering ---- */
  var sorterbare = document.querySelectorAll("table.pris th.sorter");
  sorterbare.forEach(function (th) {
    th.setAttribute("tabindex", "0");
    th.setAttribute("role", "button");

    function sorter() {
      var t = th.closest("table");
      var krop = t.querySelector("tbody");
      var noegle = th.getAttribute("data-noegle");
      var nuvaerende = th.getAttribute("data-retning");
      var retning = nuvaerende === "op" ? "ned" : "op";

      t.querySelectorAll("th.sorter").forEach(function (x) { x.removeAttribute("data-retning"); });
      th.setAttribute("data-retning", retning);

      var raekker = Array.prototype.slice.call(krop.querySelectorAll("tr"));
      raekker.sort(function (a, b) {
        var va = a.getAttribute("data-" + noegle);
        var vb = b.getAttribute("data-" + noegle);
        var na = parseFloat(va), nb = parseFloat(vb);
        var res;
        if (!isNaN(na) && !isNaN(nb)) res = na - nb;
        else res = String(va).localeCompare(String(vb), "da");
        return retning === "op" ? res : -res;
      });
      raekker.forEach(function (r) { krop.appendChild(r); });
    }

    th.addEventListener("click", sorter);
    th.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sorter(); }
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
