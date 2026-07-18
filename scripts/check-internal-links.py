#!/usr/bin/env python3
"""Check that every internal HTML link and asset resolves in a Hugo build."""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append(value.strip())


def page_url(relative_path):
    value = relative_path.as_posix()
    if value == "index.html":
        return "/"
    if value.endswith("/index.html"):
        return f"/{value[:-10]}"
    return f"/{value}"


def resolves(public_dir, url_path):
    path = unquote(url_path).lstrip("/")
    if not path:
        path = "index.html"

    candidates = [public_dir / path]
    if url_path.endswith("/"):
        candidates.append(public_dir / path / "index.html")
    elif not Path(path).suffix:
        candidates.append(public_dir / path / "index.html")

    return any(candidate.is_file() for candidate in candidates)


def main():
    public_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not public_dir.is_dir():
        raise SystemExit(f"Build directory not found: {public_dir}")

    broken = []
    checked = 0
    internal_hosts = {"blog.aymantech.net", "localhost", "127.0.0.1"}

    for html_file in sorted(public_dir.rglob("*.html")):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        source_url = page_url(html_file.relative_to(public_dir))

        for raw_link in parser.links:
            if raw_link.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
                continue

            parsed_raw = urlparse(raw_link)
            if parsed_raw.netloc and parsed_raw.hostname not in internal_hosts:
                continue

            absolute = urlparse(urljoin(f"https://blog.aymantech.net{source_url}", raw_link))
            if absolute.hostname not in internal_hosts:
                continue

            checked += 1
            if not resolves(public_dir, absolute.path):
                broken.append((html_file.relative_to(public_dir).as_posix(), raw_link))

    if broken:
        for source, target in sorted(set(broken)):
            print(f"BROKEN {source}: {target}")
        raise SystemExit(f"Found {len(set(broken))} broken internal links")

    print(f"Checked {checked} internal links and assets: all resolved")


if __name__ == "__main__":
    main()
