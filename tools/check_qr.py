"""Render site/qr.svg to a PNG with headless Chromium and decode it with OpenCV.
Usage: python3 -I tools/check_qr.py <site_dir> <expected_url>
Used to prove the QR code on the business card really opens the right address."""
import sys, pathlib, cv2
from playwright.sync_api import sync_playwright

site = pathlib.Path(sys.argv[1]).resolve()
expected = sys.argv[2]
out = pathlib.Path("/tmp/claude-0/qr_check.png")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 400, "height": 400})
    pg.goto((site / "qr.svg").as_uri())
    pg.screenshot(path=str(out))
    b.close()

img = cv2.imread(str(out))
data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
print("decoded:", repr(data))
sys.exit(0 if data.rstrip("/") == expected.rstrip("/") else 1)
