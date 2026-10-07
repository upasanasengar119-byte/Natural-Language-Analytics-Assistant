"""Map natural-language questions to a constrained semantic plan (never raw SQL)."""
import re
import unicodedata

ALLOWED_METRICS = {"total", "count", "by_region"}
ALLOWED_REGIONS = {"EU", "US", "IN"}
# Ordered for stable matching. "IN" is special-cased below so English
# preposition "in" does not become region India.
REGION_ORDER = ("EU", "US", "IN")


def tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", value).casefold()
    return re.findall(r"[\w]+", normalized)


def detect_region(question: str) -> str | None:
    """Prefer explicit region codes; never treat preposition 'in' as India."""
    raw_tokens = re.findall(r"[\w]+", unicodedata.normalize("NFC", question))
    for region in REGION_ORDER:
        if region in raw_tokens:
            return region
    lower_tokens = tokens(question)
    for region in ("EU", "US"):
        if region.casefold() in lower_tokens:
            return region
    return None


def plan_question(question: str) -> dict:
    """Deterministic local planner used as baseline / offline fallback."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question must be a nonempty string")
    lower = question.casefold()
    region = detect_region(question)
    if "by region" in lower:
        return {"metric": "by_region", "region": None}
    if "count" in lower or "how many" in lower:
        return {"metric": "count", "region": region}
    if "total" in lower or "sales" in lower:
        return {"metric": "total", "region": region}
    raise ValueError(
        "unsupported question; ask for total sales, order count, or sales by region"
    )


def validate_plan(plan: dict) -> dict:
    if not isinstance(plan, dict) or set(plan) != {"metric", "region"}:
        raise ValueError("invalid plan schema")
    if plan["metric"] not in ALLOWED_METRICS:
        raise ValueError("unsupported metric")
    if plan["region"] is not None and plan["region"] not in ALLOWED_REGIONS:
        raise ValueError("unsupported region")
    return plan
