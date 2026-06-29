import re


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    cleaned = text.replace("\x00", " ").strip()
    cleaned = _WHITESPACE_RE.sub(" ", cleaned)
    return cleaned


def parse_document_content(raw_content: bytes | str) -> str:
    if isinstance(raw_content, bytes):
        text = raw_content.decode("utf-8", errors="replace")
    else:
        text = raw_content
    return normalize_text(text)
