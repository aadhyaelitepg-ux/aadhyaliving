/* Aadhya Living — shared interactions */
(function () {
"use strict";
var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
function $(s, c) { return (c || document).querySelector(s); }
function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

/* ---- Preloader (homepage only) ---- */
var loader = $("#loader");
if (loader) {
  window.addEventListener("load", function () {
    setTimeout(function () {
      loader.classList.add("done");
      document.body.classList.remove("loading");
      $$(".hero .reveal").forEach(function (el) { el.classList.add("in"); });
      animateTitle();
      setTimeout(function () { loader.remove(); }, 1100);
    }, reduced ? 100 : 1500);
  });
} else {
  document.body.classList.remove("loading");
}

/* ---- Hero headline word stagger (homepage) ---- */
var title = $("#heroTitle");
if (title) {
  (function split(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part.trim()) { frag.appendChild(document.createTextNode(part)); return; }
          var w = document.createElement("span"); w.className = "w";
          var i = document.createElement("i"); i.textContent = part;
          w.appendChild(i); frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1) split(n);
    });
  })(title);
}
function animateTitle() {
  if (!title) return;
  title.classList.add("in");
  $$(".w i", title).forEach(function (el, i) { el.style.transitionDelay = (0.15 + i * 0.06) + "s"; });
}

/* ---- Reveal on scroll ---- */
var io = new IntersectionObserver(function (entries) {
  entries.forEach(function (e) {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  });
}, { threshold: 0.12, rootMargin: "0px 0px -40px" });
$$(".reveal:not(.hero .reveal), .split-img, .station").forEach(function (el) { io.observe(el); });

/* ---- Counters ---- */
var cio = new IntersectionObserver(function (entries) {
  entries.forEach(function (e) {
    if (!e.isIntersecting) return;
    var el = e.target, end = +el.dataset.count, suf = el.dataset.suffix || "";
    var t0 = performance.now(), dur = 1600;
    (function tick(t) {
      var p = Math.min((t - t0) / dur, 1), ease = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(end * ease) + suf;
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
    cio.unobserve(el);
  });
}, { threshold: 0.6 });
$$("[data-count]").forEach(function (el) { cio.observe(el); });

/* ---- Header: scrolled state + hide on scroll down + progress ---- */
var header = $("#header"), lastY = 0, progress = $("#progress");
addEventListener("scroll", function () {
  var y = scrollY;
  if (header) {
    header.classList.toggle("scrolled", y > 60);
    var menuOpen = $("#mobileMenu") && $("#mobileMenu").classList.contains("open");
    header.classList.toggle("hidden", y > 500 && y > lastY && !menuOpen);
  }
  lastY = y;
  if (progress) {
    var h = document.documentElement;
    progress.style.width = (y / (h.scrollHeight - innerHeight) * 100) + "%";
  }
}, { passive: true });

/* ---- Mobile menu ---- */
var ham = $("#hamburger"), menu = $("#mobileMenu");
if (ham && menu) {
  ham.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    ham.classList.toggle("open", open);
    ham.setAttribute("aria-expanded", open);
    document.body.style.overflow = open ? "hidden" : "";
  });
  $$("a", menu).forEach(function (a) {
    a.addEventListener("click", function () {
      menu.classList.remove("open"); ham.classList.remove("open"); document.body.style.overflow = "";
    });
  });
}

/* ---- Property filters (homepage) ---- */
var note = $("#resultNote");
$$(".filter-row button").forEach(function (btn) {
  btn.addEventListener("click", function () {
    $$(".filter-row button").forEach(function (b) { b.classList.remove("on"); });
    btn.classList.add("on");
    var f = btn.dataset.filter, shown = 0;
    $$(".prop-card[data-type]").forEach(function (card) {
      var show = f === "all" || card.dataset.type === f;
      card.classList.toggle("hide", !show);
      card.classList.remove("pop"); void card.offsetWidth;
      if (show) { card.classList.add("pop"); shown++; }
    });
    if (note) note.textContent = f === "all" ? "Showing all 11 homes"
      : "Showing " + shown + " " + btn.textContent.trim() + " home" + (shown !== 1 ? "s" : "");
  });
});

/* ---- Pointer-driven niceties (desktop) ---- */
if (!reduced && matchMedia("(hover:hover) and (pointer:fine)").matches) {
  $$(".tilt").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      card.style.transform = "rotateY(" + (x * 7) + "deg) rotateX(" + (-y * 7) + "deg) translateY(-4px)";
    });
    card.addEventListener("mouseleave", function () { card.style.transform = ""; });
  });

  $$(".magnetic").forEach(function (btn) {
    btn.addEventListener("mousemove", function (e) {
      var r = btn.getBoundingClientRect();
      btn.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * .25) + "px," + ((e.clientY - r.top - r.height / 2) * .35) + "px)";
    });
    btn.addEventListener("mouseleave", function () { btn.style.transform = ""; });
  });

  var dot = $("#cursor"), ring = $("#cursorRing");
  if (dot && ring) {
    var mx = 0, my = 0, rx = 0, ry = 0;
    addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = "translate(" + (mx - 4) + "px," + (my - 4) + "px)";
    });
    (function loop() {
      rx += (mx - rx) * .14; ry += (my - ry) * .14;
      ring.style.transform = "translate(" + (rx - 19) + "px," + (ry - 19) + "px)";
      requestAnimationFrame(loop);
    })();
    $$("a, button, summary, select").forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("hot"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("hot"); });
    });
  }

  var heroImg = $("#heroImg"), hero = $(".hero");
  if (heroImg && hero) {
    hero.addEventListener("mousemove", function (e) {
      var x = (e.clientX / innerWidth - .5) * 18, y = (e.clientY / innerHeight - .5) * 12;
      heroImg.style.translate = (-x) + "px " + (-y) + "px";
    });
  }
}

/* ---- FAQ: close others ---- */
var faqs = $$(".faq details");
faqs.forEach(function (d) {
  d.addEventListener("toggle", function () {
    if (d.open) faqs.forEach(function (o) { if (o !== d) o.open = false; });
  });
});

/* ---- Seamless marquee loops ---- */
["marqueeTrack", "revTrack"].forEach(function (id) {
  var t = document.getElementById(id);
  if (t) t.innerHTML += t.innerHTML;
});

/* ---- Enquiry form → WhatsApp ---- */
var enq = $("#enquiry-form");
if (enq) {
  enq.addEventListener("submit", function (e) {
    e.preventDefault();
    var wa = enq.dataset.wa || "918345888999";
    var fd = new FormData(enq), lines = ["Hi Aadhya Living! New enquiry:"];
    if (fd.get("name")) lines.push("Name: " + fd.get("name"));
    if (fd.get("type")) lines.push("Looking for: " + fd.get("type"));
    if (fd.get("area")) lines.push("Property/Area: " + fd.get("area"));
    if (fd.get("movein")) lines.push("Move-in: " + fd.get("movein"));
    window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(lines.join("\n")), "_blank");
  });
}
})();

/* ---- Careers page helpers ---- */
function showJob() {
  var v = document.getElementById("experience").value;
  ["mid", "sr", "lead"].forEach(function (k) {
    var el = document.getElementById("job-" + k);
    if (el) el.style.display = (k === v) ? "block" : "none";
  });
  if (v) {
    var el = document.getElementById("job-" + v);
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}
function handleCvEmail(role) {
  var url = "https://wa.me/916304392325?text=" + encodeURIComponent(
    "Hi Venkat! I'd like to share my CV for the " + role + " position. Sending it here in the next message.");
  window.open(url, "_blank");
}
