from __future__ import annotations

import json
import os
from typing import Optional
from urllib import request

from .agent import Motivation


def format_slack_message(m: Motivation) -> dict:
    quote_block = f"“{m.quote}”"
    desc_block = m.description
    hashtags = " ".join(str(h) for h in (m.hashtags or []) if h)
    title = f"{m.title} — {m.date_iso}"
    text = f"{title}\n{quote_block}\n\n{desc_block}\n\n{hashtags}".strip()
    return {
        "text": text,
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": title}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"> {quote_block}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": desc_block}},
            *(
                [{"type": "context", "elements": [{"type": "mrkdwn", "text": hashtags}]}]
                if hashtags
                else []
            ),
        ],
    }


def post_to_slack(m: Motivation, webhook_url: Optional[str] = None) -> None:
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        raise ValueError("SLACK_WEBHOOK_URL not set")
    payload = json.dumps(format_slack_message(m)).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with request.urlopen(req) as resp:
        if resp.status >= 400:
            raise RuntimeError(f"Slack webhook error: {resp.status}")