"""Browser test: phone + desktop. Checks horizontal overflow, console/CSP errors, clock, back-to-top,
expanders, and saves screenshots. Usage: python3 -I tools/test_site.py <base_url> <out_dir>"""
import sys, pathlib
from playwright.sync_api import sync_playwright

base, out = sys.argv[1].rstrip("/"), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
pages = ["/index.html", "/projects/homelab-v2.html", "/projects/homelab-v1.html",
         "/projects/resume-pipeline.html", "/projects/fun-project.html", "/card.html", "/404.html"]
problems = []

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in (("phone", {"width": 390, "height": 844}), ("small", {"width": 320, "height": 640}),
                     ("desktop", {"width": 1280, "height": 800})):
        ctx = b.new_context(viewport=vp, timezone_id="America/Chicago", locale="en-US",
                            device_scale_factor=2 if name == "phone" else 1, has_touch=name != "desktop")
        for path in pages:
            pg = ctx.new_page()
            msgs = []
            pg.on("console", lambda m, msgs=msgs: msgs.append(m.text) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e, msgs=msgs: msgs.append(str(e)))
            resp = pg.goto(base + path)
            pg.wait_for_timeout(300)
            over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if over > 0:
                problems.append(f"{name} {path}: horizontal overflow {over}px")
            if resp.status >= 400 and path != "/404.html":
                problems.append(f"{name} {path}: HTTP {resp.status}")
            for m in msgs:
                problems.append(f"{name} {path}: console: {m}")
            if path == "/index.html":
                if name == "phone":
                    print("clock local:", pg.inner_text("#clock-local"))
                    print("clock place:", pg.inner_text("#clock-place"), "|", pg.inner_text("#clock-tz"))
                    print("clock utc  :", pg.inner_text("#clock-utc"))
                    print("totop hidden at top:", pg.evaluate("document.getElementById('totop').hidden"))
                    pg.evaluate("window.scrollTo(0, 1500)"); pg.wait_for_timeout(250)
                    print("totop hidden after scroll:", pg.evaluate("document.getElementById('totop').hidden"))
                    pg.screenshot(path=str(out / "phone_scrolled.png"))
                    pg.click("#totop"); pg.wait_for_timeout(800)
                    print("scrollY after tap:", pg.evaluate("Math.round(window.scrollY)"))
                    # expander test: events
                    pg.click("#events details summary")
                    print("events expander open:", pg.evaluate("document.querySelector('#events details').open"))
                    pg.screenshot(path=str(out / "phone_events_open.png"), full_page=False)
                pg.screenshot(path=str(out / f"{name}_index.png"), full_page=True)
            elif path == "/card.html":
                pg.screenshot(path=str(out / f"{name}_card.png"), full_page=True)
            elif path == "/projects/homelab-v2.html" and name == "phone":
                pg.screenshot(path=str(out / "phone_project.png"), full_page=True)
            pg.close()
        ctx.close()
    b.close()

print("PROBLEMS:" if problems else "no problems found")
for x in problems:
    print(" -", x)
