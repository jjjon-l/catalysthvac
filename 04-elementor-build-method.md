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
