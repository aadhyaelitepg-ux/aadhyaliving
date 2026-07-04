# Aadhya Living — new website: deploy & edit guide

## What's in this folder
- 21 ready-to-upload files: homepage, 11 property pages, safety, food, about,
  contact, reviews, 404, sitemap.xml, robots.txt, .htaccess
- `assets/` — optimized photos (78 MB → 3 MB), CSS, JS, your logos
- `build.py` — the generator. All property data (names, phones, maps links,
  coordinates, descriptions) lives at the top of this one file.

## How to deploy (any cPanel / GoDaddy / Hostinger static hosting)
1. Back up the current site (download the old public_html folder).
2. Delete the old files from public_html.
3. Upload EVERYTHING in this folder (including the hidden `.htaccess`) to public_html.
4. Visit https://aadhyaliving.in — done. Old URLs like /khajaguda.html
   automatically redirect to the new pages (SEO preserved).

If you use GitHub Pages instead: push this folder to the repo — note that
GitHub Pages ignores .htaccess, so old-URL redirects won't work there.
cPanel-style hosting is recommended.

## How to edit later
- Change a phone number, add a property, fix a typo in a description:
  edit the PROPERTIES list at the top of build.py, then run
  `python3 build.py` — every page regenerates consistently.
- Small text tweaks can also be made directly in the HTML files.

## After deploying — do these (15 minutes, big SEO impact)
1. Google Search Console: add the site, submit sitemap.xml.
2. On each Google Business Profile: set the Website field to that property's
   exact page (e.g. womens-pg-khajaguda.html) — not just the homepage.
3. Rename "Green Home Eco PG" listing to "Aadhya Men's PG - Janardhan Hills".
4. Create the Instagram account and send me the handle — I'll update the
   footer link (currently points to instagram.com generically).

## Placeholders that need YOUR content (marked in the site)
- Photos for 10 of 11 properties (see PHOTO-SHOTLIST.md)
- Instagram handle
- The 3 sample testimonials on the homepage — replace with 3 real Google
  review quotes (short ones) and the reviewer's first name
- Food menu is a representative sample — replace with your actual weekly menu
  in build.py (the `menu` list in build_food)
- Street addresses per property (currently area-level only) — send them and
  I'll add to pages + schema, which strengthens local SEO further

## Design system (v2 — "Corridor")
The site now uses a distinctive wayfinding/transit-map identity built around
your real strength: 11 homes strung along Hyderabad's IT corridor.
- Hero = an interactive "Aadhya Line" route map (tap a stop → that neighbourhood)
- Fonts: Sora (display) · Hanken Grotesk (body) · Space Mono (labels/data)
- All emoji replaced with a custom line-icon set
- Palette: midnight navy ink · amber route-line · blueprint paper
- The previous stylesheet is saved as assets/css/style.backup.css if you ever
  want to compare or revert.
All 21 pages regenerate from build.py exactly as before — nothing about
deployment changes.
