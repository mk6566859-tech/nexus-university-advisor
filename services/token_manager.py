import json
import re
from services.config import MAX_TOTAL_TOKENS, AGENT_MAX_COMPLETION

def estimate_tokens(text: str) -> int:
    # Conservative application-side estimate; provider usage may differ.
    return max(1, len(text) // 4)

def compact_json(value, max_chars: int = 5200) -> str:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text if len(text) <= max_chars else text[:max_chars] + ',"_truncated":true}'

def normalize_output(raw) -> str:
    if raw is None:
        return ""
    if hasattr(raw, "raw"):
        raw = raw.raw
    return str(raw).strip()

def clip_text(text: str, max_chars: int = 2600) -> str:
    text = str(text)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[context clipped for token budget]"

def budget_snapshot(prompts_and_outputs: list[str]) -> dict:
    estimated = sum(estimate_tokens(x) for x in prompts_and_outputs)
    # Reserve 400 tokens per agent call for framework/task-envelope overhead.
    estimated += 4 * 400
    return {
        "estimated_total_tokens": estimated,
        "budget": MAX_TOTAL_TOKENS,
        "within_budget": estimated <= MAX_TOTAL_TOKENS,
        "max_completion_sum": sum(AGENT_MAX_COMPLETION.values()),
    }

def enforce_stage_budget(prompt: str, stage_completion_limit: int) -> None:
    # Each stage gets a hard ~700-token input envelope. Four envelopes + the
    # 3,300-token completion ceiling + 800-token framework reserve stay <= 7,500.
    prompt_tokens = estimate_tokens(prompt)
    if prompt_tokens > 700:
        raise RuntimeError(
            f"Token guard stopped this stage: prompt is estimated at "
            f"{prompt_tokens} tokens; stage input limit is 700."
        )


def enforce_budget(items: list[str]) -> None:
    snapshot = budget_snapshot(items)
    if not snapshot["within_budget"]:
        raise RuntimeError(
            f"Estimated workflow token usage {snapshot['estimated_total_tokens']} exceeds "
            f"the {MAX_TOTAL_TOKENS} token budget."
        )
