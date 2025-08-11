from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional

from .agent import MotivationalAgent
from .config import load_config
from .slack import post_to_slack
from .storage import save_json, save_markdown


def load_env_file(env_path: str) -> None:
    p = Path(env_path)
    if p.exists():
        for line in p.read_text().splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            os.environ.setdefault(key, val)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Motivator CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate today's motivation")
    gen.add_argument("--config", dest="config_path", required=True)
    gen.add_argument("--out-dir", dest="out_dir", required=True)
    gen.add_argument("--post-slack", dest="post_slack", action="store_true", default=False)
    gen.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)
    gen.add_argument("--tz", dest="tz", default=None)
    gen.add_argument("--env-file", dest="env_file", default=".env")
    return parser


def cmd_generate(args: argparse.Namespace) -> int:
    if args.env_file:
        load_env_file(args.env_file)

    company_cfg = load_config(args.config_path)
    agent = MotivationalAgent(company_cfg, tz=args.tz)
    motivation = agent.generate_daily()

    json_path = save_json(args.out_dir, motivation)
    md_path = save_markdown(args.out_dir, motivation)

    if args.dry_run:
        print(f"Title: {motivation.title}")
        print(f"Quote: {motivation.quote}")
        print(f"Description: {motivation.description}")
        if motivation.hashtags:
            print("Hashtags: " + " ".join(str(h) for h in (motivation.hashtags or []) if h))
        print(f"Saved: {json_path}")
        print(f"Saved: {md_path}")

    if args.post_slack:
        try:
            post_to_slack(motivation)
            print("Posted to Slack")
        except Exception as exc:
            print(f"Failed to post to Slack: {exc}")
            return 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())