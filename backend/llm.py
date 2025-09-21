from __future__ import annotations
import os
from typing import Any, Dict, List
from groq import Groq
from .checklist import CLAUSE_CHECKLIST
from .utils import coerce_json

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_SYSTEM = (
    "You are a contract risk reviewer."
    " Return STRICT JSON only."
)

_TEMPLATE = f"""
You are given a contract. Perform four tasks:
1) RISKS: List the top 3-10 concrete risk findings with short quotes from the contract and why they are risky.
2) MISSING_OR_UNCLEAR: Given this checklist, mark which items are missing or unclear and explain briefly.
CHECKLIST: {CLAUSE_CHECKLIST}
3) FIX_SUGGESTIONS: Provide crisp edit suggestions or sample clauses (concise, neutral tone).
4) SUMMARY: Write a plain-English summary (8-12 bullets, non-legalese).

Output JSON ONLY in this exact schema:
{{
  "risks": [{{"quote": str, "why": str, "severity": "low|medium|high"}}],
  "missing_or_unclear": [{{"item": str, "note": str}}],
  "fix_suggestions": [str],
  "summary": [str]
}}

Guidelines:
- Be specific and actionable.
- If something is fine, omit it.
- Prefer brevity.
"""


def analyze_with_llm(
    text: str, heuristic_flags: List[Dict[str, str]] | None = None
) -> Dict[str, Any]:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    hints = "" if not heuristic_flags else (
        "Heuristic flags found before LLM: "
        + "; ".join(f"{h['label']}: '{h['snippet']}'" for h in heuristic_flags)
    )
    user = f"CONTRACT:\n\n{text}\n\n{hints}"

    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=1800,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": _TEMPLATE},
            {"role": "user", "content": user},
        ],
    )
    out = resp.choices[0].message.content
    data = coerce_json(out)
    # Ensure keys exist
    return {
        "risks": data.get("risks", []),
        "missing_or_unclear": data.get("missing_or_unclear", []),
        "fix_suggestions": data.get("fix_suggestions", []),
        "summary": data.get("summary", []),
    }
