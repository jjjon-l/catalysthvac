# Building the New Site in SiteGround Staging

**Decision (2026-11-19): the client wants staging.** We build in the SiteGround staging copy (`staging2.catalysthvac.com`) and push it to live at launch. The live site stays untouched until then.

## 0. Make staging reachable (one time)
1. **GoDaddy DNS** (DNS lives at GoDaddy, not SiteGround): Domains → catalysthvac.com → DNS → **Add New Record**:
   - Type **A**, Name **staging2**, Value **34.174.177.62**, TTL 1 hour
   - Change nothing else (Microsoft 365 email depends on the existing records).
2. Wait 5–30 minutes. Check it with `dig +short staging2.catalysthvac.com`, which should return the IP.
3. **SSL:** SiteGround Site Tools → Security → **SSL Manager** → issue Let's Encrypt for `staging2.catalysthvac.com` (if it isn't already listed).
4. **Lock it down:**
   - Site Tools → WordPress → Staging → ⋮ → **Password Protect** (share the login with Derrek).
   - In staging's WP admin: Settings → Reading → **Discourage search engines** stays ticked.
5. **Get in:** Site Tools → WordPress → Staging → ⋮ → **Log In Admin Panel**.

> The staging copy was cloned on 2026-10-20 from the old site. If the live site has changed since, delete it and create a fresh copy (Staging → Create) before building.

## 1. Global setup in staging (safe here: it's not live)
1. **Clean up:** set the old Theme Builder header and footer templates to Draft. Leave the old pages alone for now; they're replaced at launch.
2. **Site Settings → Global Colors / Global Fonts / Typography / Buttons:** enter the values from [03-design-system.md](03-design-system.md) (navy `#1B1B5C`, blue `#283A8A`, red `#B51C20`, Barlow Condensed + Inter, the type scale).
3. **Site Settings → Custom CSS:** paste [elementor/global.css](elementor/global.css). Every page gets it, so **no `CX – Styles` template is needed in staging.**
4. **Theme Builder → Header:** a full-width container with one HTML widget holding [elementor/out/cx-header.html](elementor/out/cx-header.html), with display condition **Entire Site**.
5. **Theme Builder → Footer:** the same, with [elementor/out/cx-footer.html](elementor/out/cx-footer.html) (includes the mobile Call/Request bar), condition **Entire Site**.
6. **Elementor → Settings → Performance:** turn on "Load Google Fonts locally". Then Tools → **Regenerate CSS & Data**.
7. **Plugins:** install Rank Math (SEO, sitemap, redirects), with **its Schema module turned off** (see SEO below).

## 2. Every page
1. Pages → Add New, with the real title and the real slug from the register (e.g. `ac-repair`). Page Layout: **Elementor Full Width**, so the Theme Builder header and footer show.
2. Build the sections (below), following that page's preview: `preview/<page>.html` locally, or on https://jjjon-l.github.io/catalysthvac/.
3. Add an **HTML widget** at the bottom with the page's schema from `elementor/out/seo/<page>.html`.
4. Rank Math: paste the title and meta from [elementor/out/seo-register.md](elementor/out/seo-register.md).
5. Publish. Publishing inside staging is fine, because the staging site itself is password-protected and noindexed.

## 3. Launch (Build Doc runbook)
1. Back up live.
2. Site Tools → WordPress → Staging → ⋮ → **Push to Live**. Choose **Custom Deploy** if live form submissions must be kept, otherwise Full Deploy.
3. On live:
   - untick "Discourage search engines"
   - Regenerate Elementor CSS and purge the SiteGround cache
   - check that all URLs are `https://catalysthvac.com` (Elementor → Tools → Replace URL)
4. Apply the 301 redirects (old `/all-services/…` URLs → new pages) in Rank Math → Redirections. Delete old pages and legacy plugins (Royal Elementor Addons, GTranslate, PDF Embedder) once the redirects are in.
5. Submit the sitemap in Search Console.

---

### Fallback: building as drafts on the live site
Only if staging becomes unavailable. Use Canvas-layout drafts with three saved templates (`CX – Styles`, `CX – Header`, `CX – Footer`, each an HTML widget pasted from `elementor/out/`), and never touch Site Settings on live.

## Building a section
Each section of the brief's page copy is one **container** with classes from [03-design-system.md](03-design-system.md#component--class-map-from-build-doc-spec-f). Use either method:

- **Native widgets (preferred for copy Jerry or Derrek will edit):**
  - **Container:** Advanced → CSS Classes, e.g. `cx-section cx-surface`
  - **Heading widget, eyebrow:** HTML Tag `p`, class `cx-eyebrow`
  - **Heading widget, H2 or H3:** no class needed (the base styles handle it)
  - **Text Editor:** body copy. Add class `cx-lead` for intro paragraphs.
  - **Button:** add class `cx-btn`, `cx-btn--outline` or `cx-btn--light`
  - **Cards:** a child container with class `cx-card cx-card--link`, holding an HTML widget for the icon (paste from [elementor/out/icons/](elementor/out/icons/)), a Heading, Text, and a Button or link with class `cx-link-arrow`
- **HTML widget (layout-heavy pieces such as the hero router, the decision module and the FAQ):** copy that section's markup from [preview/home.src.html](preview/home.src.html). Each section has a comment naming its component.

**Page Settings → Custom CSS** is for tweaks to that one page only. Anything reusable goes in `global.css`.

## Changing styles
Edit [elementor/global.css](elementor/global.css) (or the header/footer `.html` sources), then rebuild:
```bash
python3 elementor/build.py
```
In staging, paste the updated CSS into Site Settings → Custom CSS (or the header/footer HTML into its Theme Builder template), then preview with [preview/home.html](preview/home.html).

## SEO and schema (every page)
The single sources are [elementor/seo/site.json](elementor/seo/site.json) (business facts) and [elementor/seo/pages.json](elementor/seo/pages.json) (title, meta, breadcrumb, service per page). `build.py` generates:
- **[elementor/out/seo-register.md](elementor/out/seo-register.md):** each page's title and meta to paste into the SEO plugin, the schema types, and checks (title/meta length, one H1, heading order, alt text, placeholder count).
- **`elementor/out/seo/<page>.html`:** the page's JSON-LD. Paste it into an **HTML widget at the bottom of that page**.

**What the schema includes, per Build Doc §J:**
- **Homepage:** the business node (`Organization`) plus `WebSite` (the site itself) and `WebPage`.
- **Service pages:** `BreadcrumbList`, `WebPage` and `Service`.
- **Any page with an FAQ section:** `FAQPage`, built from the visible FAQs only (held FAQs are excluded).
- **The business node becomes `HVACBusiness` with address and hours only after the address is verified.** It never gets market-page addresses or review/star markup.
- **Facts appear only when verified.** Phone, address, hours, social profiles and founding year stay out until their `verified` flag in `site.json` is set to `true`. The register lists what's held.

**SEO plugin: Rank Math (free)**
1. Install Rank Math. In its Setup Wizard, choose *Business → Organization* and skip its Local SEO step.
2. Go to **Rank Math → Dashboard → Modules** and turn **off "Schema"**. Our JSON-LD is the schema. Two Organization graphs would conflict. Leave Sitemap, SEO Analysis and Redirections **on**.
3. **Per page:** in the Rank Math panel, paste the Title and Meta from the register. Leave the canonical as default.
4. **Breadcrumbs:** they're already in the page HTML and schema, so don't enable Rank Math's breadcrumbs as well.
5. **Redirections module:** use it for the 301 map at launch (e.g. `/all-services/air-conditioning/` → `/ac-repair/`).

**Changing a fact (e.g. the phone is confirmed):** set `"verified": true` in `site.json`, run the build, and re-paste the homepage's schema widget. Every service page references the same business record.

**After launch:**
1. Run each page through Google's Rich Results Test and the Schema Markup Validator.
2. Submit the Rank Math sitemap in Search Console.
3. Decide AI-crawler access in `robots.txt` deliberately (Build Doc §I).

## Before launch: clear every highlight
Search every page for `cx-verify`, `cx-blank`, `cx-ph`, `cx-held` and `cx-temp`; none can remain. `python3 tools/attention_inventory.py` lists them per page.

## Verify in Elementor (first pages in staging)
- [ ] Global Colors and Fonts show up (no Elementor-default light-blue headings or green buttons). If a widget still shows a default color, its own Style tab has a value set; clear it.
- [ ] The Theme Builder header is sticky. It needs no ancestor with `overflow: hidden`.
- [ ] Dropdowns open on hover and keyboard focus. The mobile menu works by touch.
- [ ] Fonts load (Barlow Condensed and Inter) over https.
- [ ] Forms send to a test inbox and show the "request, not an appointment" confirmation.
