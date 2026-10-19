/* Koridor — suivi des clics.
 * Complète la mesure d'audience Umami (visites et pages vues, sans cookie) par des
 * événements nommés « Catégorie · détail ». Le script de collecte (scripts/audience.py)
 * regroupe ces événements par catégorie pour le rapport du lundi.
 * N'envoie rien si Umami n'est pas chargé (site local, bloqueur, mesure désactivée).
 */
(function () {
  var MAX = 50; // longueur maximale d'un nom d'événement chez Umami

  function send(cat, detail, data) {
    var name = (cat + " · " + String(detail || "")).slice(0, MAX);
    try { if (window.umami && typeof window.umami.track === "function") window.umami.track(name, data || {}); } catch (_) {}
  }

  function project() {
    var m = location.pathname.match(/\/(?:projets|projects)\/([a-z0-9-]+)/);
    return m ? m[1] : "";
  }

  // Zone de la page d'où part un clic interne, pour savoir quel module attire.
  var ZONES = [
    [".une-main", "À la une"], [".moved-list", "Ce qui a bougé"], [".amounts", "Montants"],
    ["#cards", "Liste des projets"], [".related", "Même secteur"], [".brief-band, .panel-ink", "Bandeau Brief"],
    [".timeline", "Chronologie"], ["header.top", "Menu"], ["footer.foot", "Pied de page"]
  ];
  function zoneOf(el) {
    for (var i = 0; i < ZONES.length; i++) if (el.closest(ZONES[i][0])) return ZONES[i][1];
    return "Autre";
  }

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href]");
    if (!a) return;
    var u;
    try { u = new URL(a.getAttribute("href"), location.href); } catch (_) { return; }
    if (u.hostname && u.hostname !== location.hostname) {
      // Lien sortant : en pratique, une source citée dans une fiche.
      send("Source", u.hostname.replace(/^www\./, ""), { projet: project(), url: u.href.slice(0, 200) });
      return;
    }
    if (a.classList.contains("lang")) { send("Langue", a.getAttribute("hreflang")); return; }
    var p = u.pathname.match(/\/(?:projets|projects)\/([a-z0-9-]+)/);
    if (p) { send("Clic fiche", zoneOf(a), { projet: p[1] }); return; }
    if (/\/brief\/?$/.test(u.pathname) && a.classList.contains("btn")) { send("Brief", "clic abonnement", { depuis: project() || location.pathname }); }
  }, true);

  // Inscription au Brief (quand le formulaire est branché).
  document.addEventListener("submit", function (ev) {
    if (ev.target.classList && ev.target.classList.contains("signup")) send("Brief", "inscription");
  }, true);

  // Filtres de la page d'accueil.
  document.addEventListener("click", function (ev) {
    var pill = ev.target.closest && ev.target.closest(".pill");
    if (pill) send("Filtre secteur", pill.dataset.sector || "tous");
    var land = ev.target.closest && ev.target.closest(".map .on");
    if (land) send("Carte", land.dataset.country);
  }, true);
  var sel = document.getElementById("country");
  if (sel) sel.addEventListener("change", function () { if (sel.value) send("Filtre pays", sel.value); });

  // Recherches : on garde le terme (sans donnée personnelle attendue) et on signale
  // celles qui ne donnent aucun résultat, utiles pour savoir quels projets ajouter.
  var q = document.getElementById("q"), timer;
  if (q) q.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      var term = (q.value || "").toLowerCase().trim();
      if (term.length < 3) return;
      var empty = document.getElementById("empty");
      send(empty && !empty.hidden ? "Recherche sans résultat" : "Recherche", term.slice(0, 30));
    }, 1200);
  });

  // Lecture complète d'une fiche projet : le visiteur atteint la chronologie des sources.
  var tl = document.querySelector(".timeline");
  if (tl && project() && "IntersectionObserver" in window) {
    var seen = false, io = new IntersectionObserver(function (entries) {
      if (!seen && entries[0].isIntersecting) { seen = true; send("Lecture complète", project()); io.disconnect(); }
    }, { threshold: 0.5 });
    io.observe(tl);
  }
})();
