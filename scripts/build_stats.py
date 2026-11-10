#!/usr/bin/env python3
"""Render a consistency card (contributions, active days, streaks) as an SVG.

Data source: the PUBLIC contribution graph at github.com/users/<user>/contributions,
i.e. exactly what a recruiter sees on the profile (private work is counted only if
"Include private contributions" is on in profile settings, with no repo names).

Standard library only. Usage: python3 scripts/build_stats.py [output.svg]
On any fetch/parse failure it exits non-zero WITHOUT writing, so the last good
card stays published.
"""
import re
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "akshayev"
URL = f"https://github.com/users/{USER}/contributions"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "dist" / "stats.svg"


def fetch() -> str:
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-stats-builder"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(html: str) -> list[tuple[str, int]]:
    """Return [(iso_date, count)] sorted by date."""
    dates = {cell: d for d, cell in re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"', html)}
    counts = {}
    for cell, text in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if cell not in dates:
            continue
        m = re.match(r"\s*(\d+) contributions? on", text)
        counts[dates[cell]] = int(m.group(1)) if m else 0
    days = sorted(counts.items())
    if len(days) < 300:
        raise ValueError(f"expected ~365 days, parsed {len(days)}")
    return days


def stats(days: list[tuple[str, int]]) -> dict:
    counts = [c for _, c in days]
    # Today is not over yet: a zero today does not break the streak.
    tail = counts[:-1] if counts[-1] == 0 else counts
    current = 0
    for c in reversed(tail):
        if c == 0:
            break
        current += 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    last30 = counts[-30:]
    return {
        "total": sum(counts),
        "active30": sum(1 for c in last30 if c),
        "current": current,
        "longest": longest,
    }


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def render(s: dict) -> str:
    w, h = 900, 168
    tiles = [
        (f'{s["total"]:,}', "contributions", "in the last 12 months", "#38bdf8"),
        (f'{s["active30"]}/30', "days active", "in the last 30 days", "#34d399"),
        (plural(s["current"], "day"), "current streak", "as of today", "#fbbf24"),
        (plural(s["longest"], "day"), "longest streak", "in the last 12 months", "#a78bfa"),
    ]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
         f'aria-label="{escape(", ".join(f"{v} {a}" for v, a, _, _ in tiles))}">',
         """<style>
  .t{font:600 12px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#94a3b8;letter-spacing:.08em;text-transform:uppercase}
  .v{font:800 30px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
  .a{font:600 14px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#e2e8f0}
  .b{font:400 12px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#64748b}
</style>""",
         f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="#0b1220" stroke="#1e293b"/>',
         '<text x="28" y="38" class="t">GitHub consistency</text>',
         f'<text x="{w-28}" y="38" class="b" text-anchor="end">updated daily from the public contribution graph</text>']
    col = (w - 56) / len(tiles)
    for i, (value, label, sub, color) in enumerate(tiles):
        x = 28 + i * col
        if i:
            o.append(f'<line x1="{x-14:.0f}" y1="64" x2="{x-14:.0f}" y2="142" stroke="#1e293b"/>')
        o.append(f'<text x="{x:.0f}" y="96" class="v" fill="{color}">{escape(value)}</text>')
        o.append(f'<text x="{x:.0f}" y="120" class="a">{escape(label)}</text>')
        o.append(f'<text x="{x:.0f}" y="138" class="b">{escape(sub)}</text>')
    o.append("</svg>")
    return "\n".join(o)


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    try:
        s = stats(parse(fetch()))
    except Exception as exc:
        print(f"stats unavailable, keeping previous card: {exc}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(s), encoding="utf-8")
    print(f"Wrote {out}: {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
