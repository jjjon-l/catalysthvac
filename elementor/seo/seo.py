"""SEO for each page: <head> tags, JSON-LD schema graph, and an on-page lint.

Follows Build Doc Architecture §J (structured data plan):
  - Organization on the homepage; becomes HVACBusiness (LocalBusiness) only
    once a real operating address is verified. No market-page addresses.
  - BreadcrumbList on hierarchical pages, Service on service pages,
    FAQPage built from the page's visible FAQ accordion only.
  - No review/rating markup (self-serving reviews are ineligible).
Unverified facts in site.json are left out and reported as warnings.
"""
import html
import json
import re

FAQ_ITEM = re.compile(r"<details><summary>(.*?)</summary><div>(.*?)</div></details>", re.S)


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment))).strip()


def extract_faqs(page_html: str) -> list[tuple[str, str]]:
    block = re.search(r'<div class="cx-faq">(.*?)</div>\s*(?:<p|</div>)', page_html, re.S)
    return [(_text(q), _text(a)) for q, a in FAQ_ITEM.findall(block.group(1))] if block else []


def _fact(site: dict, key: str, omitted: list[str]):
    fact = site.get(key)
    if not fact or fact.get("value") in (None, [], ""):
        return None
    if not fact.get("verified"):
        omitted.append(key)
        return None
    return fact["value"]


def build_graph(site: dict, key: str, page: dict, faqs: list[tuple[str, str]]) -> tuple[dict, list[str]]:
    origin = site["origin"]
    url = origin + page["path"]
    org_id, site_id, page_id = f"{origin}/#organization", f"{origin}/#website", f"{url}#webpage"
    omitted: list[str] = []

    area = [{"@type": "City", "name": f"{c}, TX"} for c in (_fact(site, "areaServed", omitted) or [])]
    org_ref = {"@id": org_id}
    graph = []

    if page.get("type") == "home":
        address = _fact(site, "address", omitted)
        org = {
            "@type": "HVACBusiness" if address else "Organization",
            "@id": org_id,
            "name": _fact(site, "name", omitted),
            "url": origin + "/",
            "logo": {"@type": "ImageObject", "url": _fact(site, "logo", omitted)},
            "description": _fact(site, "description", omitted),
            "areaServed": area or None,
            "telephone": _fact(site, "telephone", omitted),
            "email": _fact(site, "email", omitted),
            "legalName": _fact(site, "legalName", omitted),
            "foundingDate": _fact(site, "foundingDate", omitted),
            "sameAs": _fact(site, "sameAs", omitted),
        }
        if address:
            org["address"] = {"@type": "PostalAddress", **address}
            org["image"] = org["logo"]["url"]
            org["openingHours"] = _fact(site, "openingHours", omitted)
        graph.append({k: v for k, v in org.items() if v})
        graph.append({
            "@type": "WebSite", "@id": site_id, "url": origin + "/",
            "name": site["name"]["value"], "publisher": org_ref, "inLanguage": "en-US",
        })
    else:
        # Minimal node so references resolve on this page; full details live on the homepage.
        graph.append({"@type": "Organization", "@id": org_id, "name": site["name"]["value"], "url": origin + "/"})
        graph.append({"@type": "WebSite", "@id": site_id, "url": origin + "/", "name": site["name"]["value"]})

    webpage = {
        "@type": "WebPage", "@id": page_id, "url": url, "name": page["title"],
        "description": page["description"], "isPartOf": {"@id": site_id},
        "about": org_ref, "inLanguage": "en-US",
    }
    if page.get("breadcrumb"):
        webpage["breadcrumb"] = {"@id": f"{url}#breadcrumb"}
        graph.append({
            "@type": "BreadcrumbList", "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": name, "item": origin + path}
                for i, (name, path) in enumerate(page["breadcrumb"], 1)
            ],
        })
    graph.append(webpage)

    if page.get("service"):
        svc = page["service"]
        webpage["mainEntity"] = {"@id": f"{url}#service"}
        graph.append({
            "@type": "Service", "@id": f"{url}#service", "url": url,
            "name": svc["name"], "serviceType": svc["serviceType"], "description": svc["description"],
            "provider": org_ref, "areaServed": area or None,
            "audience": {"@type": "Audience", "audienceType": "Homeowners"},
        })

    if faqs:
        graph.append({
            "@type": "FAQPage", "@id": f"{url}#faq", "isPartOf": {"@id": page_id},
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    graph = [{k: v for k, v in node.items() if v is not None} for node in graph]
    return {"@context": "https://schema.org", "@graph": graph}, sorted(set(omitted))


def jsonld_script(graph: dict) -> str:
    body = json.dumps(graph, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{body}\n</script>\n'


def head_tags(site: dict, page: dict) -> str:
    url = site["origin"] + page["path"]
    e = lambda s: html.escape(s, quote=True)
    tags = [
        f"<title>{e(page['title'])}</title>",
        f'<meta name="description" content="{e(page["description"])}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{e(site["name"]["value"])}">',
        f'<meta property="og:title" content="{e(page["title"])}">',
        f'<meta property="og:description" content="{e(page["description"])}">',
        f'<meta property="og:url" content="{url}">',
        '<meta name="twitter:card" content="summary">',
    ]
    return "\n".join(tags) + "\n"


def lint(page_html: str, page: dict) -> dict:
    main = re.search(r"<main[^>]*>(.*)</main>", page_html, re.S)
    main = main.group(1) if main else page_html
    levels = [int(h) for h in re.findall(r"<h([1-6])\b", main)]
    skips = sorted({f"h{a}→h{b}" for a, b in zip(levels, levels[1:]) if b > a + 1})
    imgs = re.findall(r"<img\b[^>]*>", page_html)
    return {
        "title_len": len(page["title"]),
        "desc_len": len(page["description"]),
        "h1": levels.count(1),
        "heading_skips": skips,
        "img_no_alt": sum(1 for i in imgs if " alt=" not in i),
        "placeholders": len(re.findall(r'class="[^"]*\bcx-(?:ph|held)\b', main)),
        "internal_links": len(set(re.findall(r'href="(/[^"#]*)"', page_html))),
    }
