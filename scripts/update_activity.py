#!/usr/bin/env python3
"""Refresh the "Recent activity" block in README.md from GitHub search.

Standard library only. Calls the GitHub CLI (`gh`), which is preinstalled on
GitHub Actions runners and authenticates with GH_TOKEN.

Privacy: queries use `is:public` AND every result is re-checked for
`repository.private == false`, so private repositories are never listed even if
the token could see them.
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

USER = "akshayev"
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!--RECENT_ACTIVITY:START-->", "<!--RECENT_ACTIVITY:END-->"
MAX_ITEMS = 8


def gh_search(kind: str, query: str, sort: str, per_page: int = 20) -> list[dict]:
    out = subprocess.run(
        ["gh", "api", "-X", "GET", f"search/{kind}",
         "-f", f"q={query}", "-f", f"sort={sort}", "-f", "order=desc",
         "-f", f"per_page={per_page}"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out).get("items", [])


def short(text: str, n: int = 72) -> str:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return first if len(first) <= n else first[: n - 1] + "…"


def parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def ago(when: datetime) -> str:
    days = (datetime.now(timezone.utc) - when).days
    return "today" if days <= 0 else "yesterday" if days == 1 else f"{days}d ago"


def collect() -> list[tuple[datetime, str]]:
    items: list[tuple[datetime, str]] = []

    for c in gh_search("commits", f"author:{USER} is:public", "author-date"):
        repo = c["repository"]
        if repo.get("private"):
            continue
        when = parse(c["commit"]["author"]["date"])
        msg = short(c["commit"]["message"])
        link = f"[{repo['name']}]({repo['html_url']})"
        items.append((when, f"🔨 {link}: [{msg}]({c['html_url']})"))

    for pr in gh_search("issues", f"author:{USER} type:pr is:public", "created", 10):
        repo_name = pr["repository_url"].rsplit("/", 1)[-1]
        merged = bool((pr.get("pull_request") or {}).get("merged_at"))
        verb = "merged PR" if merged else ("closed PR" if pr["state"] == "closed" else "opened PR")
        link = f"[{repo_name}](https://github.com/{USER}/{repo_name})"
        items.append((parse(pr["created_at"]), f"🔀 {verb} in {link}: [{short(pr['title'])}]({pr['html_url']})"))

    items.sort(key=lambda x: x[0], reverse=True)
    return items


def main() -> int:
    lines, seen = [], set()
    for when, text in collect():
        if text in seen:
            continue
        seen.add(text)
        lines.append(f"- {text} · _{ago(when)}_")
        if len(lines) == MAX_ITEMS:
            break
    block = "\n".join(lines) if lines else "_No recent public activity._"

    readme = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        print("Markers not found in README.md", file=sys.stderr)
        return 1
    new = pattern.sub(lambda _: f"{START}\n{block}\n{END}", readme)
    if new != readme:
        README.write_text(new, encoding="utf-8")
        print(f"Updated with {len(lines)} items")
    else:
        print("No change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
