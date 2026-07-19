#!/usr/bin/env python3
"""Aadhya Living site generator.
Edit PROPERTIES / copy below, run `python3 build.py` — all pages regenerate.
"""
import html, os

SITE = "https://aadhyaliving.in"
VER = "20260704d"
GA_ID = ""  # Set your Google Analytics Measurement ID here (e.g. "G-XXXXXXXXXX") to enable tracking across all pages
MAPS_ALL = "https://www.google.com/maps/search/Aadhya+Living+PG+Hyderabad"  # bump this string whenever you change CSS/JS to force browsers to reload
PH_MEN, PH_WOMEN, PH_COLIVE = "919888877789", "918345888999", "919888878899"

def utm(slug):  # tag for the Google Business Profile website button
    return f"?utm_source=gbp&utm_medium=organic&utm_campaign=listing&utm_content={slug}"

# ---- inline line-icon set (stroke, currentColor) — replaces all emoji ----
_P = {
 "peak":'<path d="M12 4 3 20h18z" fill="#ff9d00" stroke="none"/><path d="M12 9 8 20h8z" fill="#0b1e3b" stroke="none"/>',
 "pin":'<path d="M12 21s7-6.4 7-11a7 7 0 1 0-14 0c0 4.6 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
 "phone":'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>',
 "chat":'<path d="M21 12a8 8 0 0 1-11.5 7.2L4 20l1-4.5A8 8 0 1 1 21 12Z"/>',
 "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
 "meal":'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-2 0-3 2-3 5s1 4 3 4 3-1 3-4-1-5-3-5ZM17 12v9"/>',
 "wifi":'<path d="M5 12.5a10 10 0 0 1 14 0M8 16a5 5 0 0 1 8 0"/><circle cx="12" cy="19" r="1" fill="currentColor" stroke="none"/>',
 "broom":'<path d="M19 5 12 12M11 9l4 4-5 5H5v-2l1-1M6 18l-2 3"/>',
 "cctv":'<path d="M3 8l14-3 1 4-14 3zM4 12l2 5M17 9l3 1v4h-3M9 20h4"/>',
 "lock":'<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 "drop":'<path d="M12 3s6 6.5 6 10.5a6 6 0 0 1-12 0C6 9.5 12 3 12 3Z"/>',
 "bolt":'<path d="M13 3 5 13h5l-1 8 8-11h-5z"/>',
 "washer":'<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="13" r="4"/><path d="M8 6h.01M11 6h.01"/>',
 "fridge":'<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M6 10h12M10 6v2M10 13v3"/>',
 "bed":'<path d="M3 8v10M3 12h18v6M21 18v-4a3 3 0 0 0-3-3h-7v4M7 11a2 2 0 1 0 0-.01"/>',
 "parking":'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16V8h3a2.5 2.5 0 0 1 0 5h-3"/>',
 "person":'<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
 "shield":'<path d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>',
 "check":'<path d="M20 6 9 17l-5-5"/>',
 "camera":'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7l1.5-2.5h5L16 7"/><circle cx="12" cy="13" r="3.5"/>',
 "insta":'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/>',
 "home":'<path d="M4 11 12 4l8 7M6 10v9h12v-9"/>',
}
def ic(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{_P[name]}</svg>'

def disp(p): return f"+91 {p[2:7]} {p[7:]}"

LANDMARKS = {
    "gachibowli": ["Wipro Circle", "DLF Cybercity", "Amazon Development Centre", "Indian School of Business (ISB)", "Gachibowli Stadium", "AIG Hospitals"],
    "kondapur":   ["Kothaguda Junction", "Sarath City Capital Mall", "Botanical Garden", "Hitec City", "Kondapur main road"],
    "hitec":      ["Hitex Exhibition Centre", "Mindspace IT Park", "Cyber Towers", "Durgam Cheruvu Metro", "Inorbit Mall"],
    "khajaguda":  ["Financial District", "Wells Fargo & ICICI campuses", "Nanakramguda", "Lanco Hills", "Khajaguda Lake", "DLF Cybercity"],
    "telecom":    ["Telecom Nagar", "Wipro Circle", "DLF Cybercity", "Gachibowli Stadium", "Masjid Banda Road"],
    "ssgrand":    ["Hitec City", "Kothaguda Junction", "Whitefields", "Botanical Garden Metro"],
}

PROPERTIES = [
 dict(slug="mens-pg-gachibowli", name="Aadhya Men's PG – Gachibowli", short="Men's PG · Gachibowli",
      type="men", area="Gachibowli", lat=17.4376242, lng=78.3668396,
      maps="https://maps.app.goo.gl/veVdYQGvjMnqBzYY6", addr='5/6, 2-48, Old Mumbai Hwy, Telecom Nagar Extn, Gachibowli, Hyderabad, Telangana 500032', pin='500032', kw=['mens pg in gachibowli', 'boys hostel in gachibowli', 'pg near me', 'mens pg near financial district'], near=LANDMARKS["gachibowli"],
      blurb="A professionally managed men's PG in the heart of Gachibowli — minutes from Wipro Circle, DLF Cybercity and the Financial District shuttle routes. Ideal for working professionals who want a fuss-free, fully serviced stay close to office."),
 dict(slug="mens-pg-2-gachibowli", name="Aadhya Men's PG 2 – Gachibowli", short="Men's PG · Gachibowli",
      type="men", area="Gachibowli", lat=17.4408067, lng=78.3652679,
      maps="https://maps.app.goo.gl/uBhdcUQ2WvVe2PJ96", addr='Plot 77, Yash Suites, Hussain Rd, P Janardhan Reddy Nagar, Gachibowli, Hyderabad, Telangana 500032', pin='500032', kw=['mens pg in gachibowli', 'boys pg near me', 'pg for men gachibowli'], near=LANDMARKS["gachibowli"],
      blurb="Our second men's property in Gachibowli, on the northern side towards Kondapur — the same Aadhya food, housekeeping and management standards, with quick access to both Gachibowli and Hitec City offices."),
 dict(slug="mens-pg-janardhan-hills", name="Aadhya Men's PG – Janardhan Hills, Gachibowli", short="Men's PG · Janardhan Hills",
      type="men", area="Gachibowli", lat=17.4371875, lng=78.3679375,
      maps="https://maps.app.goo.gl/YSqqRCR5yq37BD6L8", addr='P Janardhan Reddy Nagar, Gachibowli, Hyderabad, Telangana 500081', pin='500081', kw=['mens pg in gachibowli', 'boys hostel janardhan hills', 'pg near me'], near=LANDMARKS["gachibowli"],
      blurb="Tucked into the quiet Janardhan Hills pocket of Gachibowli, this men's PG gives you a calmer street with the same unbeatable commute — Wipro Circle and DLF are minutes away."),
 dict(slug="womens-pg-gachibowli", name="Aadhya Women's PG – Gachibowli", short="Women's PG · Gachibowli",
      type="women", area="Gachibowli", lat=17.4385886, lng=78.366434,
      maps="https://maps.app.goo.gl/moR1MhmBwbwqUBLR9", addr='Babukhan Lane, P Janardhan Reddy Nagar, Gachibowli, Hyderabad, Telangana 500032', pin='500032', kw=['womens pg in gachibowli', 'ladies pg in gachibowli', 'girls hostel in gachibowli', 'ladies pg near me'], near=LANDMARKS["gachibowli"],
      blurb="A secure, well-run women's PG in central Gachibowli with CCTV coverage, controlled entry and an on-call warden — walking distance to major IT campuses and daily-needs markets."),
 dict(slug="womens-pg-telecom-nagar", name="Aadhya Women's PG – Telecom Nagar, Gachibowli", short="Women's PG · Telecom Nagar",
      type="women", area="Gachibowli", lat=17.4325156, lng=78.3678256,
      maps="https://maps.app.goo.gl/qnhbe2NzTHj5EWeN7", addr='Telecom Nagar Extn, Gachibowli, Hyderabad, Telangana 500032', pin='500032', kw=['womens pg in gachibowli', 'ladies pg near me', 'girls hostel telecom nagar'], near=LANDMARKS["telecom"],
      blurb="Located in Telecom Nagar, one of Gachibowli's most convenient residential pockets — a safe, homely option for women working across Gachibowli, DLF and the Financial District."),
 dict(slug="womens-pg-kondapur", name="Aadhya Women's PG – Kondapur", short="Women's PG · Kondapur",
      type="women", area="Kondapur", lat=17.4621736, lng=78.3657885,
      maps="https://maps.app.goo.gl/ZgdttPsAmonAMZqo7", addr='210, opposite MITRAS NEST, Prashanth Nagar Colony, Kondapur, Hyderabad, Telangana 500084', pin='500084', kw=['womens pg in kondapur', 'ladies pg in kondapur', 'girls hostel in kondapur', 'ladies pg near me'], near=LANDMARKS["kondapur"],
      blurb="A women's PG in Kondapur with easy reach to both Hitec City and Gachibowli — close to Kothaguda Junction, Sarath City Capital Mall and everyday conveniences."),
 dict(slug="coliving-pg-hitec-city", name="Aadhya Elite Co-Living PG – Hitec City, Madhapur", short="Co-Living · Hitec City",
      type="colive", area="Hitec City · Madhapur", lat=17.4636263, lng=78.3767311,
      maps="https://maps.app.goo.gl/4gXcf8VWvJgtYDVm6", addr='11,12, Plot no:10, Hitex Road, beside Dynamic Ryderz, Vinayaka Nagar, Khanammet, Hyderabad, Telangana 500084', pin='500084', kw=['co-living pg in khanammet', 'best co-living pg vinayaka nagar', 'ladies pg in khanammet', 'mens pg in khanammet'], near=LANDMARKS["hitec"],
      blurb="Aadhya Elite is our premium co-living property near Hitex, Madhapur — separate, secure floors in a managed community, minutes from Mindspace, Cyber Towers and Durgam Cheruvu Metro."),
 dict(slug="womens-pg-khajaguda", name="Aadhya Women's PG – Khajaguda", short="Women's PG · Khajaguda",
      type="women", area="Khajaguda", lat=17.4182977, lng=78.3799983,
      maps="https://maps.app.goo.gl/B8fKEMgd23xzFKoL8", addr='66/2, Prashant Hills, Manikonda, Hyderabad, Telangana 500033', pin='500033', kw=['ladies pg in khajaguda', 'girls hostel in khajaguda', 'womens pg in khajaguda', 'ladies pg near me', 'womens pg near me'], near=LANDMARKS["khajaguda"],
      photos=True, sister="womens-pg-prashant-hills",
      blurb="Our flagship women's property in Khajaguda — a purpose-run building minutes from the Financial District and Nanakramguda campuses, with full CCTV coverage, nutritious daily meals and housekeeping."),
 dict(slug="womens-pg-prashant-hills", name="Aadhya Women's PG – Prashant Hills, Khajaguda", short="Women's PG · Prashant Hills",
      type="women", area="Khajaguda", lat=17.4181553, lng=78.3799093,
      maps="https://maps.app.goo.gl/cyfsKpoG5f6v5D2h8", addr='Prashant Hills, Manikonda, Hyderabad, Telangana 500033', pin='500033', kw=['ladies pg in khajaguda', 'womens pg in prashant hills', 'girls hostel near financial district'], near=LANDMARKS["khajaguda"],
      sister="womens-pg-khajaguda",
      blurb="Directly opposite our flagship Khajaguda women's building, the Prashant Hills property offers the same management, food and safety standards — double the capacity in one of Hyderabad's fastest-growing neighbourhoods."),
 dict(slug="mens-pg-khajaguda", name="Aadhya Men's PG – Khajaguda", short="Men's PG · Khajaguda",
      type="men", area="Khajaguda", lat=17.419183, lng=78.379562,
      maps="https://maps.app.goo.gl/U742wPPCC1jnH7Kh9", addr='Road no 4, Plot no 284, Prashant Hills, Gachibowli, Rai Durg, Hyderabad, Telangana 500032', pin='500032', kw=['mens pg in khajaguda', 'boys hostel in khajaguda', 'pg near financial district'], near=LANDMARKS["khajaguda"],
      blurb="A men's PG in Khajaguda built for Financial District commuters — minutes from Wells Fargo, ICICI and the Nanakramguda tech corridor, with all meals and housekeeping included."),
 dict(slug="ss-grand-womens-pg-gachibowli", name="SS Grand Women's PG – by Aadhya Living", short="Women's PG · Gachibowli East",
      type="women", area="Gachibowli", lat=17.4428348, lng=78.385631,
      maps="https://maps.app.goo.gl/gWBhoxZ53h3TGMgdA", addr='Gachibowli, Hyderabad, Telangana 500032', pin='500032', kw=['womens pg in gachibowli', 'ladies pg near me', 'girls hostel gachibowli'], near=LANDMARKS["ssgrand"],
      blurb="SS Grand is a long-running women's hostel now part of the Aadhya Living family — located between Gachibowli and Hitec City with quick access to Kothaguda Junction and Whitefields offices."),
]

AMEN = [("meal","All meals included"),("wifi","High-speed Wi-Fi"),("broom","Daily housekeeping"),
        ("cctv","24×7 CCTV"),("lock","Secure entry"),("drop","Hot water"),
        ("bolt","Power backup"),("washer","Washing machine"),("fridge","Refrigerator"),
        ("bed","Furnished rooms"),("parking","Two-wheeler parking"),("person","On-site caretaker")]

TYPE_META = {"men":("Men's PG","badge-m",PH_MEN),
             "women":("Women's PG","badge-w",PH_WOMEN),
             "colive":("Co-Living","badge-c",PH_COLIVE)}

KJ = [f"assets/img/khajaguda/gallery{i}" for i in range(1,7)]

# ---------------------------------------------------------------- shared bits
def head(title, desc, path, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:image" content="{SITE}/assets/img/khajaguda/hero-building.jpg">
<meta name="theme-color" content="#1b438b">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={VER}">
{extra}
</head>
<body class="has-bar">
"""

def nav(active=""):
    links = [("index.html","Home"),("index.html#locations","Locations"),("safety.html","Safety"),
             ("food.html","Food"),("reviews.html","Reviews"),("about.html","About"),("contact.html","Contact"),("careers.html","Careers")]
    dl = "".join(f'<li><a href="{h}" class="{"active" if h==active else ""}">{t}</a></li>' for h,t in links)
    ml = "".join(f'<a href="{h}">{t}</a>' for h,t in links)
    return f"""<header class="site-header">
 <div class="container nav">
  <a class="logo" href="index.html" aria-label="Aadhya Living home"><img src="assets/logo/aadhya_logo.jpeg" alt="Aadhya Living" style="height:52px;max-height:56px;width:auto;border-radius:6px;object-fit:contain"></a>
  <ul class="nav-links">{dl}</ul>
  <a class="btn btn-amber btn-sm nav-cta" href="tel:+{PH_WOMEN}">{ic('phone')} {disp(PH_WOMEN)}</a>
  <button class="hamburger" aria-label="Open menu" aria-expanded="false"><span></span></button>
 </div>
 <nav class="mobile-menu container">{ml}
  <a class="btn btn-amber menu-call" href="tel:+{PH_WOMEN}" style="display:inline-flex">{ic('phone')} Call us</a>
 </nav>
</header>
"""

def footer():
    loc = "".join(f'<a href="{p["slug"]}.html">{p["short"]}</a>' for p in PROPERTIES[:7])
    loc2 = "".join(f'<a href="{p["slug"]}.html">{p["short"]}</a>' for p in PROPERTIES[7:])
    return f"""<footer>
 <div class="container foot-grid">
  <div class="foot-logo"><img src="assets/logo/aadhya_logo.jpeg" alt="Aadhya Living" style="height:48px;width:auto;border-radius:6px;object-fit:contain">
   <p style="font-size:.92rem">Professionally managed PGs & co-living across Hyderabad's IT corridor — Gachibowli, Kondapur, Hitec City & Khajaguda. A home for every budget.</p>
   <div class="socials">
    <a href="https://www.instagram.com/" aria-label="Instagram">{ic('insta','')}</a>
    <a href="https://wa.me/{PH_WOMEN}" aria-label="WhatsApp">{ic('chat','')}</a>
   </div>
  </div>
  <div><h4>Locations</h4>{loc}</div>
  <div><h4>More locations</h4>{loc2}</div>
  <div><h4>Contact</h4>
   <a href="tel:+{PH_MEN}">Men's PGs: {disp(PH_MEN)}</a>
   <a href="tel:+{PH_WOMEN}">Women's PGs: {disp(PH_WOMEN)}</a>
   <a href="tel:+{PH_COLIVE}">Co-Living: {disp(PH_COLIVE)}</a>
   <a href="safety.html">Safety at Aadhya</a>
   <a href="food.html">Food & kitchen</a>
  </div>
 </div>
 <div class="container foot-note"><span>© 2026 Aadhya Living, Hyderabad. All rights reserved.</span><span>Women's · Men's · Co-Living PGs</span></div>
</footer>
<a class="wa-float" href="https://wa.me/{PH_WOMEN}?text=Hi%20Aadhya%20Living!%20I%27m%20looking%20for%20a%20PG." aria-label="Chat on WhatsApp">{ic('chat','')}</a>
<script src="assets/js/main.js?v={VER}"></script>
</body></html>"""

def action_bar(call, wa, maps):
    return f"""<div class="action-bar">
 <a class="ab-home" href="index.html">{ic('home')}Home</a>
 <a class="ab-call" href="tel:+{call}">{ic('phone')}Call</a>
 <a class="ab-wa" href="https://wa.me/{wa}?text=Hi%20Aadhya%20Living!%20I%27m%20looking%20for%20a%20PG.">{ic('chat')}WhatsApp</a>
 <a class="ab-dir" href="{maps}" target="_blank" rel="noopener">{ic('pin')}Directions</a>
</div>"""

def action_bar_simple(call, wa):
    return f"""<div class="action-bar">
 <a class="ab-home" href="index.html">{ic('home')}Home</a>
 <a class="ab-call" href="tel:+{call}">{ic('phone')}Call</a>
 <a class="ab-wa" href="https://wa.me/{wa}?text=Hi%20Aadhya%20Living!%20I%27m%20looking%20for%20a%20PG.">{ic('chat')}WhatsApp</a>
</div>"""

def card(p):
    label, badge, phone = TYPE_META[p["type"]]
    if p.get("photos"):
        media = f'<img src="{KJ[0]}-sm.webp" alt="{html.escape(p["name"])} building" loading="lazy" width="640" height="427">'
    else:
        media = f'<div class="soon">{ic("camera","")}Photos coming soon</div>'
    near = " · ".join(p["near"][:3])
    return f"""<article class="card prop-card" data-type="{p['type']}">
 <a class="card-media" href="{p['slug']}.html" aria-label="{html.escape(p['name'])}">{media}
  <span class="badge {badge}">{label}</span></a>
 <div class="card-body">
  <h3><a href="{p['slug']}.html" style="color:inherit">{html.escape(p['name'])}</a></h3>
  <p class="card-near">{ic('pin','')}Near {near}</p>
  <div class="card-actions">
   <a class="btn btn-blue btn-sm" href="{p['slug']}.html">View</a>
   <a class="btn btn-wa btn-sm" href="https://wa.me/{phone}?text=Hi!%20Enquiring%20about%20{p['name'].replace(' ','%20')}">WhatsApp</a>
   <a class="btn btn-ghost btn-sm" href="tel:+{phone}">Call</a>
  </div>
 </div>
</article>"""

# ---------------------------------------------------------------- home page
def build_home():
    areas = {}
    order = ["Gachibowli","Kondapur","Hitec City · Madhapur","Khajaguda"]
    for p in PROPERTIES: areas.setdefault(p["area"], []).append(p)
    area_html = ""
    subs = {"Gachibowli":"The heart of the IT corridor — Wipro Circle, DLF, Amazon, ISB",
            "Kondapur":"Between Hitec City and Gachibowli — malls, metro, everything nearby",
            "Hitec City · Madhapur":"Mindspace, Cyber Towers, Hitex — premium co-living",
            "Khajaguda":"Financial District's neighbourhood — Wells Fargo, ICICI, Nanakramguda"}
    for a in order:
        plist = areas.get(a, [])
        cards = "".join(card(p) for p in plist)
        n = len(plist)
        area_html += f"""<div class="area-group"><span class="area-marker">{ic('peak','')}</span>
<div class="area-title">{a} <span class="stops">{n} {'stop' if n==1 else 'stops'}</span></div>
<div class="area-sub">{subs[a]}</div><div class="prop-grid">{cards}</div></div>"""

    faqs = [
     ("Do Aadhya PGs include food?", "Yes — breakfast, lunch and dinner are included at all our properties, cooked fresh in-house daily. See the <a href='food.html'>food page</a> for a sample menu."),
     ("What budgets do you accommodate?", "All of them. Across our 11 properties we offer everything from economical multi-sharing rooms to premium single occupancy. Tell us your budget on WhatsApp and we'll match you to the right room."),
     ("Is it safe for women?", "Safety is our first design principle: 24×7 CCTV, controlled entry, on-site caretakers and responsive management at every women's property. Read more on our <a href='safety.html'>safety page</a>."),
     ("How do I book a visit?", "Message us on WhatsApp or call the number for your preferred property — we'll arrange a visit the same day in most cases."),
     ("What is the notice period and are there hidden charges?", "We keep terms simple and transparent — everything is explained clearly before you move in. Ask us anything on WhatsApp before booking."),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><div class='a'>{a}</div></details>" for q,a in faqs)
    faq_ld = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                      % (q.replace('"','\\"'), a.replace('"','\\"').replace("<a href='food.html'>","").replace("<a href='safety.html'>","").replace("</a>",""))
                      for q,a in faqs)
    org_ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Organization","name":"Aadhya Living",
"url":"{SITE}","logo":"{SITE}/assets/img/al-logo-color.svg",
"description":"Professionally managed women's, men's and co-living PGs across Hyderabad's IT corridor.",
"telephone":"+{PH_WOMEN}","areaServed":"Hyderabad",
"sameAs":["https://www.instagram.com/"]}}
</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld}]}}</script>"""

    feats = [("meal","Fresh food, daily","Breakfast, lunch and dinner cooked in-house — a weekly menu you'll actually look forward to."),
             ("shield","Safety first","CCTV, controlled entry and on-site caretakers at every property. Parents, we built this for your peace of mind."),
             ("broom","Fully serviced","Housekeeping, laundry machines, hot water, Wi-Fi and power backup — all handled, always included."),
             ("home","Every budget","From economical sharing to premium singles across 11 properties — there's an Aadhya home at your price.")]
    feat_html = "".join(f'<div class="feat"><div class="ico">{ic(i,"")}</div><h3>{t}</h3><p>{d}</p></div>' for i,t,d in feats)

    revs = [("Stayed here for over a year — food is homely and the management actually responds. Felt like a second home.","Resident","Women's PG · Khajaguda"),
            ("Best part is the location. Five minutes to office, and everything is taken care of.","Resident","Men's PG · Gachibowli"),
            ("As a parent I visited before admission — the security and cleanliness convinced me immediately.","Parent of resident","Women's PG · Kondapur")]
    rev_html = "".join(f'<div class="rev"><div class="stars">★★★★★</div><p>“{t}”</p><div class="who">{w}</div><div class="where">{l}</div></div>' for t,w,l in revs)

    # route-map hero: 4 neighbourhood "stations" with live property counts
    stations = [("Gachibowli","Wipro · DLF · Amazon · ISB",6,"#locations"),
                ("Kondapur","Hitec City · Sarath City Mall",1,"womens-pg-kondapur.html"),
                ("Hitec City","Mindspace · Cyber Towers",1,"coliving-pg-hitec-city.html"),
                ("Khajaguda","Financial District · Nanakramguda",3,"womens-pg-khajaguda.html")]
    st_html = "".join(f"""<a class="station" href="{href}">
     <span class="peak">{ic('peak')}</span>
     <div class="s-info">
      <div class="s-name">{nm}</div>
      <div class="s-meta">{mt}</div>
     </div>
     <span class="s-count">{n} {'home' if n==1 else 'homes'}</span></a>""" for nm,mt,n,href in stations)

    body = f"""{nav('index.html')}
<section class="route-hero">
 <div class="container route-wrap">
  <div>
   <span class="eyebrow">Women's · Men's · Co-Living</span>
   <h1>A home on every stop of your <em>commute.</em></h1>
   <p>11 professionally managed PGs strung along Hyderabad's IT corridor. Wherever you work, there's an Aadhya minutes away — with fresh food, real safety, and a room for every budget.</p>
   <div class="hero-actions">
    <a class="btn btn-amber" href="https://wa.me/{PH_WOMEN}?text=Hi%20Aadhya%20Living!%20I%27m%20looking%20for%20a%20PG.">{ic('chat')} WhatsApp us</a>
    <a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="#locations">Explore the map {ic('arrow')}</a>
   </div>
   <div class="hero-metrics">
    <div class="m"><b>11</b><span>Properties</span></div>
    <div class="m"><b>4</b><span>Neighbourhoods</span></div>
    <div class="m"><b>1500+</b><span>Beds in Hyderabad</span></div>
    <div class="m"><b>24×7</b><span>CCTV secured</span></div>
   </div>
  </div>
  <div class="route-map">
   <div class="rm-head"><b>The Aadhya Line</b><span>HYD · IT CORRIDOR</span></div>
   <div class="line"><div class="track"></div>{st_html}</div>
   <div class="rm-foot">↑ tap a stop to see homes there</div>
  </div>
 </div>
</section>

<section id="locations">
 <div class="container">
  <span class="eyebrow">Find your neighbourhood</span>
  <h2>11 homes along the IT corridor</h2>
  <p class="lead mt-2">Every Aadhya property sits minutes from a major office cluster. Pick your area, pick your type, and message us — we'll match a room to your budget.</p>
  <div class="filter-row" role="group" aria-label="Filter properties">
   <button class="on" data-filter="all">All</button>
   <button data-filter="women">Women's</button>
   <button data-filter="men">Men's</button>
   <button data-filter="colive">Co-Living</button>
  </div>
  <div class="corridor mt-3">{area_html}</div>
 </div>
</section>

<section style="padding-top:0">
 <div class="container">
  <span class="eyebrow">Why Aadhya</span>
  <h2>Run like a brand, feels like a home</h2>
  <div class="feat-grid">{feat_html}</div>
 </div>
</section>

<section style="padding-top:0">
 <div class="container"><div class="band">
  <div><h2>Every budget has a home here.</h2>
   <p>We don't publish one price because we don't have one product — economical sharing, comfortable doubles, premium singles. Tell us what you can spend; we'll show you what it gets.</p></div>
  <div class="btn-row">
   <a class="btn btn-amber" href="https://wa.me/{PH_WOMEN}?text=Hi!%20My%20budget%20is%20____%20—%20what%20rooms%20do%20you%20have%3F">{ic("chat")} Share your budget</a>
   <a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="contact.html">Book a visit</a>
  </div>
 </div></div>
</section>

<section style="padding-top:0">
 <div class="container split">
  <div>
   <span class="eyebrow">For parents, especially</span>
   <h2>Safety isn't a feature. It's the foundation.</h2>
   <ul class="ticks">
    <li>{ic("check","icon")}<span>24×7 CCTV coverage in common areas and entrances</span></li>
    <li>{ic("check","icon")}<span>Controlled entry and visitor policy at every property</span></li>
    <li>{ic("check","icon")}<span>On-site caretakers and responsive management</span></li>
    <li>{ic("check","icon")}<span>Well-lit surroundings in established residential pockets</span></li>
   </ul>
   <a class="btn btn-blue mt-3" href="safety.html" style="margin-top:24px">How we keep residents safe</a>
  </div>
  <picture><source srcset="assets/img/khajaguda/gallery2.webp" type="image/webp">
  <img src="assets/img/khajaguda/gallery2.jpg" alt="Secure Aadhya Living residence" loading="lazy"></picture>
 </div>
</section>

<section style="padding-top:0">
 <div class="container">
  <span class="eyebrow">What residents say</span>
  <h2>Trusted on the ground. Now online too.</h2>
  <div class="rev-grid">{rev_html}</div>
  <p class="center mt-3"><a class="btn btn-ghost" href="reviews.html">Read reviews by location →</a></p>
 </div>
</section>

<section style="padding-top:0">
 <div class="container">
  <span class="eyebrow">Good to know</span>
  <h2 class="center">Questions everyone asks</h2>
  <div class="faq">{faq_html}</div>
 </div>
</section>
{action_bar(PH_WOMEN, PH_WOMEN, MAPS_ALL)}
{footer()}"""
    title = "Aadhya Living | Women's, Men's & Co-Living PG in Gachibowli, Kondapur, Hitec City & Khajaguda, Hyderabad"
    desc = "11 professionally managed PGs across Hyderabad's IT corridor. All meals, CCTV security, housekeeping included — rooms for every budget. WhatsApp us to book a visit."
    return head(title, desc, "", org_ld) + body

# ---------------------------------------------------------------- property page
def build_property(p):
    label, badge, phone = TYPE_META[p["type"]]
    wa = phone
    if p.get("photos"):
        gal = "".join(f"""<a href="{b}.jpg" target="_blank" rel="noopener"><picture>
<source srcset="{b}.webp" type="image/webp"><img src="{b}.jpg" alt="{html.escape(p['name'])} — photo {i+1}" loading="lazy"></picture></a>""" for i,b in enumerate(KJ))
    else:
        gal = ('<div class="g-soon">📸 Real photos of this property<br>coming soon</div>'*3 +
               '<a href="womens-pg-khajaguda.html" class="g-soon" style="border-style:solid">See our Khajaguda flagship →</a>')
    near = "".join(f"<li>{ic('pin','')}{n}</li>" for n in p["near"])
    amen = "".join(f'<div class="amen">{ic(i)}{t}</div>' for i,t in AMEN)
    sister = ""
    if p.get("sister"):
        s = next(x for x in PROPERTIES if x["slug"]==p["sister"])
        sister = f'<div class="sister">{ic("home")} <strong>Sister property directly opposite:</strong> <a href="{s["slug"]}.html">{html.escape(s["name"])}</a> — same management, same standards, double the availability.</div>'
    others = [x for x in PROPERTIES if x["slug"]!=p["slug"] and x["area"]==p["area"]][:3]
    others_html = "".join(card(x) for x in others)
    others_sec = f"""<section style="padding-top:0"><div class="container">
<h2>More Aadhya homes in {p['area']}</h2><div class="prop-grid mt-3">{others_html}</div></div></section>""" if others else ""

    ld = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LodgingBusiness",
"name":"{p['name']}","url":"{SITE}/{p['slug']}.html",
"image":"{SITE}/assets/img/khajaguda/hero-building.jpg",
"telephone":"+{phone}",
"address":{{"@type":"PostalAddress","streetAddress":"{html.escape(p.get('addr',''))}","addressLocality":"{p['area'].split(' ·')[0]}","addressRegion":"Telangana","postalCode":"{p.get('pin','')}","addressCountry":"IN"}},
"geo":{{"@type":"GeoCoordinates","latitude":{p['lat']},"longitude":{p['lng']}}},
"hasMap":"{p['maps']}",
"parentOrganization":{{"@type":"Organization","name":"Aadhya Living","url":"{SITE}"}},
"amenityFeature":[{{"@type":"LocationFeatureSpecification","name":"Meals included"}},{{"@type":"LocationFeatureSpecification","name":"Wi-Fi"}},{{"@type":"LocationFeatureSpecification","name":"CCTV security"}},{{"@type":"LocationFeatureSpecification","name":"Housekeeping"}}]}}
</script>"""

    body = f"""{nav()}
<div class="prop-hero">
 <div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / <a href="index.html#locations">Locations</a> / {p['area']}</div>
  <h1>{html.escape(p['name'])}</h1>
  <div class="meta"><span class="chip">{label}</span><span class="chip">All meals included</span><span class="chip">24×7 CCTV</span></div>
  <div class="actions">
   <a class="btn btn-wa" href="https://wa.me/{wa}?text=Hi!%20Enquiring%20about%20{p['name'].replace(' ','%20').replace("'","%27")}.%20Please%20share%20room%20options.">{ic("chat")} WhatsApp</a>
   <a class="btn btn-amber" href="tel:+{phone}">{ic("phone")} {disp(phone)}</a>
   <a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="{p['maps']}" target="_blank" rel="noopener">{ic("pin")} Directions</a>
  </div>
 </div>
</div>

<section><div class="container">
 <p class="lead">{p['blurb']}</p>
 <p style="color:var(--ink-faint);font-size:.9rem;margin-top:12px;display:flex;gap:7px;align-items:center">{ic("pin","icon")} {html.escape(p.get("addr",""))}</p>
 <div class="sister" style="background:var(--teal-tint);border-color:#bfe3e2">{ic("person")} <strong>Visitors welcome — come see a room today.</strong> Most families decide after a quick visit. Walk in, or WhatsApp us and we'll keep a room ready to show you.</div>
 {sister}
 <h2 class="mt-3" style="margin-top:44px">Photos</h2>
 <div class="gallery mt-2">{gal}</div>

 <h2 style="margin-top:56px">What's included</h2>
 <div class="amen-grid">{amen}</div>

 <div class="grid-2" style="margin-top:56px">
  <div>
   <h2>What's nearby</h2>
   <ul class="near-list">{near}</ul>
   <h2 style="margin-top:44px">On the map</h2>
   <div class="map-wrap"><iframe title="Map: {html.escape(p['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
     src="https://maps.google.com/maps?q={p['lat']},{p['lng']}&z=16&output=embed"></iframe></div>
   <p style="margin-top:14px"><a class="btn btn-blue" href="{p['maps']}" target="_blank" rel="noopener">Open in Google Maps →</a></p>
  </div>
  <div>
   <h2>Enquire now</h2>
   <p class="lead" style="margin:10px 0 18px;font-size:.98rem">Fill this in — it opens WhatsApp with your details ready to send. We usually reply within minutes.</p>
   <form class="enq" id="enquiry-form" data-wa="{wa}">
    <label for="f-name">Your name</label>
    <input id="f-name" name="name" required placeholder="e.g. Priya">
    <input type="hidden" name="type" value="{label} — {p['area']}">
    <input type="hidden" name="area" value="{html.escape(p['name'])}">
    <label for="f-move">Move-in (roughly)</label>
    <select id="f-move" name="movein"><option>This week</option><option>Within 2 weeks</option><option>This month</option><option>Just exploring</option></select>
    <button class="btn btn-wa" type="submit">{ic("chat")} Send on WhatsApp</button>
    <p class="fine">Prefer to talk? Call <a href="tel:+{phone}">{disp(phone)}</a></p>
   </form>
  </div>
 </div>
</div></section>
{others_sec}
{action_bar(phone, wa, p['maps'])}
{footer()}"""
    kw = p.get('kw', [])
    primary = kw[0] if kw else f"{label.lower()} in {p['area']}"
    title = f"{primary.title()} | {p['name']} — Aadhya Living Hyderabad"
    desc = f"{p['name']}: {primary} with all meals, Wi-Fi, housekeeping & 24×7 CCTV included. Near {', '.join(p['near'][:3])}. Call {disp(phone)} or WhatsApp to visit today."
    return head(title, desc, f"{p['slug']}.html", ld) + body

# ---------------------------------------------------------------- simple pages
def simple(title, desc, path, hero_h1, hero_p, inner):
    page_label = path.replace('.html','').replace('-',' ').title()
    if path == "careers.html" or path == "GoogleAI_Job_Roles.html":
        page_label = "Careers"
    crumb = f'<div class="crumbs" style="margin-bottom:14px;color:rgba(255,255,255,.7);font-size:.9rem"><a href="index.html" style="color:var(--amber);font-weight:600">← Home</a> / {page_label}</div>'
    home_band = f"""<section style="padding-top:0"><div class="container"><div class="band">
 <div><h2>Looking for a room along the IT corridor?</h2><p>Explore all 11 Aadhya homes in Gachibowli, Kondapur, Hitec City & Khajaguda — with fresh food, safety, and rooms for every budget.</p></div>
 <div class="btn-row"><a class="btn btn-amber" href="index.html#locations">{ic("home")} Explore All 11 Locations</a></div>
</div></div></section>"""
    body = f"""{nav(path)}
<div class="page-hero"><div class="container">{crumb}<h1>{hero_h1}</h1><p>{hero_p}</p></div></div>
{inner}
{home_band}
{action_bar_simple(PH_WOMEN, PH_WOMEN)}
{footer()}"""
    return head(title, desc, path) + body

def build_safety():
    inner = f"""<section><div class="container split">
 <div>
  <span class="eyebrow">Our first design principle</span>
  <h2>What "safe" actually means at Aadhya</h2>
  <ul class="ticks">
   <li>{ic("check","icon")}<span><strong>24×7 CCTV</strong> at entrances and common areas, at every property</span></li>
   <li>{ic("check","icon")}<span><strong>Controlled entry</strong> — visitors don't walk in unannounced</span></li>
   <li>{ic("check","icon")}<span><strong>On-site caretaker</strong> at each building, with escalation to central management</span></li>
   <li>{ic("check","icon")}<span><strong>Established residential streets</strong> — our buildings are in lived-in, well-lit neighbourhoods, not isolated plots</span></li>
   <li>{ic("check","icon")}<span><strong>Separate, secure floors</strong> at our co-living property</span></li>
   <li>{ic("check","icon")}<span><strong>Responsive management</strong> — one WhatsApp message reaches people who can act</span></li>
  </ul>
 </div>
 <picture><source srcset="assets/img/khajaguda/banner2.webp" type="image/webp">
 <img src="assets/img/khajaguda/banner2.jpg" alt="Aadhya Living secure residence building"></picture>
</div></section>
<section style="padding-top:0"><div class="container"><div class="band">
 <div><h2>Parents: visit us first.</h2><p>Before your daughter or son moves in, come see the building, meet the caretaker, taste the food. We'll arrange a visit the same day in most cases.</p></div>
 <div class="btn-row"><a class="btn btn-amber" href="https://wa.me/{PH_WOMEN}?text=Hi!%20I%27m%20a%20parent%20and%20would%20like%20to%20visit%20a%20property.">{ic("chat")} Arrange a parent visit</a></div>
</div></div></section>"""
    return simple("Safety at Aadhya Living | CCTV, Secure Entry & On-site Caretakers","How Aadhya Living keeps residents safe: 24×7 CCTV, controlled entry, on-site caretakers and responsive management at every PG in Hyderabad.","safety.html","Safety isn't a feature here.","It's the reason parents choose us — and residents stay. Here's exactly what we do at every property.",inner)

def build_food():
    menu = [("Monday","Idli · chutney · sambar","Rice · dal · veg curry · curd","Roti · paneer curry · rice"),
            ("Tuesday","Poha · tea","Rice · sambar · fry · curd","Veg biryani · raita"),
            ("Wednesday","Dosa · chutney","Roti · rice · dal · veg","Fried rice · manchurian"),
            ("Thursday","Upma · banana","Rice · rasam · curry · curd","Roti · chana masala · rice"),
            ("Friday","Puri · aloo curry","Rice · dal · fry · buttermilk","Pulao · curry · sweet"),
            ("Saturday","Idli / vada mix","Special thali","Roti · veg curry · rice"),
            ("Sunday","Chapati · curry","Special lunch (chicken / paneer)","Light dinner · fruits")]
    rows = "".join(f"<tr><td><strong>{d}</strong></td><td>{b}</td><td>{l}</td><td>{n}</td></tr>" for d,b,l,n in menu)
    inner = f"""<section><div class="container">
 <span class="eyebrow">Cooked in-house, every day</span>
 <h2>A sample week at the Aadhya kitchen</h2>
 <p class="lead mt-2">All three meals are included at every property. Menus vary a little by location and season — this is a representative week. Special meals on Sundays and festivals.</p>
 <div class="menu-scroll"><table class="menu-table"><thead><tr><th>Day</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr></thead><tbody>{rows}</tbody></table></div>
 <p class="mt-3" style="color:var(--ink-soft)">Dietary preference or allergy? Tell us before you move in — we accommodate where we can.</p>
 <a class="btn btn-wa mt-2" href="https://wa.me/{PH_WOMEN}?text=Hi!%20Question%20about%20the%20food%20menu%20—">{ic("chat")} Ask about the menu</a>
</div></section>"""
    return simple("Food at Aadhya Living | All Meals Included at Every PG","Breakfast, lunch and dinner cooked fresh in-house daily at every Aadhya Living PG in Hyderabad. See a sample weekly menu.","food.html","Food you'll actually look forward to.","Three fresh meals a day, cooked in-house at every property — included, always.",inner)

def build_about():
    inner = f"""<section><div class="container split">
 <div>
  <span class="eyebrow">The Aadhya story</span>
  <h2>Built on the ground, one building at a time</h2>
  <p class="lead mt-2">Aadhya Living grew the old-fashioned way — by running good buildings well, and letting residents tell their friends. Today we manage <strong>11 properties across Gachibowli, Kondapur, Hitec City and Khajaguda</strong>: women's PGs, men's PGs and a premium co-living community.</p>
  <p class="lead mt-2">Every property runs on the same standards: fresh food cooked in-house, daily housekeeping, real security, and management that answers the phone. From economical sharing to premium singles, there's an Aadhya home for every budget.</p>
 </div>
 <picture><source srcset="assets/img/khajaguda/gallery1.webp" type="image/webp">
 <img src="assets/img/khajaguda/gallery1.jpg" alt="Aadhya Living flagship building, Khajaguda"></picture>
</div></section>
<section style="padding-top:0"><div class="container"><div class="band">
 <div><h2>Come see for yourself.</h2><p>The best way to know a PG is to walk through it. Message us — we'll set up a visit today.</p></div>
 <div class="btn-row"><a class="btn btn-amber" href="https://wa.me/{PH_WOMEN}?text=Hi!%20I%27d%20like%20to%20visit%20a%20property.">{ic("chat")} Book a visit</a></div>
</div></div></section>"""
    return simple("About Aadhya Living | Hyderabad's Trusted PG & Co-Living Brand","Aadhya Living runs 11 women's, men's and co-living PGs across Hyderabad's IT corridor — built on food, safety and management standards residents recommend.","about.html","A brand built by word of mouth.","11 properties. Three neighbourhoods' worth of residents who found us the same way: a friend said, 'stay at Aadhya.'",inner)

def build_contact():
    rows = "".join(f"""<article class="card"><div class="card-body">
<h3>{html.escape(p['name'])}</h3><p class="card-near">{p['area']}</p>
<div class="card-actions">
<a class="btn btn-blue btn-sm" href="tel:+{TYPE_META[p['type']][2]}">{ic("phone")} Call</a>
<a class="btn btn-wa btn-sm" href="https://wa.me/{TYPE_META[p['type']][2]}">{ic("chat")} WhatsApp</a>
<a class="btn btn-ghost btn-sm" href="{p['maps']}" target="_blank" rel="noopener">{ic("pin")} Map</a>
</div></div></article>""" for p in PROPERTIES)
    inner = f"""<section><div class="container">
 <div class="grid-2">
  <div>
   <h2>One number per need</h2>
   <ul class="ticks mt-2">
    <li>{ic("phone","icon")}<span><strong>Men's PGs:</strong>&nbsp;<a href="tel:+{PH_MEN}">{disp(PH_MEN)}</a></span></li>
    <li>{ic("phone","icon")}<span><strong>Women's PGs:</strong>&nbsp;<a href="tel:+{PH_WOMEN}">{disp(PH_WOMEN)}</a></span></li>
    <li>{ic("phone","icon")}<span><strong>Co-Living (Aadhya Elite):</strong>&nbsp;<a href="tel:+{PH_COLIVE}">{disp(PH_COLIVE)}</a></span></li>
   </ul>
   <h2 style="margin-top:44px">Or start on WhatsApp</h2>
   <form class="enq mt-2" id="enquiry-form" data-wa="{PH_WOMEN}">
    <label for="c-name">Your name</label><input id="c-name" name="name" required placeholder="e.g. Priya">
    <label for="c-type">Looking for</label>
    <select id="c-type" name="type"><option>Women's PG</option><option>Men's PG</option><option>Co-Living</option></select>
    <label for="c-area">Preferred area</label>
    <select id="c-area" name="area"><option>Gachibowli</option><option>Kondapur</option><option>Hitec City / Madhapur</option><option>Khajaguda</option><option>Flexible</option></select>
    <label for="c-move">Move-in (roughly)</label>
    <select id="c-move" name="movein"><option>This week</option><option>Within 2 weeks</option><option>This month</option><option>Just exploring</option></select>
    <button class="btn btn-wa" type="submit">{ic("chat")} Send on WhatsApp</button>
   </form>
  </div>
  <div><h2>Every property, one tap away</h2><div class="prop-grid mt-2" style="grid-template-columns:1fr">{rows}</div></div>
 </div>
</div></section>"""
    return simple("Contact Aadhya Living | Call or WhatsApp Any Property","Contact Aadhya Living PGs in Hyderabad. Men's PGs: +91 98888 77789 · Women's PGs: +91 83458 88999 · Co-Living: +91 98888 78899. WhatsApp for same-day visits.","contact.html","Talk to a human, today.","Call, WhatsApp, or send your details — we usually reply within minutes during the day.",inner)

def build_reviews():
    blocks = "".join(f"""<article class="card"><div class="card-body">
<h3>{html.escape(p['name'])}</h3><p class="card-near">{p['area']}</p>
<div class="card-actions">
<a class="btn btn-amber btn-sm" href="{p['maps']}" target="_blank" rel="noopener">★ Read Google reviews</a>
<a class="btn btn-ghost btn-sm" href="{p['slug']}.html">View property</a>
</div></div></article>""" for p in PROPERTIES)
    inner = f"""<section><div class="container">
 <span class="eyebrow">Verified, not curated</span>
 <h2>Read our reviews where we can't edit them</h2>
 <p class="lead mt-2">Every Aadhya property has its own Google listing with real reviews from real residents. Tap any property below — you'll see the ratings straight on Google Maps.</p>
 <div class="prop-grid mt-3">{blocks}</div>
</div></section>"""
    return simple("Aadhya Living Reviews | Real Google Ratings by Property","Read verified Google reviews for every Aadhya Living PG in Gachibowli, Kondapur, Hitec City and Khajaguda, Hyderabad.","reviews.html","Reviews we can't edit.","Every property links straight to its Google listing — read what residents actually say.",inner)

def build_careers():
    def apply_block(role):
        wa_text = f"Hi Venkat! I'm registering my interest for the {role} position."
        wa_url = f"https://wa.me/916304392325?text={html.escape(wa_text).replace(' ', '%20')}"
        return f"""
  <div class="apply-box" style="margin-top:32px;padding:24px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-sm)">
   <h3 style="font-size:1.15rem;font-weight:800;color:var(--ink);margin-bottom:4px">Fast Track Application Options</h3>
   <p style="font-size:0.9rem;color:var(--ink-soft);margin-bottom:20px">Choose how you'd like to apply directly via your hostel network:</p>
   
   <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:18px">
    <!-- Option 1: WhatsApp -->
    <div style="background:var(--surface);padding:20px;border-radius:12px;border:1px solid var(--line);display:flex;flex-direction:column;justify-content:space-between;box-shadow:var(--shadow)">
     <div>
      <span style="display:inline-block;font-size:0.75rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#1eb85a;margin-bottom:6px">Option 1</span>
      <h4 style="font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:4px">Register your interest</h4>
      <p style="font-size:0.86rem;color:var(--ink-soft);margin-bottom:16px;line-height:1.5">Send a direct WhatsApp message to register your profile.</p>
     </div>
     <a href="{wa_url}" target="_blank" rel="noopener" class="btn btn-wa" style="width:100%;justify-content:center;font-size:0.92rem;padding:12px 16px">
      <svg class="icon" viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.5 7.2L4 20l1-4.5A8 8 0 1 1 21 12Z"/></svg> Register on WhatsApp
     </a>
    </div>

    <!-- Option 2: Email CV -->
    <div style="background:var(--surface);padding:20px;border-radius:12px;border:1px solid var(--line);box-shadow:var(--shadow)">
     <span style="display:inline-block;font-size:0.75rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:var(--blue);margin-bottom:6px">Option 2</span>
     <h4 style="font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:4px">Send your CV</h4>
     <p style="font-size:0.86rem;color:var(--ink-soft);margin-bottom:14px;line-height:1.5">Select your CV file to submit via email.</p>
     
     <form onsubmit="handleCvEmail(event, '{role}')" style="display:flex;flex-direction:column;gap:12px">
      <div>
       <label style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:4px;color:var(--ink)">Your Name *</label>
       <input type="text" required class="cv-name" placeholder="e.g. Priya Sharma" style="width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:6px;font-size:0.88rem;background:var(--paper)">
      </div>
      <div>
       <label style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:4px;color:var(--ink)">Attach CV (PDF, DOC, DOCX) *</label>
       <input type="file" accept=".pdf,.doc,.docx" required class="cv-file" style="width:100%;font-size:0.82rem;color:var(--ink)">
      </div>
      <button type="submit" class="btn btn-amber" style="width:100%;justify-content:center;font-size:0.92rem;padding:12px 16px;margin-top:4px">
       <svg class="icon" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg> Send CV via Email
      </button>
     </form>
    </div>
   </div>
  </div>"""

    inner = f"""<section><div class="container" style="max-width:780px">
 <div class="filter-box" style="margin-bottom:30px;background:var(--surface);padding:24px;border-radius:var(--radius-sm);border:1px solid var(--line);box-shadow:var(--shadow)">
  <label for="experience" style="font-weight:700;display:block;margin-bottom:10px;color:var(--ink);font-size:1.05rem">Select your total IT work experience:</label>
  <select id="experience" onchange="showJob()" style="width:100%;padding:12px 16px;border-radius:8px;border:1px solid var(--line);font-size:1rem;font-family:var(--body);color:var(--ink);background:var(--paper);cursor:pointer">
   <option value="">-- Choose your experience level --</option>
   <option value="mid">3 to 5 Years</option>
   <option value="sr">5 to 9 Years</option>
   <option value="lead">10+ Years</option>
  </select>
 </div>

 <!-- ROLE 3: MID LEVEL -->
 <div id="job-mid" class="job-card" style="display:none;background:var(--surface);border-top:4px solid var(--blue);padding:30px;border-radius:var(--radius-sm);border-left:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line);box-shadow:var(--shadow);margin-top:25px">
  <span class="critical" style="background:#fee2e2;color:#dc2626;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;display:inline-block;margin-bottom:14px">🔥 High Priority Requirement (2 Openings)</span>
  <h2 class="job-title" style="margin-top:0;color:var(--ink);font-size:1.5rem;font-weight:800">AI Software Engineer (Mid-Level)</h2>
  <div class="meta-info" style="font-size:0.95rem;color:var(--ink-soft);margin-bottom:20px">📍 Hyderabad (Hybrid) &nbsp;|&nbsp; 💼 3–5 Years Experience</div>
  
  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Key Responsibilities</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Build robust production AI APIs and backend services.</li>
   <li>Integrate Gemini models and develop advanced AI workflows.</li>
   <li>Construct clean RAG pipelines and design detailed prompt templates.</li>
   <li>Build automated agent workflows and debug production AI systems.</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Required Technical Skills</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li><strong>Languages & Frameworks:</strong> Python, FastAPI, REST APIs, Git</li>
   <li><strong>Google Cloud Ecosystem:</strong> Vertex AI, Gemini API, Cloud Run, Docker</li>
   <li><strong>Core Competence:</strong> Prompt Engineering</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Good to Have</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Agent Development Kit (ADK), LangChain, LangGraph</li>
   <li>Vector databases, PostgreSQL, BigQuery, Vertex AI Search</li>
  </ul>
  
  {apply_block("AI Software Engineer (Mid-Level)")}
 </div>

 <!-- ROLE 2: SENIOR -->
 <div id="job-sr" class="job-card" style="display:none;background:var(--surface);border-top:4px solid var(--blue);padding:30px;border-radius:var(--radius-sm);border-left:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line);box-shadow:var(--shadow);margin-top:25px">
  <span class="critical" style="background:#fee2e2;color:#dc2626;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;display:inline-block;margin-bottom:14px">🔥 High Priority Requirement (2 Openings)</span>
  <h2 class="job-title" style="margin-top:0;color:var(--ink);font-size:1.5rem;font-weight:800">Senior AI Engineer (Google Cloud AI)</h2>
  <div class="meta-info" style="font-size:0.95rem;color:var(--ink-soft);margin-bottom:20px">📍 Hyderabad (Hybrid) &nbsp;|&nbsp; 💼 5–9 Years Experience</div>
  
  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Role Summary & Responsibilities</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Design and develop production-grade enterprise AI applications using Google Cloud AI services and Gemini technologies.</li>
   <li>Build sophisticated AI applications using Vertex AI and deploy smart AI agents via ADK.</li>
   <li>Build Gemini-powered enterprise assistants and orchestrate multi-format RAG applications.</li>
   <li>Integrate vital enterprise data sources and architect APIs for seamless internal AI services.</li>
   <li>Implement rigorous AI evaluation frameworks, optimize complex prompts, and manage secure production deployments while collaborating heavily with core architects.</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Required Technical Skills (Must Have)</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li><strong>Google Cloud AI:</strong> Vertex AI, Vertex AI Agent Builder, Gemini API, Gemini Enterprise</li>
   <li><strong>AI Engineering Specialized:</strong> ADK (Agent Development Kit), Prompt Engineering</li>
   <li><strong>Core Backend Systems:</strong> Python, FastAPI, Docker, Kubernetes, REST APIs</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Good Experience In</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li><strong>Orchestration & Tools:</strong> LangChain, LangGraph, LlamaIndex, MCP (Model Context Protocol)</li>
   <li><strong>Data Frameworks:</strong> Vector Search, Pinecone / Vertex Vector Search, BigQuery, Pub/Sub, Cloud Run</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Preferred Qualifications</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Google Cloud Professional Certifications</li>
   <li>Hands-on familiarity with MLOps, AI data evaluation, and overall system Observability</li>
  </ul>
  
  {apply_block("Senior AI Engineer (Google Cloud AI)")}
 </div>

 <!-- ROLE 1: LEAD -->
 <div id="job-lead" class="job-card" style="display:none;background:var(--surface);border-top:4px solid var(--blue);padding:30px;border-radius:var(--radius-sm);border-left:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line);box-shadow:var(--shadow);margin-top:25px">
  <h2 class="job-title" style="margin-top:0;color:var(--ink);font-size:1.5rem;font-weight:800">Lead AI Engineer / AI Technical Lead (Google Cloud AI)</h2>
  <div class="meta-info" style="font-size:0.95rem;color:var(--ink-soft);margin-bottom:20px">📍 Hyderabad (Hybrid) &nbsp;|&nbsp; 💼 10–15+ Years Experience (4+ in AI/ML & GenAI)</div>
  
  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">About the Role & Essential Functions</h3>
  <p style="margin-top:10px;line-height:1.7;color:var(--ink-soft)">This is a hands-on technical leadership role to design and deliver enterprise-scale Generative AI solutions using Google Cloud's AI ecosystem.</p>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Lead the overall architecture and high-scale deployment of corporate AI platforms.</li>
   <li>Design complex multi-agent systems via Gemini Enterprise and Gemini Enterprise Agents.</li>
   <li>Build intelligent AI assistants utilizing the Agent Development Kit (ADK) and deploy robust enterprise RAG architectures.</li>
   <li>Construct clean MCP-based integrations with crucial production systems.</li>
   <li>Implement dynamic AI orchestration workflows and design highly scalable Vertex AI deployments.</li>
   <li>Fine-tune foundation models, evaluate real-world performance, and build production AI microservices.</li>
   <li><strong>Enterprise System Integration:</strong> Connect core AI engines with backend environments like ERP, CRM, BPM, ServiceNow, Salesforce, and Pega.</li>
   <li>Provide close mentorship to engineering teams, outline strict coding standards/governance, and coordinate directly with stakeholders.</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Deep Technical Requirements</h3>
  
  <h4 style="margin-top:15px;margin-bottom:5px;color:var(--ink-soft);font-size:0.95rem;font-weight:700">Google Cloud AI & Gemini Ecosystem</h4>
  <ul style="padding-left:20px;margin-top:6px;line-height:1.7">
   <li>Vertex AI, Vertex AI Pipelines, Vertex AI Search, Vertex AI Agent Builder, Vertex AI Extensions, Vertex AI Model Garden, Vertex AI Evaluation, Vertex AI Prompt Management, Vertex AI Vector Search</li>
   <li>Gemini Enterprise, Gemini Enterprise Agents, Gemini API, Gemini 2.x models</li>
   <li>Prompt Engineering, Function Calling, Structured Outputs, Tool Calling</li>
  </ul>

  <h4 style="margin-top:15px;margin-bottom:5px;color:var(--ink-soft);font-size:0.95rem;font-weight:700">Agent Development & AI Architecture</h4>
  <ul style="padding-left:20px;margin-top:6px;line-height:1.7">
   <li>Agent Development Kit (ADK), Multi-Agent Systems, Agent orchestration, AI Planning, Memory management, Context management</li>
   <li>RAG, Hybrid Search, Vector Databases, Knowledge Graphs, Embeddings, Semantic Search</li>
  </ul>

  <h4 style="margin-top:15px;margin-bottom:5px;color:var(--ink-soft);font-size:0.95rem;font-weight:700">Google Cloud Platform (GCP) Core</h4>
  <ul style="padding-left:20px;margin-top:6px;line-height:1.7">
   <li>Cloud Run, GKE (Google Kubernetes Engine), Cloud Functions, Pub/Sub, BigQuery, Cloud Storage, Secret Manager, IAM</li>
  </ul>

  <h4 style="margin-top:15px;margin-bottom:5px;color:var(--ink-soft);font-size:0.95rem;font-weight:700">Programming, Frameworks & DevOps</h4>
  <ul style="padding-left:20px;margin-top:6px;line-height:1.7">
   <li>Python, FastAPI, Java, Go (preferred), REST APIs, gRPC</li>
   <li>LangChain, LangGraph, LlamaIndex, MCP (Model Context Protocol)</li>
   <li>Docker, Kubernetes, Terraform, GitHub Actions / Cloud Build</li>
  </ul>

  <h3 class="section-label" style="color:var(--ink);font-size:1.1rem;margin-top:25px;border-bottom:1px solid var(--line);padding-bottom:6px">Nice to Have</h3>
  <ul style="padding-left:20px;margin-top:10px;line-height:1.7">
   <li>Google Professional Machine Learning Engineer or Professional Cloud Architect certifications</li>
   <li>Proven background leading agile groups of 8–15 software engineers</li>
   <li>Strong foundation in enterprise AI governance</li>
  </ul>
  
  {apply_block("Lead AI Engineer (Google Cloud AI)")}
 </div>
</div></section>
<script>
function showJob() {{
  document.querySelectorAll('.job-card').forEach(function(card) {{ card.style.display = 'none'; }});
  var exp = document.getElementById('experience').value;
  if(exp) {{
    document.getElementById('job-' + exp).style.display = 'block';
  }}
}}

function handleCvEmail(e, role) {{
  e.preventDefault();
  var form = e.target;
  var nameInput = form.querySelector('.cv-name');
  var fileInput = form.querySelector('.cv-file');
  var candidateName = nameInput ? nameInput.value.trim() : 'Candidate';
  var fileName = (fileInput && fileInput.files && fileInput.files[0]) ? fileInput.files[0].name : '';
  
  var subject = encodeURIComponent("Aadhya Fast Track Application: " + role + " - " + candidateName);
  var bodyText = "Hi Venkat,\\n\\nI am applying for the " + role + " position via Aadhya Living Fast Track.\\n\\nApplicant Name: " + candidateName + "\\n" + (fileName ? "CV Attachment File: " + fileName + "\\n\\n" : "") + "Please find my attached CV.\\n\\nBest regards,\\n" + candidateName;
  var body = encodeURIComponent(bodyText);
  
  alert("Opening your email client to send your CV.\\n\\nPlease make sure your CV file (" + (fileName || "PDF/DOC") + ") is attached before sending!");
  
  window.location.href = "mailto:venkat.muddana@gmail.com?subject=" + subject + "&body=" + body;
}}
</script>"""
    return simple("Exclusive Tech Opportunities | Aadhya Living",
                  "Direct internal AI engineering opportunities via your Hostel Network for Aadhya Living residents.",
                  "careers.html",
                  "Exclusive Career Fast-Track",
                  "Direct internal opportunities via your Hostel Network",
                  inner)

def build_404():
    inner = f"""<section><div class="container center">
 <h2>That page moved — your new home didn't.</h2>
 <p class="lead mt-2" style="margin-left:auto;margin-right:auto">The page you're looking for isn't here. Head back home or jump straight to our locations.</p>
 <p class="mt-3"><a class="btn btn-amber" href="index.html">Go home</a> <a class="btn btn-ghost" href="index.html#locations">See locations</a></p>
</div></section>"""
    return simple("Page not found | Aadhya Living","Page not found — explore Aadhya Living PGs across Hyderabad.","404.html","Page not found","",inner)

# ---------------------------------------------------------------- infra files
def build_sitemap():
    pages = ["", "safety.html","food.html","about.html","contact.html","reviews.html","careers.html","GoogleAI_Job_Roles.html"] + [p["slug"]+".html" for p in PROPERTIES]
    urls = "".join(f"<url><loc>{SITE}/{p}</loc></url>" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'

HTACCESS = """# Aadhya Living — redirects from old site structure (SEO-preserving 301s)
RewriteEngine On
Redirect 301 /khajaguda.html /womens-pg-khajaguda.html
Redirect 301 /gachibowli.html /index.html
Redirect 301 /kondapur.html /womens-pg-kondapur.html
Redirect 301 /madhapur.html /coliving-pg-hitec-city.html
Redirect 301 /kphb.html /index.html
Redirect 301 /nanakramguda.html /mens-pg-khajaguda.html
Redirect 301 /blog.html /index.html
ErrorDocument 404 /404.html
# Compression + caching
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 30 days"
ExpiresByType image/jpeg "access plus 30 days"
ExpiresByType text/css "access plus 7 days"
ExpiresByType application/javascript "access plus 7 days"
</IfModule>
"""

ROBOTS = f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n"

def make_redirect_html(target_url):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target_url}">
<link rel="canonical" href="{SITE}/{target_url}">
<script>window.location.replace("{target_url}");</script>
<title>Redirecting to Aadhya Living...</title>
</head>
<body style="font-family:sans-serif;text-align:center;padding:50px">
<p>Redirecting to <a href="{target_url}">Aadhya Living</a>...</p>
</body>
</html>"""

# ---------------------------------------------------------------- run
OUT = os.path.dirname(os.path.abspath(__file__))
careers_content = build_careers()
pages = {"index.html": build_home(), "safety.html": build_safety(), "food.html": build_food(),
         "about.html": build_about(), "contact.html": build_contact(), "reviews.html": build_reviews(),
         "careers.html": careers_content, "GoogleAI_Job_Roles.html": careers_content,
         "404.html": build_404(), "sitemap.xml": build_sitemap(), ".htaccess": HTACCESS, "robots.txt": ROBOTS}

# Add HTML redirects for legacy URLs (works on Railway, Vercel, Netlify & GitHub Pages)
legacy_redirects = {
    "khajaguda.html": "womens-pg-khajaguda.html",
    "gachibowli.html": "index.html",
    "kondapur.html": "womens-pg-kondapur.html",
    "madhapur.html": "coliving-pg-hitec-city.html",
    "nanakramguda.html": "mens-pg-khajaguda.html",
    "kphb.html": "index.html",
    "blog.html": "index.html"
}
for old_page, new_target in legacy_redirects.items():
    pages[old_page] = make_redirect_html(new_target)

for p in PROPERTIES:
    pages[p["slug"] + ".html"] = build_property(p)
for name, content in pages.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
print(f"Built {len(pages)} files.")
