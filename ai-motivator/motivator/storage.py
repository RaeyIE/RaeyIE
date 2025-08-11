from __future__ import annotations

import json
from pathlib import Path

from .agent import Motivation


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(output_dir: str | Path, m: Motivation) -> Path:
    out_dir = ensure_dir(output_dir)
    out_path = out_dir / f"{m.date_iso}.json"
    out_path.write_text(json.dumps(m.to_dict(), indent=2, ensure_ascii=False))
    return out_path


def save_markdown(output_dir: str | Path, m: Motivation) -> Path:
    out_dir = ensure_dir(output_dir)
    out_path = out_dir / f"{m.date_iso}.md"
    hashtags = " ".join(str(h) for h in (m.hashtags or []) if h)
    content = (
        f"# {m.title} — {m.date_iso}\n\n"
        f"> {m.quote}\n\n"
        f"{m.description}\n\n"
        f"{hashtags}\n"
    )
    out_path.write_text(content)
    return out_path