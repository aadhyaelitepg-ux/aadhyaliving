// Aadhya Living — site JS (no dependencies)
(function () {
  // mobile menu
  var burger = document.querySelector(".hamburger");
  var menu = document.querySelector(".mobile-menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      menu.classList.toggle("open");
      burger.setAttribute("aria-expanded", menu.classList.contains("open"));
    });
    // close the menu after tapping any link inside it (incl. same-page #anchors)
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      });
    });
  }

  // property filter (home page)
  var filters = document.querySelectorAll(".filter-row button");
  filters.forEach(function (b) {
    b.addEventListener("click", function () {
      filters.forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      var f = b.dataset.filter;
      document.querySelectorAll(".prop-card").forEach(function (c) {
        c.classList.toggle("hide", f !== "all" && c.dataset.type !== f);
      });
      document.querySelectorAll(".area-group").forEach(function (g) {
        var visible = g.querySelectorAll(".prop-card:not(.hide)").length;
        g.classList.toggle("hide", visible === 0);
      });
    });
  });

  // enquiry form -> opens WhatsApp with a pre-filled message (no backend needed)
  var form = document.getElementById("enquiry-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var wa = form.dataset.wa || "919888877789";
      var msg =
        "Hi Aadhya Living! I'm looking for a PG.\n" +
        "Name: " + (d.get("name") || "-") + "\n" +
        "Looking for: " + (d.get("type") || "-") + "\n" +
        "Preferred area: " + (d.get("area") || "-") + "\n" +
        "Move-in: " + (d.get("movein") || "Flexible") + "\n" +
        "Please share availability and pricing options.";
      window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(msg), "_blank");
    });
  }
})();
