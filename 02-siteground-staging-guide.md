# Staging for the Catalyst Rebuild: a Fresh Install on a Subdomain

The Build Doc (Creative & Elementor Spec §B) calls for a **fresh WordPress install with a fresh database** on its own subdomain, and **no clone of the legacy site**. SiteGround's *WordPress → Staging* tool makes a clone, so we don't use it. The `staging2` copy can be deleted later, once the new install is up. It's harmless in the meantime.

## Key DNS facts (checked 2026-10-20)
- **The nameservers are GoDaddy's** (`ns77/ns78.domaincontrol.com`), so DNS changes happen **at GoDaddy**. The SiteGround DNS Zone Editor is not used by the internet, and changing it does nothing.
- **Email runs on Microsoft 365.** The live MX record is `catalysthvac-com.mail.protection.outlook.com`. SiteGround's unused zone lists *different* MX records (mailspamprotection.com). **Never switch the nameservers to SiteGround** without copying the M365 records first, or email will stop arriving.
- Site IP: `34.174.177.62`

## 1. Back up live
Site Tools → Security → Backups → **Create Backup** (a 10:22am 2026-10-20 backup already exists).

## 2. Add the DNS record at GoDaddy
GoDaddy → Domains → catalysthvac.com → DNS → **Add New Record**
- **Type:** A
- **Name:** `new`
- **Value:** `34.174.177.62`
- **TTL:** 1 hour

Change nothing else. Check it with `dig +short new.catalysthvac.com`, which should return the IP within 5–30 minutes.

## 3. Create the subdomain in SiteGround
Site Tools → Domain → **Subdomains** → Create `new.catalysthvac.com`.

## 4. Install a fresh WordPress on it
Site Tools → WordPress → **Install & Manage** → WordPress → domain `new.catalysthvac.com`, path empty.
- Set a new admin username and password. Don't reuse the live site's.
- Untick any "WordPress Starter" or "Jetpack" add-ons.

## 5. SSL
Site Tools → Security → **SSL Manager** → Let's Encrypt → `new.catalysthvac.com`. Then Security → **HTTPS Enforce** on for that site.

## 6. Lock it down
- **Password-protect it:** Site Tools → Security → **Protected URLs** → protect `/` on `new.catalysthvac.com`, and share the login with Derrek.
- **Hide it from search engines:** WP → Settings → Reading → tick **Discourage search engines**.
- **Stop test emails reaching customers:** keep test forms sending only to your own inbox.

## 7. Base stack (keep it minimal)
- **Theme:** Hello Elementor (a child theme only if needed)
- **Builder:** Elementor and Elementor Pro (activate the license in Elementor → License)
- **SiteGround Speed Optimizer:** Dynamic Cache **off** during the build
- **Security plugin:** whatever SiteGround Security suggests
- **SEO plugin:** pick one, e.g. Rank Math or Yoast
- **Spam protection:** reCAPTCHA v3 or Cloudflare Turnstile for forms
- **Leave out the legacy plugins:** no Royal Elementor Addons, GTranslate or PDF Embedder

## 8. Bring over only the media we need
Download the logo and any keeper images from the live Media Library, then upload them to the new site. Don't import the old database.

## Tonight, before DNS exists: hosts-file workaround (your Mac only)
SiteGround's installer may need the domain to resolve. You can preview locally by adding this line to `/etc/hosts`:
```
34.174.177.62  new.catalysthvac.com
```
Edit it in Terminal with `sudo nano /etc/hosts`, then flush the DNS cache with `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`. Remove the line once the GoDaddy record is live. SSL won't issue until the real DNS exists, so expect a browser warning until then.

## At launch (later)
Migrate the new install onto `catalysthvac.com`. Use SiteGround's WordPress Migrator, or a full-site backup/restore tool like All-in-One WP Migration or Duplicator. Then:
- Replace URLs (`new.` → root)
- Apply the 301 map
- Untick "Discourage search engines"
- Regenerate Elementor CSS
- Purge the cache

The full checklist is in Build Doc Runbook §22–24.
