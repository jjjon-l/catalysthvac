# Block 2 Changes (2A / 2B / 2C, received 2026-11-14)

Per the PM: **the Block 2A, 2B and 2C docs override the original Build Doc.** Source files are in `brief/` (git-ignored).

## Scope: 21 → 31 launch pages
| Change | Detail |
|---|---|
| **Positioning** | Residential, **multi-family, commercial and industrial** HVAC across **all of Greater Houston** (coverage confirmed). |
| **Attic Insulation replaces Indoor Air Quality** | `/attic-insulation/` (301 from `/all-services/attic-insulation/`). CTA: *Request an Attic Insulation Assessment*. IAQ page dropped. |
| **New: Multi-Family HVAC** | `/multi-family-hvac/`, a top-level nav item, with Senior Living HVAC under it. CTA: *Start a Multi-Family Inquiry*. |
| **New: Industrial HVAC** | `/industrial-hvac/`, a top-level nav item (energy corridor, petrochemical, hydronic, fan coils, VRV/VRF). CTA: *Start an Industrial Inquiry*. |
| **New: Careers** | `/careers/` under About, with a resume-upload form. Never enters the lead pipeline. |
| **Commercial expanded** | Building types (shopping centers, theaters, big-box, churches, modular), plus specialty routes and two new FAQs. |
| **Coil page defined** | `/coil-cleaning-repair/`: *Commercial HVAC Coil Cleaning & Repair*. |
| **Project Management** | H1: *HVAC Project Management & Coordination*. |
| **Seven regional pages** | Under `/service-areas/`, one regional template. The six local pages now sit under Southeast Houston & Bay Area. |

## Facts newly confirmed
- **Daikin** is the installed brand. Catalyst is a **Daikin Pro**, and the homepage and residential hub get a Daikin section. *Still held:* the Daikin Pro listing link and the Texas Daikin warranty terms.
- The **Catalyst Membership Plan** exists, and its name and benefits are confirmed from the current site's page. The membership module is **on**. *Still held:* price and terms.
- A **financing partner** exists. *Still held:* the partner's name.
- **All of Greater Houston** is confirmed coverage.

## Still held (no change)
- Phone, hours, license, address treatment, reviews and photos.
- **24-hour emergency service** is listed as a hold on every regional page. It dropped off the house-rules "never claim" list, but it isn't confirmed. Keep it off until Jerry confirms in writing.

## New navigation
**Residential · Multi-Family · Commercial · Industrial · About**

| Menu | Items |
|---|---|
| Residential | AC Repair · AC Replacement · Heating Repair · Heating Replacement · HVAC Maintenance · **Attic Insulation** · All Residential HVAC |
| Multi-Family | Multi-Family HVAC · Senior Living HVAC |
| Commercial | Commercial HVAC · HVAC Project Management · Coil Cleaning & Repair |
| Industrial | Industrial HVAC |
| About | About Catalyst · **Service Areas** · Careers · **Contact** |

Service Areas and Contact move under About.

## New forms and events
- **New forms:** Multi-family, senior living, industrial and careers. Each lead type stays separate, and careers goes to hiring.
- **Events:** `multifamily_form_submit`, `senior_living_form_submit`, `industrial_form_submit`, `careers_application_submit` (tracked, never counted as a lead).

## Timeline
**Launch before Thanksgiving (Nov 26)**, with all seven regional pages in the set and Google Ads starting right after launch.

## Impact on the four pages already built
| Item | Where |
|---|---|
| IAQ links → Attic Insulation | Header, footer, homepage service card and FAQ, AC Replacement's comfort section |
| Homepage hero eyebrow → "Residential · Multi-Family · Commercial · Industrial HVAC" | Home |
| Homepage Commercial band → "HVAC for Properties, Businesses and Industrial Facilities" (three cards) | Home |
| New homepage section: "Daikin Comfort, Installed and Serviced by Catalyst" | Home (copy needed) |
| Service-area headings → "…Across Greater Houston"; replace the "operating focus through South/Southeast Houston" wording; chips → seven regions | Home, AC Repair, AC Replacement, Heating Repair |
| Meta updates | Home (new meta), AC Repair ("appropriate" for "right") |
| Membership module can now show the plan name and benefits | Maintenance bridges on all pages |
| `site.json` `areaServed` → Greater Houston and the regions | Schema |

## Needed from Derrek
The **sub-tab copy**. These three docs are the register and summaries, and they point to the sub-tabs for the actual copy:
- Home (updated)
- Residential hub
- Attic Insulation
- Commercial (Nov)
- Multi-Family
- Senior Living
- Industrial
- Careers
- Service Areas hub
- The seven Region sub-tabs
- The regional template
- About and Contact (if changed)
- The updated Fact Sheet (if any facts were confirmed)

## Applied to the four built pages (2026-11-14)
- **Header and footer:** new nav (Residential · Multi-Family · Commercial · Industrial · About) and Attic Insulation in place of IAQ. The footer lists the seven regions and the new Company links, and its positioning line is updated.
- **Homepage:**
  - new hero eyebrow and properties router
  - Attic Insulation card
  - "HVAC for Properties, Businesses and Industrial Facilities" band with Multi-Family, Commercial and Industrial cards
  - "HVAC Service Across All of Greater Houston" with seven region links
  - Daikin section slot
  - membership card
  - updated FAQs and final CTA
- **AC Repair, AC Replacement, Heating Repair:**
  - all-of-Greater-Houston coverage wording and seven region links
  - headings "…Across Greater Houston"
  - Attic Insulation link
  - membership mention in the maintenance bridges
  - Daikin, financing and warranty hold notes updated
- **Schema and metas:** all of Greater Houston plus its counties as `areaServed`; the new positioning line; the 2B metas for Home and AC Repair.
- **Interim copy:** some is drawn from the register and the 2A customer table (Attic card, properties cards, service-area body). It's marked in the source with HTML comments. Swap it for the sub-tab copy when it arrives.
- **Held conflict:** the current Membership Plan page lists "24-hour emergency service" as a benefit, but 2B holds 24-hour service on every regional page. It's left off the membership card until Jerry confirms.

## Full exports received (2026-11-14, later)
The first PDFs were the cover tab only. The full exports (all Google Doc tabs) are `brief/block-2{a,b,c}-full-2026-11-14.pdf`:
- **2B:** register and full copy for all original pages, plus About, Contact, the Service Areas hub, the regions and the local pages.
- **2C:** Multi-Family, Commercial (Nov), Industrial and Careers.
- **2A:** Fact Sheet, Architecture, Messaging and the Elementor spec.

**Yellow = to confirm.** The docs highlight best-guess facts in yellow, and Jerry confirms or cuts each before launch. `brief/*.yellow.txt` marks them with ⟦Y …⟧ (read from the PDF's highlight colors). On the site they render with `cx-verify` / `cx-blank`.

**Rebuilt from the full 2B copy:** Home, AC Repair, AC Replacement, Heating Repair. That replaces the interim copy from the earlier pass.
- New sections: trust strips, the AC Repair 4-step process and proof cards, the AC Replacement process, tiers, Daikin FIT feature, proposal, financing and warranty copy, the Heating Repair equipment list, and the new FAQs.

**Phone:** the docs now show **(832) 281-4515**, highlighted yellow (to confirm). Every phone link sitewide was switched from the old site's (713) 244-5070. It stays out of schema until verified.

**Fact Sheet A additions:**
- Daikin Pro with a national account; Goodman partner for multi-family.
- Financing offered; partner TBD (Synchrony, or GreenSky via ServiceTitan).
- All of Greater Houston, with no exclusions (B-8 closed).
