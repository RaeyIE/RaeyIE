from typing import List
from ..models import Objective, KeyResult, SuggestionRequest


def generate_okrs(request: SuggestionRequest) -> List[Objective]:
    audience = request.team or request.role or request.org or "Team"
    period = request.period or "this period"

    objective_1 = Objective(
        title=f"Improve {audience} outcome delivery in {period}",
        description=(
            "Strengthen planning, execution cadence, and cross-functional alignment "
            "to deliver higher-impact outcomes."
        ),
        key_results=[
            KeyResult(title="Increase on-time delivery rate", metric="on_time_delivery_rate", target=0.9),
            KeyResult(title="Reduce cycle time", metric="cycle_time_days", target=10),
            KeyResult(title="Improve story acceptance rate", metric="acceptance_rate", target=0.95),
        ],
    )

    objective_2 = Objective(
        title=f"Elevate customer value for {audience}",
        description="Drive measurable improvements in user satisfaction and adoption.",
        key_results=[
            KeyResult(title="Increase weekly active users", metric="wau", target="+20%"),
            KeyResult(title="Improve NPS", metric="nps", target="≥ 45"),
            KeyResult(title="Raise feature adoption", metric="feature_adoption", target="+30%"),
        ],
    )

    return [objective_1, objective_2]