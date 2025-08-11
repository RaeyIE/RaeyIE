from ..models import ChatRequest


def generate_reply(request: ChatRequest) -> str:
    persona = (request.persona or "coach").lower()
    prefix = {
        "coach": "Coaching insight",
        "checker": "Performance check",
        "nudger": "Nudge",
    }.get(persona, "Assistant")

    metrics_snippet = ""
    if request.metrics:
        top_keys = list(request.metrics.keys())[:3]
        metrics_snippet = f" Based on metrics: {', '.join(top_keys)}."

    return f"{prefix}: {request.message.strip()}{metrics_snippet}"