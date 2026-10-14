// Small, dependency-free script. No network requests, no cookies, no tracking.
// It lives in its own file so the Content-Security-Policy can forbid inline scripts.
(function () {
  "use strict";

  // Footer year
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // ---- Back-to-top button: appears after scrolling down ----
  var toTop = document.getElementById("totop");
  if (toTop) {
    var onScroll = function () {
      toTop.hidden = window.scrollY < 400;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- Clock: the visitor's local date/time/location + UTC ----
  // Everything comes from the visitor's own device (Intl API). Nothing is sent anywhere.
  var elLocal = document.getElementById("clock-local");
  var elTz = document.getElementById("clock-tz");
  var elPlace = document.getElementById("clock-place");
  var elUtc = document.getElementById("clock-utc");
  if (!elLocal && !elUtc) return;

  // "sv-SE" gives an ISO-like layout: 2026-10-12 14:03:11 (24-hour, year first).
  function fmt(timeZone) {
    var opts = {
      year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false
    };
    if (timeZone) opts.timeZone = timeZone;
    return new Intl.DateTimeFormat("sv-SE", opts);
  }

  var tz = "";
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) { /* ignore */ }

  var local = fmt();
  var utc = fmt("UTC");

  // The device's time zone name is the "location" (e.g. America/Chicago -> Chicago).
  // This needs no permission prompt. Precise GPS would need one, so it is not used.
  if (elPlace) {
    var parts = tz.split("/");
    var city = (parts[parts.length - 1] || "").replace(/_/g, " ");
    elPlace.textContent = city || "unknown";
  }
  if (elTz) {
    var abbr = "";
    try {
      var p = new Intl.DateTimeFormat("en-US", { timeZoneName: "short" }).formatToParts(new Date());
      for (var i = 0; i < p.length; i++) if (p[i].type === "timeZoneName") abbr = p[i].value;
    } catch (e) { /* ignore */ }
    elTz.textContent = (tz || "unknown") + (abbr ? " (" + abbr + ")" : "");
  }

  function tick() {
    var now = new Date();
    if (elLocal) elLocal.textContent = local.format(now);
    if (elUtc) elUtc.textContent = utc.format(now) + " UTC";
  }
  tick();
  setInterval(tick, 1000);
})();
