#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urldefrag, urljoin

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SOURCE_INDEX = ROOT / "docs.html"
HTML_CACHE = ROOT / ".cache" / "pretix-html"
OUT_DIR = ROOT / "knowledge" / "pretix-plugin-development"
BASE_URL = "https://docs.pretix.eu/dev/development/api/index.html"
BASE_DIR = BASE_URL.rsplit("/", 1)[0] + "/"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"`", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "index"


def title_from_page(html: str, fallback: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("div.body, main, article, section") or soup
    heading = article.find(["h1", "h2"])
    if heading:
        return " ".join(heading.get_text(" ", strip=True).replace("¶", "").split())
    title = soup.find("title")
    if title:
        return title.get_text(" ", strip=True).split(" - ")[0].strip()
    return fallback


def extract_links() -> list[tuple[str, str]]:
    soup = BeautifulSoup(SOURCE_INDEX.read_text(encoding="utf-8"), "html.parser")
    seen: set[str] = set()
    links: list[tuple[str, str]] = [("index.html", "Plugin development")]
    for link in soup.select("li.toctree-l1 > a[href]"):
        href, _fragment = urldefrag(link["href"])
        if not href or href in seen:
            continue
        seen.add(href)
        links.append((href, " ".join(link.get_text(" ", strip=True).split())))
    return links


def fetch_page(href: str) -> Path:
    HTML_CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = HTML_CACHE / href
    if href == "index.html":
        cache_path.write_text(SOURCE_INDEX.read_text(encoding="utf-8"), encoding="utf-8")
        return cache_path
    if cache_path.exists() and cache_path.stat().st_size:
        return cache_path
    url = urljoin(BASE_DIR, href)
    subprocess.run(["curl", "-sS", "-L", url, "-o", str(cache_path)], check=True)
    return cache_path


def trim_html(cache_path: Path) -> Path:
    html = cache_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    body = soup.select_one("div.body, main, article")
    if body is None:
        body = soup.find("section") or soup.body or soup

    for node in body.select("script, style, nav, form, .headerlink"):
        node.decompose()
    for link in body.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".html") or ".html#" in href:
            clean_href, fragment = urldefrag(href)
            md_name = "index.md" if clean_href == "index.html" else f"{Path(clean_href).stem}.md"
            link["href"] = md_name + (f"#{fragment}" if fragment else "")
        elif href.startswith("#"):
            pass
        elif href.startswith(("http://", "https://")):
            pass
        else:
            link["href"] = urljoin(BASE_DIR, href)

    temp_path = cache_path.with_suffix(".content.html")
    temp_path.write_text(str(body), encoding="utf-8")
    return temp_path


def convert_to_markdown(content_path: Path) -> str:
    result = subprocess.run(
        [
            "pandoc",
            "-f",
            "html",
            "-t",
            "gfm",
            "--wrap=none",
            str(content_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    markdown = result.stdout
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip() + "\n"
    return markdown


def add_front_matter(markdown: str, title: str, source_url: str) -> str:
    return (
        "---\n"
        f"title: \"{title.replace(chr(34), chr(39))}\"\n"
        f"source: \"{source_url}\"\n"
        "source_type: \"pretix docs\"\n"
        "retrieved: \"2026-07-07\"\n"
        "---\n\n"
        f"> Source: [{source_url}]({source_url})\n\n"
        f"{markdown}"
    )


def build_index(pages: list[tuple[str, str, str]]) -> str:
    lines = [
        "---",
        'title: "pretix plugin development knowledge index"',
        f'source: "{BASE_URL}"',
        'source_type: "pretix docs"',
        'retrieved: "2026-07-07"',
        "---",
        "",
        "# pretix Plugin Development Knowledge Index",
        "",
        f"Base source: [{BASE_URL}]({BASE_URL})",
        "",
        "This folder contains markdown converted from the pretix plugin development documentation. Use these files as source material when building a pretix plugin.",
        "",
        "## Pages",
        "",
    ]
    for title, file_name, source_url in pages:
        lines.append(f"- [{title}]({file_name}) - [source]({source_url})")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not SOURCE_INDEX.exists():
        print(f"Missing {SOURCE_INDEX}", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[tuple[str, str, str]] = []
    for href, fallback_title in extract_links():
        cache_path = fetch_page(href)
        title = title_from_page(cache_path.read_text(encoding="utf-8"), fallback_title)
        content_path = trim_html(cache_path)
        markdown = convert_to_markdown(content_path)
        source_url = urljoin(BASE_DIR, href)
        out_name = "index.md" if href == "index.html" else f"{Path(href).stem}.md"
        (OUT_DIR / out_name).write_text(add_front_matter(markdown, title, source_url), encoding="utf-8")
        generated.append((title, out_name, source_url))
    (OUT_DIR / "README.md").write_text(build_index(generated), encoding="utf-8")
    print(f"Generated {len(generated) + 1} markdown files in {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
