# Building on the Live Site (drafts) Without Touching Site Settings

## One-time setup (do once, in this order)
1. **Backup:** the 2026-10-20 10:22 backup exists. Take another before launch.
2. **Saved templates:** Templates → Saved Templates → Add New → **Section**. Make three, each holding one full-width container with one **HTML widget**:

| Template name | Paste into the HTML widget |
|---|---|
| `CX – Styles` | [elementor/out/cx-styles.html](elementor/out/cx-styles.html) (fonts and all component CSS) |
| `CX – Header` | [elementor/out/cx-header.html](elementor/out/cx-header.html) |
| `CX – Footer` | [elementor/out/cx-footer.html](elementor/out/cx-footer.html) (includes the mobile Call / Request bar) |

   On each template container, set padding to 0 and Content Width to Full Width.

## Every new page
1. Pages → Add New. Title it `NEW – Home`, `NEW – AC Repair`, etc. **Status: Draft.**
2. Page Settings (gear icon) → **Page Layout: Elementor Canvas**. This keeps the live site's header and footer off the page.
3. At the top, add a **Template** widget → `CX – Styles`, then another Template widget → `CX – Header`.
4. Build the sections (below).
5. At the bottom, add a Template widget → `CX – Footer`.
6. Preview from the editor. Drafts never show to logged-out visitors.

Because they're Template widgets (references, not copies), **editing a CX template once updates every page.**

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
Paste the regenerated `out/` file into its CX template, then preview with [preview/home.html](preview/home.html).

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

## At launch (per Build Doc runbook)
1. Move `global.css` into Site Settings → Custom CSS and set Global Colors and Fonts.
2. Rebuild the header and footer in Theme Builder, or keep the HTML versions as Theme Builder templates.
3. Remove the `CX – Styles` and header/footer Template widgets from each page, and switch the pages from Canvas to the default layout.
4. Search every page for `cx-ph` and `STAGING PLACEHOLDER`. None of them can remain.
5. Swap the slugs, publish, add the 301s, untick "Discourage search engines", regenerate Elementor CSS, and purge the cache.

## Verify in Elementor (not yet tested on the live install)
- [ ] The base overrides beat the live kit's default colors (light-blue `#6EC1E4` headings, gray text, green buttons). If a widget still shows the default color, its own Style tab has a value set; clear it.
- [ ] Sticky header works inside Canvas. It needs no ancestor with `overflow: hidden`.
- [ ] Dropdowns open on hover and keyboard focus. Mobile menu works by touch.
- [ ] Fonts load (Barlow Condensed and Inter) over https.
