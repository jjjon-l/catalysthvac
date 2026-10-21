# Catalyst HVAC — Current Site Audit
_Audited 2026-10-20 · https://catalysthvac.com_

> **Read with the Build Doc.** Where this audit and the Build Doc disagree, the Build Doc wins. Specifically:
> - **Sitemap:** use the Build Doc's 21-page register (Architecture §C), not §7 below.
> - **Claims:** none of the following go on the site until Jerry confirms them in writing: 24/7 or emergency service, same-day service, free estimates, financing, guarantees, "Book Online", years in business, brands, license number, membership pricing.
> - **Competitor patterns that are out:** coupon or specials grids, badge strips, rotating sliders, and an "us vs. them" table that implies unverified claims (§8 below).
> - **CTAs:** use "Request Service" and "Call Catalyst".
> - **Phone number:** the (713) 244-5070 on the current site is still an *open fact* (Fact Sheet B-2).
> - **Brand values:** the logo-derived colors and the font pairing in §3 are a *proposal* for Global tokens, pending the approved logo files (Fact Sheet B-1).

## 1. Stack
| Item | Current |
|---|---|
| CMS | WordPress 7.1.3 |
| Theme | Hello Elementor 3.0.2 + child theme `catalyst` |
| Builder | Elementor 4.3.5 + Elementor Pro (Theme Builder header/footer, Forms) |
| Add-ons | Royal Elementor Addons, GTranslate, PDF Embedder, Site Kit by Google |
| Analytics | GA4 `G-SM7HZPLK1G` (via Site Kit) |
| Host | SiteGround |
| Services | Custom post type `all-services` (URLs `/all-services/<slug>/`) |
| Container width | 1366px (Kit), containers with 0 default padding |

## 2. Page inventory
| URL | Status | Notes |
|---|---|---|
| `/` (Home, ID 10) | 200 | No H1. Main stylesheet broken (see §4). |
| `/all-services/air-conditioning/` | 200 | ~900 words. Repair, Tune-Up, Install, Ductless, Air Handlers, Service Plan |
| `/all-services/heating/` | 200 | ~750 words. Repair, Tune-Up, Install, Furnace, Heat Pumps |
| `/all-services/indoor-air-quality/` | 200 | ~900 words. Testing, Filtration, Purification, Duct Cleaning, Coils, Humidity |
| `/all-services/attic-insulation/` | 200 | ~840 words. Has a stray "Heater Installation" section copied from Heating |
| `/all-services/hvac-services/` | 200 | Commercial/multifamily. Zoning, Ducts, Thermostats, Blown-in insulation |
| `/all-services/visit-catalyst-construction/` | 200 | **Duplicate of the Heating page** under the wrong title. Meant to link to the sister company |
| `/membership-plan/` (ID 1416) | 200 | Main plan page |
| `/hvac-membership-plan/` (ID 2036) | 200 | Orphan second version, not linked in nav. Duplicate content |
| `/contact-us/` (ID 12) | 200 | Elementor Pro form |
| `/hello-world/` | 200 | Default WP post, still published |
| About / Careers / Blog / Service-area pages | — | **Don't exist.** "About Us" and "Our Services" in the footer are `#anchors` on the home page. A "careers" link exists but has no page |

Nav: Home · Contact Us · Membership Plan (the services aren't in the main nav at all).

## 3. Brand: colors & fonts

### From the logo (sampled pixels)
| Token | Hex | Use |
|---|---|---|
| Navy (wordmark) | `#1B1B5C` | Primary dark, headings, footer |
| Royal blue (panel) | `#283A8A` | Primary brand, buttons/sections |
| Mid blue | `#203078` | Gradients, hover |
| Red (A/C & Heat band) | `#B51C20` | Accent, CTA, "Call now" / emergency |
| Silver / chrome | `#D8D8D8` → `#F8F8F8` | Borders, light surfaces |

### What the current site actually uses (CSS)
- Cyan `#33FFFF` / `#3FFFFF` (most-used color, 30+ hits). **Not in the logo, and it clashes with the navy and red.**
- Reds `#D95040`, `#B5332A`, `#A5281F` (close to the logo red, not the same)
- Dark `#222222`, grays `#8A8A8A`, `#EFEFEF`, `#E8E8E8`
- Elementor Global Colors were never set. They're still the defaults (`#6EC1E4`, `#54595F`, `#7A7A7A`, `#61CE70`), and that's why headings show up light blue right now.

### Fonts loaded
- **Noto Sans Anatolian Hieroglyphs**: the main body/heading font in the CSS (13 uses). Almost certainly picked by mistake. It's a hieroglyph font that falls back to Noto Sans for Latin letters.
- **Monoton**: retro display font (used for the "CUSTOMER" letter graphic)
- Roboto / Roboto Slab: Elementor defaults, still set as the global fonts
- Noto Sans

### Recommendation for the rebuild
- **Headings:** a bold, condensed sans that matches the logo's heavy wordmark, e.g. *Barlow Condensed 700/800*, *Oswald*, or *Saira Condensed*
- **Body:** *Inter* or *Barlow* 400/500
- **Palette:** Navy `#1B1B5C`, Royal `#283A8A`, Red `#B51C20` (CTA only), Ice/light `#F3F5FA`, Silver `#D8DBE2`, Text `#1E2230`. Drop the cyan.
- Set all of these in **Site Settings → Global Colors / Global Fonts** first, so every container references tokens.
- Host the fonts locally (Elementor → Settings → Performance "Load Google Fonts locally"), and make sure they load over https.

## 4. Critical issues (fix or avoid in the rebuild)
1. **The whole site is set to `noindex, nofollow`.** Every page returns `<meta name="robots" content="noindex, nofollow">`, so Google is told not to index it. That's almost certainly *Settings → Reading → "Discourage search engines"* left on. **This is the #1 reason the site gets no organic traffic.** Unchecking it on the live site is a one-click win that could happen today.
2. **The homepage design CSS returns 404 in browsers.** `/wp-content/uploads/elementor/css/post-10.css` 404s, so visitors see an unstyled page (plain stacked headings in default light blue). Fix: Elementor → Tools → Regenerate CSS & Data, then flush SiteGround's Dynamic Cache.
3. **Mixed content: fonts load over `http://`.** All 5 Google-font CSS files are requested over http and blocked by the browser. The WP Address/Site URL or Elementor's font cache has an `http://` URL in it. (SiteGround Security → HTTPS Enforce, plus Search & Replace `http://catalysthvac.com` → `https://`.)
4. **The child theme hardcodes an old dev-server IP**, `http://104.248.230.237/wp-content/uploads/2024/06/unnamed-file.png`, so those decorations break.
5. **No sitemap.** Both `/sitemap_index.xml` and `/wp-sitemap.xml` 404. No SEO plugin is installed (no meta descriptions, no Open Graph tags).
6. **No H1 on any page.** Every heading is an H2, including paragraphs that were styled as H2s.
7. **The phone number isn't clickable.** There are zero `tel:` links anywhere. (713) 244-5070 is only in the footer as plain text, and there's no phone in the header. That's a big mobile conversion loss for HVAC.
8. **No structured data.** There's no LocalBusiness/HVACBusiness schema.
9. **No TACLA license number on the site.** Texas requires HVAC contractors to show the TACLA license # on advertising, including the website. The TDLR notice is there, but not the license number. Get it from the client.
10. **Duplicate or junk content:** "Visit catalyst construction" is a clone of Heating, there's a second membership page, the Hello World post is live, and a "Heater Installation" block sits on the Attic Insulation page.
11. **No trust proof:** no reviews, ratings, Google review widget, brand/manufacturer logos, warranties, or license badges. Financing says "COMING SOON" (it mentions GreenSky, and a GoodLeap logo is in the media library).
12. **Typos and quality:** "hEATER rEPAIR" (caps-lock), "inaccurate thermoset", "Afterall", the Instagram handle `catalystcontstruction`. "25 years" on Home vs "50+ years" on HVAC Services.
13. **Weak forms:** the contact form has "Full Name" *and* "Last Name", duplicated Yes/No questions, and no service-type or ZIP field. There's no "Request Service" destination (the header button text exists, but there's no booking flow).
14. **Accessibility:** 5 of 11 homepage images have no alt text. The "CUSTOMER" acrostic is built from single-letter H3s, which screen readers read as "c", "u", "s"…
15. **GTranslate** adds a floating EN flag. Keep it only if Spanish is a real need, and then do proper `/es/` pages.

## 5. Content worth keeping (rewrite and tighten, don't discard)
- Origin story: 25+ yrs construction background (sister company Catalyst Construction), launched early 2024
- Mission: customer-first, fair and competitive pricing
- Team claims: full-time W-2 techs, background-checked, insured, certified, **never subcontract**
- "CUSTOMER FIRST" promise: Commitment to Excellence · Urgent Responsiveness · State-of-the-Art Equipment · Top Quality Techs · Options for Financing · Maintenance Plans · Emergency 24/7 · Risk-Free Price Guarantee. Good differentiators, but present them as an icon grid, not letters.
- Segments: **Residential · Multifamily · Commercial**. Multifamily is a real differentiator; most Houston competitors are residential-only.
- Service areas: Houston, Friendswood, Webster, Pasadena, Dickinson, Pearland, Seabrook, League City (Bay Area / south-east Houston)
- Membership plan copy (Houston humidity, storm season, heat; "$5–10k replacement" cost-avoidance angle)
- Full service copy on all 5 service pages (it just needs H1/H2/H3 structure and editing)

## 6. Media library (in use)
- `2024/06/Catalyst-HVAC-Logo-2.png` (512×319, transparent): primary logo. **Ask for an SVG or a larger master.** 512px is soft on retina headers.
- `2024/06/Catalyst-HVAC-Logo.png`, `2024/06/Catalyst-Construction-Logo1.png`
- `2024/06/good-leap.svg` (financing partner)
- `2024/06/services-happy-couple.jpg`, `2024/08/family-plan.jpg`, `2024/08/hvac-5.png`, `2024/08/hvac-below-hero.png`, `2024/09/new-map-scaled.jpg` (service-area map)
- Most imagery appears to be stock. Real photos of trucks, techs, and jobs will out-convert stock. Ask the client.

## 7. Proposed sitemap for the rebuild
```
Home
Services (hub)
  ├─ AC Repair · AC Installation & Replacement · AC Tune-Up · Ductless/Mini-Split
  ├─ Heating Repair · Heater/Furnace Installation · Heat Pumps
  ├─ Indoor Air Quality (Testing, Filtration, Purification, Duct Cleaning, Humidity)
  ├─ Ductwork (Repair/Replacement/Zoning) · Thermostats
  └─ Attic Insulation
Commercial & Multifamily HVAC   ← own landing page (differentiator)
Membership Plan
Financing
Service Areas (hub) → one page per city (8)
About (Story, Team, CUSTOMER FIRST promise, Catalyst Construction link)
Reviews
Careers
Contact / Request Service
Privacy Policy · Terms / SMS terms (the form already references an "Acceptable Use Policy")
```
Confirm the final page list against the client brief/SOP before building.

## 8. Competitor design research
Sites reviewed: **Abacus** (Houston), **Village Plumbing, Air & Electric** (Houston), **One Hour Heating & Air** (Houston local page and national site), **Reliant Heating & AC** (DFW, design reference), **Parker & Sons** (Phoenix), and **Service Experts** (national). John Moore blocked automated fetching, so it's not covered. Review it by hand.

| Site | What stands out | Idea to borrow |
|---|---|---|
| Abacus | Promo carousel hero, "24/7" in the utility bar, a strip of award badges, ServiceTitan online booking, VIP membership everywhere | "Day in the Life of a Technician" video with the CEO |
| Village | Hero lists every service plus "Houston, TX", 10,000+ Google reviews, **Partner Plan $80/yr shown with the price**, coupon grid, ~40 city pages, Podium chat | Plain-language promises ("cleanest techs": drop cloths, shoe covers) |
| One Hour | ZIP check plus "Book Now" hero, 4.82★ shown everywhere, sticky Call bar, 2-year satisfaction guarantee | **Named guarantee** ("On time or you don't pay"). Service page order: H1 "AC Repair in Houston, TX" → symptoms → services → 5-step "What to Expect" → financing → FAQ → reviews |
| Reliant | "Gimmick-free since 1983", techs **not on commission**, 4.9/5 shown under the CTA, "Hero Club from $22/mo" | A **"Other Guys vs. Us" comparison table** |
| Parker & Sons | Photo of a tech with a customer, "no extra charge nights/weekends", scheduler gets its own section | Community programs (teacher and senior giveaways) placed high on the page |
| Service Experts | Stats bar, shareable coupon cards, monthly leasing framed as "$155/mo" | Monthly-payment framing for system replacements |

### Patterns to adopt for Catalyst
1. **Sticky header**: logo, click-to-call (713) 244-5070, red **Book Online** button. On mobile, a sticky bottom bar with **Call / Book**.
2. **Navy utility bar**: 24/7 Emergency · Financing Available · TACLA license #.
3. **Hero**: a headline that names Houston, 2–3 proof bullets, Book plus Call buttons, and the star rating right under the CTA. **Real tech and truck photo**, not stock.
4. **Online booking**: embed the client's field-service software scheduler (ServiceTitan, Housecall Pro, etc.; *ask which they use*), with a short callback form as a fallback (name, phone, ZIP, service dropdown).
5. **Named guarantee**: turn the existing "Risk-Free Price Guarantee" into a specific, named promise.
6. **Compete as the honest new company**: a 2024 company can't win on "since 1946". Lean on full-time W-2 techs who never subcontract (already in the copy), upfront pricing, 25+ yrs of construction background, and a comparison table.
7. **Google reviews widget** (Elfsight, or Trustindex for free) plus named testimonials. Show the rating on every service page.
8. **Membership card shows the price** and benefits, and every page states the same discount.
9. **Specials grid**: tune-up price, $0 diagnostic with repair, military/first-responder/senior discounts.
10. **Financing band** on Home and on every install page ("from $X/mo", "See if you qualify"). Replace the "COMING SOON".
11. **One service page template** used for every service, in the One Hour order above, plus a local FAQ (with FAQ schema).
12. **Service-area pages** with real local content for Catalyst's actual South-East / Bay Area cities (Pearland, Friendswood, League City, Webster, Seabrook, Pasadena, Dickinson).
13. **Separate Residential / Multifamily / Commercial paths**. None of the competitors do this well, and it's Catalyst's clearest differentiator.
14. **Proof for a young company**: founder or tech video, badges (EPA 608, NATE if any, TDLR/TACLA, BBB, equipment brand dealer), and community involvement.

### Recommended homepage order
1. Utility bar + sticky header
2. Hero (headline, bullets, Book/Call, rating)
3. Trust strip (badges · license · guarantee · financing)
4. Service tiles (AC · Heating · Install/Replace · Maintenance · Air Quality · Insulation)
5. Residential / Multifamily / Commercial split
6. Why Catalyst (CUSTOMER FIRST icon grid + comparison table)
7. Specials
8. Reviews
9. Membership plan card
10. Financing band
11. Story / team video (Catalyst Construction heritage)
12. Book online / callback form
13. Service areas + map
14. Houston FAQ
15. Final CTA band → footer (name/address/phone, license, hours, socials, TDLR notice)

### Typography decision
Competitors mostly use Poppins/Montserrat with Inter. To match Catalyst's heavy, wide logo wordmark, use **Barlow Condensed 700 (headings) + Inter 400/500/600 (body)**. It's bolder and more "trade" than Poppins and still easy to read. Use red for CTAs and urgency only. Competitors use one warm accent color, and the logo red does that job here.
