#!/usr/bin/env python3
"""Render assets/activity.svg: a live "recent activity" card for the profile.

Left side: timeline of the latest public commits and pull requests.
Right side: a 16-week contribution heatmap.

Standard library only. Talks to GitHub through the `gh` CLI (preinstalled on
GitHub Actions runners; authenticates with GH_TOKEN).

Privacy: searches use `is:public` AND every result is re-checked for
`repository.private == false`, so private repositories are never listed. The
heatmap only uses per-day counts (no repo names).
The SVG has its own dark background, so it reads well in light and dark mode.
"""
import json
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = "akshayev"
OUT = Path(__file__).resolve().parent.parent / "assets" / "activity.svg"
ROWS = 6
WEEKS = 16


def gh(*args: str) -> dict:
    out = subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def search(kind: str, query: str, sort: str, per_page: int) -> list[dict]:
    return gh("-X", "GET", f"search/{kind}", "-f", f"q={query}", "-f", f"sort={sort}",
              "-f", "order=desc", "-f", f"per_page={per_page}").get("items", [])


def parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def ago(when: datetime) -> str:
    days = (datetime.now(timezone.utc) - when).days
    return "today" if days <= 0 else "yesterday" if days == 1 else f"{days}d ago"


def clip(text: str, n: int) -> str:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first if len(first) <= n else first[: n - 1] + "…"


def timeline() -> list[dict]:
    items: list[dict] = []
    for c in search("commits", f"author:{USER} is:public", "author-date", 20):
        repo = c["repository"]
        if repo.get("private"):
            continue
        items.append({"when": parse(c["commit"]["author"]["date"]), "kind": "commit",
                      "repo": repo["name"], "text": clip(c["commit"]["message"], 54)})
    for pr in search("issues", f"author:{USER} type:pr is:public", "created", 10):
        merged = bool((pr.get("pull_request") or {}).get("merged_at"))
        kind = "merged" if merged else "pr"
        items.append({"when": parse(pr["created_at"]), "kind": kind,
                      "repo": pr["repository_url"].rsplit("/", 1)[-1], "text": clip(pr["title"], 54)})
    items.sort(key=lambda i: i["when"], reverse=True)
    seen, out = set(), []
    for i in items:
        key = (i["repo"], i["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append(i)
    return out[:ROWS]


def heatmap() -> tuple[list[list[int]], int]:
    """Return (weeks x 7 grid of counts, total) for the last WEEKS weeks. Empty on failure."""
    try:
        query = '{user(login:"%s"){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}' % USER
        data = gh("graphql", "-f", "query=" + query)
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    except Exception as exc:  # degrade gracefully: the card still renders without the heatmap
        print(f"heatmap unavailable: {exc}", file=sys.stderr)
        return [], 0
    grid = [[d["contributionCount"] for d in w["contributionDays"]] for w in weeks[-WEEKS:]]
    return grid, sum(map(sum, grid))


def level_color(n: int, peak: int) -> str:
    if n <= 0:
        return "#1e293b"
    ratio = n / max(peak, 1)
    return "#134e4a" if ratio < .25 else "#0f766e" if ratio < .5 else "#14b8a6" if ratio < .75 else "#5eead4"


KIND = {"commit": ("#38bdf8", "commit"), "pr": ("#a78bfa", "PR opened"), "merged": ("#34d399", "PR merged")}


def render(items: list[dict], grid: list[list[int]], total: int) -> str:
    w, h = 900, 318
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Recent GitHub activity">')
    p.append("""<style>
  .t{font:700 18px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#f1f5f9}
  .s{font:500 12px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#94a3b8}
  .r{font:600 14px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#e2e8f0}
  .m{font:400 13px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#94a3b8}
  .row{opacity:0;animation:in .6s ease-out forwards}
  .live{animation:pulse 1.8s ease-in-out infinite}
  @keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
  @keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
  @media (prefers-reduced-motion:reduce){.row,.live{animation:none;opacity:1}}
</style>""")
    p.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16" fill="#0b1220" stroke="#1e293b"/>')
    p.append('<circle cx="34" cy="38" r="5" fill="#34d399" class="live"/>')
    p.append('<text x="48" y="43" class="t">Live activity</text>')
    p.append('<text x="48" y="62" class="s">Latest public commits and pull requests</text>')

    y = 96
    for idx, it in enumerate(items):
        color, label = KIND[it["kind"]]
        delay = f"{0.1 + idx * 0.12:.2f}s"
        p.append(f'<g class="row" style="animation-delay:{delay}">')
        p.append(f'<circle cx="34" cy="{y-5}" r="5" fill="{color}"/>')
        if idx < len(items) - 1:
            p.append(f'<line x1="34" y1="{y+1}" x2="34" y2="{y+35}" stroke="#1e293b" stroke-width="2"/>')
        p.append(f'<text x="52" y="{y}" class="r">{escape(clip(it["repo"], 30))}</text>')
        p.append(f'<text x="52" y="{y+18}" class="m">{escape(label)} · {escape(it["text"])}</text>')
        p.append(f'<text x="520" y="{y}" class="s" text-anchor="end">{ago(it["when"])}</text>')
        p.append("</g>")
        y += 37
    if not items:
        p.append('<text x="52" y="110" class="m">No recent public activity.</text>')

    if grid:
        peak = max(max(col) for col in grid)
        x0, y0, cell, gap = 572, 98, 14, 3
        p.append(f'<text x="{x0}" y="43" class="t">Last {len(grid)} weeks</text>')
        p.append(f'<text x="{x0}" y="62" class="s">{total} contributions</text>')
        for wi, col in enumerate(grid):
            for di, n in enumerate(col):
                p.append(f'<rect x="{x0 + wi*(cell+gap)}" y="{y0 + di*(cell+gap)}" width="{cell}" height="{cell}" rx="3" fill="{level_color(n, peak)}"/>')
        ly = y0 + 7 * (cell + gap) + 18
        p.append(f'<text x="{x0}" y="{ly+10}" class="s">Less</text>')
        for i, c in enumerate(["#1e293b", "#134e4a", "#0f766e", "#14b8a6", "#5eead4"]):
            p.append(f'<rect x="{x0 + 34 + i*17}" y="{ly}" width="13" height="13" rx="3" fill="{c}"/>')
        p.append(f'<text x="{x0 + 34 + 5*17 + 4}" y="{ly+10}" class="s">More</text>')
    p.append("</svg>")
    return "\n".join(p)


def main() -> int:
    items = timeline()
    grid, total = heatmap()
    svg = render(items, grid, total)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if svg != old:
        OUT.write_text(svg, encoding="utf-8")
        print(f"Updated: {len(items)} timeline rows, {total} contributions")
    else:
        print("No change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
