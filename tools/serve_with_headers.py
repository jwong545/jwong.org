"""Tiny local test server that applies the same security headers as site/_headers (the /* block),
so CSP problems show up locally before deploying. Usage: python3 -I tools/serve_with_headers.py <site_dir> <port>"""
import sys, pathlib, http.server, functools

site = pathlib.Path(sys.argv[1]).resolve()
port = int(sys.argv[2])

headers, in_all = {}, False
for line in (site / "_headers").read_text().splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if not line.startswith(" "):
        in_all = line.strip() == "/*"
        continue
    if in_all and ":" in line and not line.strip().startswith("!"):
        k, v = line.strip().split(":", 1)
        headers[k.strip()] = v.strip()

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        for k, v in headers.items():
            self.send_header(k, v)
        super().end_headers()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=str(site))).serve_forever()
