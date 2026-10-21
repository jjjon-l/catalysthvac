# Catalyst A/C & Heat: Website Rebuild

Working files for the catalysthvac.com rebuild (WordPress + Elementor Pro on SiteGround).

| File | What it is |
|---|---|
| [01-site-audit.md](01-site-audit.md) | Audit of the current site, brand colors/fonts, competitor research |
| [02-siteground-staging-guide.md](02-siteground-staging-guide.md) | Fresh-install staging steps and DNS notes (GoDaddy DNS, M365 email) |
| [03-design-system.md](03-design-system.md) | Tokens: colors, type scale, buttons, component → class map |
| [04-elementor-build-method.md](04-elementor-build-method.md) | How pages are assembled in Elementor as drafts on the live site |
| `elementor/` | Sources: `global.css`, header/footer HTML, icons, and `build.py` |
| `elementor/out/` | Generated paste-ready snippets for the CX saved templates |
| `preview/home.html` | Local homepage preview (open in a browser) |

Rebuild the snippets and preview after editing any source:

```bash
python3 elementor/build.py
```

The Build Doc lives outside the repo (`brief/` is git-ignored).
