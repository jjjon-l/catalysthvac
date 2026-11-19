# Catalyst A/C & Heat: Website Rebuild

Working files for the catalysthvac.com rebuild (WordPress + Elementor Pro on SiteGround).

| File | What it is |
|---|---|
| [01-site-audit.md](01-site-audit.md) | Audit of the current site, brand colors/fonts, competitor research |
| [02-siteground-staging-guide.md](02-siteground-staging-guide.md) | Fresh-install staging steps and DNS notes (GoDaddy DNS, M365 email) |
| [03-design-system.md](03-design-system.md) | Tokens: colors, type scale, buttons, component → class map |
| [04-elementor-build-method.md](04-elementor-build-method.md) | How pages are assembled in Elementor as drafts on the live site |
| [05-block-2-changes.md](05-block-2-changes.md) | What Block 2A/2B/2C changed and how it was applied |
| [06-questions-for-derrek.md](06-questions-for-derrek.md) | Plain-English question sheet: everything still to confirm before launch |
| `tools/attention_inventory.py` | Lists every highlighted (to confirm), blank and placeholder item per page |
| `elementor/` | Sources: `global.css`, header/footer HTML, icons, and `build.py` |
| `elementor/out/` | Generated paste-ready snippets for the CX saved templates |
| `elementor/seo/` | SEO single source: `site.json` (business facts, published only when verified), `pages.json` (title/meta/breadcrumb/service per page), `seo.py` (schema + checks) |
| `elementor/out/seo-register.md` | Generated: titles/metas for the SEO plugin, schema types, on-page checks, facts held out |
| `elementor/out/pages/*.html` | Generated: each page's full body + schema, ready to paste into one Elementor HTML widget |
| `elementor/out/seo/*.html` | Generated: per-page JSON-LD schema to paste into an HTML widget |
| `preview/home.html`, `preview/ac-repair.html` | Local page previews (open in a browser): the Block 1 sample pages |

Rebuild the snippets and preview after editing any source:

```bash
python3 elementor/build.py
```

The Build Doc lives outside the repo (`brief/` is git-ignored).
