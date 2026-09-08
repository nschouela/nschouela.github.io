#!/usr/bin/env python3
"""Post-render: advertise directory URLs (/research/) rather than
/research/index.html, matching the paths the WordPress site used for six years,
and add a canonical <link> to each page so the two forms don't split indexing."""
import pathlib, re

docs = pathlib.Path(__file__).parent / "docs"
SITE = "https://noahschouela.com"

sm = docs / "sitemap.xml"
if sm.exists():
    s = sm.read_text()
    s = s.replace("/index.html</loc>", "/</loc>").replace(f"{SITE}/</loc>", f"{SITE}/</loc>")
    sm.write_text(s)
    print("tidy-urls: sitemap rewritten to directory URLs")

for html in docs.rglob("*.html"):
    rel = html.relative_to(docs).as_posix()
    url = SITE + "/" + re.sub(r"(^|/)index\.html$", r"\1", rel)
    s = html.read_text()
    if 'rel="canonical"' in s:
        continue
    s = s.replace("</head>", f'<link rel="canonical" href="{url}">\n</head>', 1)
    html.write_text(s)
print("tidy-urls: canonical tags added")
