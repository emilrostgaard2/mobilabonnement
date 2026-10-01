/* telemobil.dk — adressetjek på bredbåndssiderne. Indlæses kun dér. */
/* Adressetjek på bredbåndssiderne.
   Data: Digitaliseringsstyrelsens Bredbåndskortlægning 2026, delt op pr.
   postnummer (/assets/adr/p/) og et vejnavne-indeks pr. to bogstaver
   (/assets/adr/v/). Alt hentes kun, når brugeren skriver. */
(function () {
  var felt = document.getElementById("adr-felt");
  if (!felt) return;
  var liste = document.getElementById("adr-forslag");
  var res = document.querySelector(".adr-resultat");
  var std = document.querySelector(".adr-standard");
  var knap = document.querySelector(".adr-knap");
  var hero = document.querySelector(".hero-adr");
  var fokus = hero ? hero.getAttribute("data-fokus") : "";
  var bb = [];
  try { bb = JSON.parse(document.getElementById("bb-data").textContent); } catch (e) {}
  var cache = {};
  var valgt = null; // {vej, p, k}
  var aktiv = -1;
  var forslag = [];

  function hent(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) { if (!r.ok) throw 0; return r.json(); });
    }
    return cache[url];
  }
  function noegle(s) {
    s = s.toLowerCase().replace(/æ/g, "ae").replace(/ø/g, "oe").replace(/å/g, "aa")
      .replace(/é/g, "e").replace(/ü/g, "u").replace(/ö/g, "oe").replace(/ä/g, "ae")
      .replace(/[^a-z0-9]/g, "");
    return (s.slice(0, 2) + "__").slice(0, 2);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function kr(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
  function naturlig(a, b) { return a.localeCompare(b, "da", { numeric: true }); }

  /* Skrivemaskine i feltet, så det er tydeligt, hvad man skal gøre */
  var eks = [];
  try { eks = JSON.parse(felt.getAttribute("data-eksempler")); } catch (e) {}
  var stop = false;
  function skriv(i, pos, slet) {
    if (stop || felt.value) { felt.setAttribute("placeholder", "Skriv din adresse"); return; }
    var t = eks[i % eks.length];
    if (!slet) {
      felt.setAttribute("placeholder", t.slice(0, pos + 1));
      if (pos + 1 < t.length) return setTimeout(function () { skriv(i, pos + 1, false); }, 65);
      return setTimeout(function () { skriv(i, t.length, true); }, 1500);
    }
    felt.setAttribute("placeholder", t.slice(0, pos - 1));
    if (pos - 1 > 0) return setTimeout(function () { skriv(i, pos - 1, true); }, 30);
    setTimeout(function () { skriv(i + 1, 0, false); }, 350);
  }
  if (eks.length) setTimeout(function () { skriv(0, 0, false); }, 500);
  felt.addEventListener("focus", function () { stop = true; felt.setAttribute("placeholder", "Fx Vestergade 5, 5000 Odense"); });

  function vis(items) {
    forslag = items; aktiv = -1;
    if (!items.length) { liste.hidden = true; felt.setAttribute("aria-expanded", "false"); return; }
    liste.innerHTML = items.map(function (x, i) {
      return '<li role="option" id="adr-o' + i + '" data-i="' + i + '">' + x.html + "</li>";
    }).join("");
    liste.hidden = false; felt.setAttribute("aria-expanded", "true");
  }
  function markér(i) {
    aktiv = i;
    liste.querySelectorAll("li").forEach(function (li, j) { li.classList.toggle("on", j === i); });
    felt.setAttribute("aria-activedescendant", i >= 0 ? "adr-o" + i : "");
  }

  function vejForslag(tekst) {
    var del = tekst.replace(/\s+\d.*$/, "").trim();
    if (del.length < 2) return vis([]);
    var pnr = (tekst.match(/\b(\d{4})\b/) || [])[1];
    hent("/assets/adr/v/" + noegle(del) + ".json").then(function (veje) {
      var l = del.toLowerCase(), ud = [];
      veje.forEach(function (v) {
        if (v[0].toLowerCase().indexOf(l) !== 0) return;
        v[1].forEach(function (pk) {
          if (pnr && pk[0] !== pnr) return;
          ud.push({ type: "vej", vej: v[0], p: pk[0], k: pk[1],
            html: "<b>" + esc(v[0]) + "</b> <span>" + pk[0] + " " + esc(pk[1]) + "</span>" });
        });
      });
      ud.sort(function (a, b) { return a.vej.length - b.vej.length || naturlig(a.vej, b.vej); });
      vis(ud.slice(0, 8));
    }).catch(fejl);
  }
  function fejl() {
    vis([]);
    res.innerHTML = '<div class="adr-kort"><p>Adressedata kunne ikke hentes lige nu. Prøv igen om lidt, eller brug ' +
      '<a href="https://tjekditnet.dk/" target="_blank" rel="noopener">tjekditnet.dk</a>.</p></div>';
    res.hidden = false;
  }
  function husForslag(tekst) {
    var rest = tekst.slice(valgt.vej.length).replace(/,.*$/, "").trim().toLowerCase();
    hent("/assets/adr/p/" + valgt.p + ".json").then(function (d) {
      var v = d.v.filter(function (x) { return x[0] === valgt.vej; })[0];
      if (!v) return vis([]);
      var hus = v[1].split(" ").map(function (h) { var i = h.lastIndexOf(":"); return [h.slice(0, i), +h.slice(i + 1)]; });
      hus.sort(function (a, b) { return naturlig(a[0], b[0]); });
      var ud = hus.filter(function (h) { return !rest || h[0].toLowerCase().indexOf(rest) === 0; })
        .slice(0, 8).map(function (h) {
          return { type: "hus", hus: h[0], prof: d.f[h[1]],
            html: "<b>" + esc(valgt.vej) + " " + esc(h[0]) + "</b> <span>" + valgt.p + " " + esc(valgt.k) + "</span>" };
        });
      vis(ud);
    }).catch(fejl);
  }
  function opdater() {
    var t = felt.value;
    if (valgt && t.indexOf(valgt.vej) === 0) return husForslag(t);
    valgt = null;
    vejForslag(t);
  }
  function vælg(x) {
    if (!x) return;
    if (x.type === "vej") {
      valgt = { vej: x.vej, p: x.p, k: x.k };
      felt.value = x.vej + " ";
      felt.focus();
      husForslag(felt.value);
    } else {
      felt.value = valgt.vej + " " + x.hus + ", " + valgt.p + " " + valgt.k;
      vis([]);
      resultat(x.prof);
    }
  }

  function kortHtml(lab, a) {
    return '<div class="vk"><span class="vk-lab">' + esc(lab) + "</span>" +
      '<img src="/assets/img/logoer/' + esc(a.s) + '.webp" alt="' + esc(a.u) + '" width="' + a.w + '" height="22">' +
      '<b class="vk-navn">' + ({ fiber: "Fiber", coax: "Kabel (coax)", "5g": "5G", "4g": "4G" }[a.t] || a.t) +
      " " + kr(a.n) + "/" + kr(a.o) + " Mbit/s</b>" +
      '<div class="vk-pris">' + kr(a.i || a.p) + "<span> kr./md." + (a.i ? " i " + a.m + " mdr." : "") + "</span></div>" +
      '<p class="vk-linje">' + (a.i ? "Herefter " + kr(a.p) + " kr. " : "Fast pris. ") + "Snit " + kr(a.a) + " kr./md. år 1.</p>" +
      '<a class="knap knap-primaer vk-knap" href="' + esc(a.l) + '" rel="sponsored nofollow noopener" target="_blank" data-udgaaende="' + esc(a.s) + '">Tjek hos ' + esc(a.u) + "</a></div>";
  }
  function billigst(t, maks) {
    var k = bb.filter(function (a) { return a.t === t && (!maks || a.n <= maks); });
    k.sort(function (a, b) { return a.a - b.a; });
    return k[0];
  }
  function resultat(f) {
    var fdl = f[0], ful = f[1], kdl = f[2], kul = f[3], xdl = f[4], mdl = f[5], mul = f[6], tdl = f[7];
    var rk = [
      ["Fiber", fdl, ful], ["Kabel-tv (coax)", kdl, kul], ["5G / mobilt bredbånd", mdl, mul],
      ["Kobber (xDSL)", xdl, 0], ["Fast trådløst", tdl, 0]
    ];
    var liste = rk.map(function (r) {
      var ok = r[1] > 0;
      return '<li class="' + (ok ? "ja" : "nej") + '"><span>' + r[0] + "</span><b>" +
        (ok ? "Op til " + kr(r[1]) + (r[2] ? "/" + kr(r[2]) : "") + " Mbit/s" : "Ikke udbudt") + "</b></li>";
    }).join("");
    var tek = [];
    if (fdl) tek.push(["fiber", "Billigste fibernet på adressen", fdl]);
    if (kdl) tek.push(["coax", "Billigste kabel-internet på adressen", kdl]);
    if (mdl) tek.push(["5g", "Billigste 5G-internet", 0]);
    if (fokus) tek.sort(function (a, b) { return (b[0] === fokus) - (a[0] === fokus); });
    var kort = tek.map(function (t) { var a = billigst(t[0], t[2]); return a ? kortHtml(t[1], a) : ""; })
      .filter(Boolean).slice(0, 3).join("");
    res.innerHTML = '<div class="adr-kort"><h2>Det kan du få på ' + esc(felt.value) + "</h2><ul>" + liste + "</ul>" +
      '<p class="adr-note">Kilde: Digitaliseringsstyrelsens Bredbåndskortlægning 2026 — hastigheder udbudt til private. ' +
      "Kortlægningen viser ikke, hvilke selskaber der leverer på adressen, så bekræft altid hos selskabet.</p>" +
      (liste2 ? '<a class="adr-hop" href="#sammenlign">Se alle tilbud på adressen</a>' : "") + "</div>" +
      (kort ? '<div class="seg-res on">' + kort + "</div>" : "");
    res.hidden = false;
    if (std) std.hidden = true;
    filtrerListe(f);
    if (typeof window.gtag === "function") window.gtag("event", "adressetjek", { fiber: fdl > 0, kabel: kdl > 0 });
  }

  /* Den store liste under hero'en følger adressen: kun det, der kan leveres */
  var liste2 = document.querySelector("[data-bb-liste]");
  var bjaelke = null;
  function kanLeveres(p, f) {
    var t = p.getAttribute("data-tek"), n = +p.getAttribute("data-ned");
    if (t === "fiber") return f[0] > 0 && n <= f[0];
    if (t === "coax") return f[2] > 0 && n <= f[2];
    if (t === "5g" || t === "4g") return f[5] > 0;
    if (t === "dsl") return f[4] > 0 && n <= f[4];
    return true;
  }
  function filtrerListe(f) {
    if (!liste2) return;
    window.tmAdrFilter = function (p) { return kanLeveres(p, f); };
    document.dispatchEvent(new CustomEvent("tm-adresse"));
    var alle = liste2.querySelectorAll("[data-bb-plan]").length;
    var match = Array.prototype.filter.call(liste2.querySelectorAll("[data-bb-plan]"),
      function (p) { return kanLeveres(p, f); }).length;
    if (!bjaelke) {
      bjaelke = document.createElement("div");
      bjaelke.className = "adr-bjaelke";
      var mål = liste2.querySelector(".planliste");
      mål.parentNode.insertBefore(bjaelke, mål);
    }
    bjaelke.innerHTML = '<span><b>' + match + " af " + alle + "</b> tilbud kan leveres på " + esc(felt.value) +
      '</span><button type="button" class="adr-ryd">Vis alle ' + alle + "</button>";
    bjaelke.hidden = false;
    bjaelke.querySelector(".adr-ryd").addEventListener("click", function () {
      window.tmAdrFilter = null; bjaelke.hidden = true;
      document.dispatchEvent(new CustomEvent("tm-adresse"));
    });
    var hop = res.querySelector(".adr-hop");
    if (hop) hop.textContent = "Se alle " + match + " tilbud på adressen";
  }

  felt.addEventListener("input", opdater);
  felt.addEventListener("keydown", function (e) {
    if (liste.hidden) { if (e.key === "Enter") { e.preventDefault(); opdater(); } return; }
    if (e.key === "ArrowDown") { e.preventDefault(); markér(Math.min(aktiv + 1, forslag.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); markér(Math.max(aktiv - 1, 0)); }
    else if (e.key === "Enter") { e.preventDefault(); vælg(forslag[aktiv >= 0 ? aktiv : 0]); }
    else if (e.key === "Escape") { vis([]); }
  });
  liste.addEventListener("mousedown", function (e) {
    var li = e.target.closest("li"); if (!li) return;
    e.preventDefault(); vælg(forslag[+li.getAttribute("data-i")]);
  });
  knap.addEventListener("click", function () {
    if (forslag.length) return vælg(forslag[0]);
    felt.focus(); opdater();
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".adr")) vis([]); });
})();
