import re

_PUNCT_RE = re.compile(r"[.!?]+$")

def extract_trailing_punct(sentence: str) -> str:
    """
    文末の連続した . ! ? を返す（なければ空文字）。
    例: "Are you ok?!" -> "?!"
    """
    s = sentence.strip()
    m = _PUNCT_RE.search(s)
    return m.group(0) if m else ""

def strip_trailing_punct(sentence: str) -> str:
    """文末の . ! ? を除去した文を返す"""
    return _PUNCT_RE.sub("", sentence.strip())

def tokenize_for_shuffle(sentence: str):
    """
    末尾句読点を外してからトークン化。中3想定の簡易版。
    """
    core = strip_trailing_punct(sentence)
    return core.split()
