from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

from .config import CompanyConfig


@dataclass
class Motivation:
    date_iso: str
    title: str
    quote: str
    description: str
    hashtags: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OpenAIConfig:
    api_key: Optional[str]
    model: str = "gpt-4o-mini"


class MotivationalAgent:
    def __init__(self, company: CompanyConfig, tz: Optional[str] = None):
        self.company = company
        self.tz = tz or os.environ.get("TZ", "UTC")

    def _now_iso(self) -> str:
        return datetime.now().astimezone().date().isoformat()

    def _build_system_prompt(self) -> str:
        return (
            "You are a concise, inspirational writing assistant for corporate audiences. "
            "Write a daily motivational quote and a short, practical description. "
            "Keep the tone aligned with the company culture and values. Use the specified language."
        )

    def _build_user_prompt(self) -> str:
        c = self.company
        themes = ", ".join(c.themes) if c.themes else "general motivation"
        values = ", ".join(c.values) if c.values else "impact, teamwork"
        hashtags = " ".join(c.hashtags) if c.hashtags else ""
        return (
            f"Company: {c.company_name}\n"
            f"Audience: {c.audience}\n"
            f"Tone: {c.tone}\n"
            f"Language: {c.language}\n"
            f"Themes to emphasize: {themes}\n"
            f"Core values: {values}\n"
            f"Quote length: between {c.quote_length.min} and {c.quote_length.max} words\n"
            f"Description target length: ~{c.description_words} words\n"
            f"Hashtags: {hashtags}\n"
            "Return ONLY a JSON object with keys: title, quote, description."
        )

    def _try_openai(self) -> Optional[Motivation]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt()},
                ],
                temperature=0.8,
                max_tokens=400,
            )
            content = response.choices[0].message.content or "{}"
            data = json.loads(content)
            motivation = Motivation(
                date_iso=self._now_iso(),
                title=data.get("title", "Daily Motivation"),
                quote=data.get("quote", "Show up. Stay curious. Keep going."),
                description=data.get(
                    "description",
                    "Today, commit to one small action that moves a priority forward. Momentum compounds.",
                ),
                hashtags=self.company.hashtags,
            )
            return motivation
        except Exception:
            return None

    def _fallback(self) -> Motivation:
        date_iso = self._now_iso()
        snippets = [
            (
                "Own The Day",
                "Own the day, one honest decision at a time.",
                "Progress rarely arrives in heroic leaps. It’s the quiet discipline of small, well-chosen actions. Pick one task that matters and finish it with integrity.",
            ),
            (
                "Together, Further",
                "We go faster alone, but we go further together.",
                "Ask for a partner or offer your help. Collaboration turns individual effort into enduring outcomes and strengthens trust across the team.",
            ),
            (
                "Curiosity Creates",
                "Curiosity is the spark; ownership is the flame.",
                "Ask one better question today, then act on the answer. When we pair learning with action, we turn ideas into impact for our customers.",
            ),
        ]
        idx = sum(map(ord, date_iso)) % len(snippets)
        title, quote, description = snippets[idx]
        return Motivation(
            date_iso=date_iso,
            title=title,
            quote=quote,
            description=description,
            hashtags=self.company.hashtags,
        )

    def generate_daily(self) -> Motivation:
        return self._try_openai() or self._fallback()