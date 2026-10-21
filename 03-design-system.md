# Catalyst Design System (Elementor Global Tokens)
_Proposal v1 · 2026-10-20 · the colors are sampled from `Catalyst-HVAC-Logo-2.png`. They're final once Jerry supplies the approved logo files (Fact Sheet B-1)._

## How it fits together
1. **Elementor Site Settings** hold the tokens (colors, fonts, type scale, buttons, form fields). Everything references them.
2. **One sitewide CSS file**, [elementor/global.css](elementor/global.css), pasted into *Site Settings → Custom CSS*. It holds component styles (cards, bands, CTA pairs, mobile call bar) keyed to `cx-` classes.
3. **Containers and widgets** get those classes in *Advanced → CSS Classes*. A container's own Custom CSS box is only for layout specific to that one section.
4. **Components are saved once** (Templates → Saved Templates, or Theme Builder for the header and footer) and inserted everywhere. Edit once and every page changes.

That keeps the brief's rules ("no one-off typography or button styles per page", "edit once, change everywhere", "no custom code outside Elementor") and still lets us hand-code layouts.

## Colors → Site Settings → Global Colors
| Elementor slot | Name | Hex | Use |
|---|---|---|---|
| System · Primary | Catalyst Blue | `#283A8A` | Links, section accents, secondary buttons |
| System · Secondary | Catalyst Navy | `#1B1B5C` | Header/footer, dark bands, headings |
| System · Text | Body Text | `#2A2F45` | Body copy |
| System · Accent | Catalyst Red | `#B51C20` | **Primary CTA only** (Request Service) |
| Custom | Red Hover | `#8F1519` | CTA hover |
| Custom | Navy Deep | `#121240` | Commercial band, footer base |
| Custom | Ink | `#161A2E` | H1/H2 on light backgrounds |
| Custom | Muted | `#5A6075` | Captions, helper text |
| Custom | Border | `#D8DBE2` | Card and field borders |
| Custom | Surface | `#F3F5FA` | Alternating light sections |
| Custom | Silver | `#E7E9EE` | Dividers, chips |
| Custom | Success | `#1E7A46` | Form success |
| Custom | Error | `#B3261E` | Form errors |

Contrast checks (WCAG AA for body text needs at least 4.5:1):
| Text color | Background | Ratio |
|---|---|---|
| Red `#B51C20` | White | 6.7:1 ✓ |
| White | Red `#B51C20` | 6.7:1 ✓ |
| Blue `#283A8A` | White | 10.2:1 ✓ |
| Muted `#5A6075` | White | 6.2:1 ✓ |
| Muted `#5A6075` | Surface | 5.7:1 ✓ |
| White | Navy `#1B1B5C` | 15.5:1 ✓ |
| Body `#2A2F45` | White | 13.2:1 ✓ |

## Fonts → Site Settings → Global Fonts
| Slot | Family / weight | Use |
|---|---|---|
| Primary | **Barlow Condensed 700** | H1, H2 (matches the heavy, wide logo wordmark) |
| Secondary | Barlow Condensed 600 | H3, card titles |
| Text | **Inter 400** | Body |
| Accent | Inter 600 | Eyebrows, buttons, nav, labels |

Load only these two families. Turn on Elementor → Settings → Performance → **Load Google Fonts locally**.

## Type scale → Site Settings → Typography
| Element | Desktop | Tablet | Mobile (360–390) | Line-height | Notes |
|---|---|---|---|---|---|
| H1 | 60px | 48px | 38px | 1.05 | Barlow Cond 700 |
| H2 | 44px | 38px | 32px | 1.1 | Barlow Cond 700 |
| H3 | 26px | 24px | 22px | 1.2 | Barlow Cond 600 |
| H4 | 20px | 19px | 18px | 1.3 | Inter 600 |
| Body | 18px | 17px | 16px | 1.6 | Inter 400 |
| Small / caption | 15px | 15px | 14px | 1.5 | Inter 400, Muted |
| Eyebrow | 14px | 14px | 13px | 1.2 | Inter 600, uppercase, +0.12em letter spacing, Blue (Red on dark) |
| Button | 17px | 17px | 16px | 1 | Inter 600 |

## Layout
| Token | Value |
|---|---|
| Container max width | **1240px** (Site Settings → Layout) |
| Reading width (long copy) | 720px (`cx-measure`) |
| Side gutter | 24px desktop · 20px mobile |
| Section padding (vertical) | 96px desktop · 72px tablet · 56px mobile (`cx-section`); compact 64 / 48 / 40 (`cx-section--tight`) |
| Grid gaps | 24px cards · 48px columns |
| Breakpoints | Elementor defaults: mobile ≤767, tablet ≤1024. Test at 360px. |

## Buttons → Site Settings → Buttons
| Variant | Class | Style |
|---|---|---|
| Primary | `cx-btn` (default) | Red fill, white text, 6px radius, 16×28px padding, hover Red Hover |
| Secondary | `cx-btn--outline` | 2px Navy border, Navy text; on dark backgrounds use white border and white text |
| Tertiary / text | `cx-link-arrow` | Blue text with a → that slides on hover |
| Focus (all) | — | 3px outline with a 2px offset: Blue `#283A8A` on light backgrounds (10.2:1), `#7FA2FF` on dark backgrounds (6.3:1 on Navy) |

Minimum tap target is 48px tall. Labels come from the brief's CTA system: **Request Service**, **Call Catalyst**, **Commercial HVAC Inquiry**, **Request AC Service**, etc. Never use *Book Now*, *Schedule*, *Free Estimate* or *Learn More*.

## Surfaces
- Cards: white, 1px Border, **8px radius**, a very light shadow (`0 1px 2px rgba(22,26,46,.06)`), hover lifts 2px with a Blue border
- Dark band: Navy, white text (Commercial gets **Navy Deep with a red rule**, its own visual treatment as the brief asks)
- Imagery ratios: hero 4:3 (desktop side image) / 16:9 (mobile crop), cards 3:2, team 4:5, project 4:3

## Component → class map (from Build Doc spec §F)
| # | Component | Class(es) |
|---|---|---|
| 1 | Hero + CTA pair | `cx-hero`, `cx-cta-pair` |
| 2 | Trust strip (hidden until verified) | `cx-trust` |
| 3 | Service card grid / router | `cx-grid-3`, `cx-card cx-card--link` |
| 4 | Commercial split band | `cx-band-commercial` |
| 5 | Symptom card grid | `cx-grid-3`, `cx-card cx-card--symptom` |
| 6 | Process steps | `cx-steps` |
| 7 | Repair / Replace decision module | `cx-decision` |
| 15 | Proof module | `cx-proof` (container hidden while empty) |
| 16 | Service-area bridge | `cx-areas`, `cx-chip` |
| 18 | FAQ accordion | Elementor *Accordion* widget plus the `cx-faq` class |
| 19 | Final CTA band | `cx-band-cta` |
| — | Eyebrow | `cx-eyebrow` (on a Heading widget, size "p") |
| — | Mobile call / request bar | `cx-mobilebar` (Theme Builder footer) |
| — | Brand motif (chamfered corners) | `cx-chamfer` (set `--cx-cut`) |
| — | Hero quick router | `cx-routes`, `cx-route` |
| — | Service hero + breadcrumb | `cx-hero cx-hero--service cx-dark`, `cx-breadcrumb` |
| 5 | Symptom grid (numbered) | `cx-grid-3 cx-symptoms` + `cx-card cx-card--symptom` |
| — | Two-column copy/panel | `cx-split`, `cx-split--wide-left` |
| — | Decision factors / checklists | `cx-checklist`, callout `cx-note` |
| 17 | Related-service bridge | `cx-bridge` |
| 19–20 | Final CTA with request form | `cx-request` (id `request`, `data-cta="Request AC Service"`), form `cx-form` |
| — | Header / footer / mobile bar | `cx-header`, `cx-footer`, `cx-mobilebar` (the bar jumps to `#request` when the page has one) |
| — | Staging placeholder | `cx-ph` (dashed amber box; **search for and remove all of these before launch**) |
