"""Render site/card.html to site/business-card.pdf (2 pages, 3.5in x 2in) with headless Chromium.
Usage: python3 -I tools/build_card_pdf.py <site_dir>
Re-run after editing card.html / card.css / qr.svg."""
import sys, pathlib
from playwright.sync_api import sync_playwright

site = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto((site / "card.html").as_uri())
    pg.pdf(path=str(site / "business-card.pdf"), prefer_css_page_size=True, print_background=True)
    b.close()
print("wrote", site / "business-card.pdf")
