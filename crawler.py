from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


DEFAULT_CONITEC_URL = "https://www.gov.br/conitec/pt-br"


class _AnchorHrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.hrefs.append(value.strip())


@dataclass(frozen=True)
class CrawlResult:
    source_url: str
    pdf_urls: list[str]


def _is_pdf_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    return parsed.path.lower().endswith(".pdf")


def discover_pdf_urls(url: str, timeout_seconds: int = 20) -> CrawlResult:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = _AnchorHrefParser()
    parser.feed(html)

    normalized: set[str] = set()
    for href in parser.hrefs:
        absolute = urljoin(url, href)
        if _is_pdf_url(absolute):
            normalized.add(absolute)

    return CrawlResult(source_url=url, pdf_urls=sorted(normalized))


def save_pdf_manifest(pdf_urls: list[str], output_file: str | Path) -> Path:
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(pdf_urls).strip()
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")
    return path
