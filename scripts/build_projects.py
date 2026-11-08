#!/usr/bin/env python3
"""Build project cards (assets/projects/<slug>.svg) and the README project grid
from projects.toml. Standard library only (needs Python 3.11+ for tomllib).

Add a project by adding a [[project]] block to projects.toml; nothing else.
The README grid is rewritten between the PROJECTS:START / PROJECTS:END markers.
"""
import re
import sys
import textwrap
import tomllib
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "projects.toml"
README = ROOT / "README.md"
CARD_DIR = ROOT / "assets" / "projects"
START, END = "<!--PROJECTS:START-->", "<!--PROJECTS:END-->"

PALETTE = {"sky": "#38bdf8", "emerald": "#34d399", "amber": "#fbbf24", "violet": "#a78bfa", "rose": "#fb7185"}
CYCLE = ["amber", "emerald", "sky", "violet"]
W, H = 440, 252


def clip(text: str, n: int) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"


def card(p: dict) -> str:
    accent = PALETTE.get(p.get("color", ""), PALETTE["sky"])
    metrics = p.get("metrics", [])[:3]
    lines = textwrap.wrap(p["description"], 54)[:3]
    if len(textwrap.wrap(p["description"], 54)) > 3:
        lines[-1] = clip(lines[-1], 51) + "…" if not lines[-1].endswith("…") else lines[-1]

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label={quoteattr(p["name"] + ": " + p["description"])}>']
    o.append("""<style>
  .k{font:600 11px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;letter-spacing:.08em;text-transform:uppercase}
  .n{font:700 18px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#f1f5f9}
  .d{font:400 13px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#94a3b8}
  .v{font:800 26px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
  .l{font:400 11px system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;fill:#94a3b8}
  .s{font:500 12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#64748b}
</style>""")
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="#0b1220" stroke="#1e293b"/>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="4" rx="2" fill="{accent}"/>')
    o.append(f'<text x="22" y="34" class="k" fill="{accent}">{escape(p.get("kind", "Project"))}</text>')
    o.append(f'<text x="22" y="58" class="n">{escape(clip(p["name"], 36))}</text>')
    for i, line in enumerate(lines):
        o.append(f'<text x="22" y="{84 + i*18}" class="d">{escape(line)}</text>')

    if metrics:
        col_w = (W - 44) / len(metrics)
        for i, m in enumerate(metrics):
            x = 22 + i * col_w
            color = PALETTE[CYCLE[i % len(CYCLE)]]
            if i:
                o.append(f'<line x1="{x-10:.0f}" y1="150" x2="{x-10:.0f}" y2="204" stroke="#1e293b"/>')
            o.append(f'<text x="{x:.0f}" y="176" class="v" fill="{color}">{escape(str(m["value"]))}</text>')
            for j, lab in enumerate(textwrap.wrap(m["label"], int(col_w / 6.2))[:2]):
                o.append(f'<text x="{x:.0f}" y="{194 + j*14}" class="l">{escape(lab)}</text>')
    stack = " · ".join(p.get("stack", []))
    o.append(f'<text x="22" y="{H-16}" class="s">{escape(clip(stack, 56))}</text>')
    o.append("</svg>")
    return "\n".join(o)


def grid(projects: list[dict]) -> str:
    cells = []
    for p in projects:
        alt = quoteattr(f'{p["name"]}: {p["description"]}')
        cells.append(
            f'    <td width="50%" valign="top">\n'
            f'      <a href="{p["url"]}"><img src="assets/projects/{p["slug"]}.svg" alt={alt} width="100%"></a>\n'
            f'    </td>'
        )
    rows = []
    for i in range(0, len(cells), 2):
        pair = cells[i:i + 2]
        if len(pair) == 1:
            pair.append('    <td width="50%"></td>')
        rows.append("  <tr>\n" + "\n".join(pair) + "\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main() -> int:
    projects = tomllib.loads(CONFIG.read_text(encoding="utf-8")).get("project", [])
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for p in projects:
        for key in ("slug", "name", "url", "description"):
            if key not in p:
                print(f"project is missing '{key}': {p}", file=sys.stderr)
                return 1
        wanted.add(f'{p["slug"]}.svg')
        (CARD_DIR / f'{p["slug"]}.svg').write_text(card(p), encoding="utf-8")
    for stale in CARD_DIR.glob("*.svg"):  # remove cards for projects deleted from the file
        if stale.name not in wanted:
            stale.unlink()

    readme = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        print("PROJECTS markers not found in README.md", file=sys.stderr)
        return 1
    new = pattern.sub(lambda _: f"{START}\n{grid(projects)}\n{END}", readme)
    if new != readme:
        README.write_text(new, encoding="utf-8")
    print(f"Built {len(projects)} project cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
