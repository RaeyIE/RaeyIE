from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class QuoteLength:
    min: int = 8
    max: int = 28


@dataclass
class CompanyConfig:
    company_name: str
    audience: str = "All employees"
    tone: str = "uplifting, authentic, and actionable"
    language: str = "en"
    themes: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    quote_length: QuoteLength = field(default_factory=QuoteLength)
    description_words: int = 80
    hashtags: List[str] = field(default_factory=list)


def _parse_scalar(value: str) -> Any:
    v = value.strip()
    if v == "":
        return ""
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    # Try int
    try:
        return int(v)
    except ValueError:
        pass
    # Try float
    try:
        return float(v)
    except ValueError:
        pass
    # Booleans
    low = v.lower()
    if low in {"true", "yes"}:
        return True
    if low in {"false", "no"}:
        return False
    return v


def _parse_simple_yaml(path: Path) -> Dict[str, Any]:
    lines = path.read_text().splitlines()
    result: Dict[str, Any] = {}
    i = 0
    n = len(lines)

    def current_indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    while i < n:
        line = lines[i]
        i += 1
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.lstrip() != line:
            # We only expect top-level entries here
            continue
        if ":" not in line:
            continue
        key, _, remainder = line.partition(":")
        key = key.strip()
        remainder = remainder.strip()
        # Case 1: key: value
        if remainder:
            result[key] = _parse_scalar(remainder)
            continue
        # Case 2: key: followed by list or nested dict
        # Peek next significant line
        block: List[str] = []
        start_pos = i
        while i < n and (lines[i].startswith("  ") or not lines[i].strip()):
            block.append(lines[i])
            i += 1
        # Determine if list or dict
        list_items: List[Any] = []
        dict_items: Dict[str, Any] = {}
        is_list = False
        for b in block:
            if b.strip().startswith("- "):
                is_list = True
                break
        if is_list:
            for b in block:
                s = b.strip()
                if not s or s.startswith("#"):
                    continue
                if s.startswith("- "):
                    list_items.append(_parse_scalar(s[2:].strip()))
            result[key] = list_items
        else:
            for b in block:
                if not b.strip() or b.strip().startswith("#"):
                    continue
                if ":" not in b:
                    continue
                sub_key, _, sub_val = b.strip().partition(":")
                dict_items[sub_key.strip()] = _parse_scalar(sub_val.strip())
            result[key] = dict_items
    return result


def load_config(path: str | Path) -> CompanyConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    raw: Dict[str, Any]
    try:
        # Try PyYAML if available
        import yaml  # type: ignore

        raw = yaml.safe_load(config_path.read_text()) or {}
    except Exception:
        raw = _parse_simple_yaml(config_path)

    # Build QuoteLength
    ql_raw = raw.get("quote_length", {}) or {}
    quote_length = QuoteLength(
        min=int(ql_raw.get("min", 8)),
        max=int(ql_raw.get("max", 28)),
    )

    cfg = CompanyConfig(
        company_name=str(raw.get("company_name", "Company")),
        audience=str(raw.get("audience", "All employees")),
        tone=str(raw.get("tone", "uplifting, authentic, and actionable")),
        language=str(raw.get("language", "en")),
        themes=list(raw.get("themes", []) or []),
        values=list(raw.get("values", []) or []),
        quote_length=quote_length,
        description_words=int(raw.get("description_words", 80)),
        hashtags=list(raw.get("hashtags", []) or []),
    )
    return cfg