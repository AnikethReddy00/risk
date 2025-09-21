# backend/utils.py
from __future__ import annotations
import json, re
from typing import Any, Dict

JSON_FENCE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)

def coerce_json(text: str) -> Dict[str, Any]:
    """Try to parse JSON from raw model output. Accepts fenced blocks or raw."""
    if not text:
        return {}
    m = JSON_FENCE.search(text)
    raw = m.group(1) if m else text
    # Remove trailing commas and fix common issues lightly
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    try:
        return json.loads(raw)
    except Exception:
        # Try to find first/last brace
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start : end + 1])
            except Exception:
                pass
    return {}

# --- File extraction helpers ---
from io import BytesIO
from typing import Optional
from pypdf import PdfReader
from docx import Document
import chardet

MAX_CHARS = 120_000  # guardrail for token limits

def _decode_bytes_guess(b: bytes) -> str:
    if not b:
        return ""
    guess = chardet.detect(b) or {}
    enc = (guess.get("encoding") or "utf-8").lower()
    try:
        return b.decode(enc, errors="replace")
    except Exception:
        return b.decode("utf-8", errors="replace")

def extract_text_from_bytes(content: bytes, filename: Optional[str], content_type: Optional[str]) -> str:
    name = (filename or "").lower()
    ct = (content_type or "").lower()
    try:
        if ct == "application/pdf" or name.endswith(".pdf"):
            reader = PdfReader(BytesIO(content))
            parts = []
            for page in reader.pages[:400]:
                parts.append(page.extract_text() or "")
            text = "\n\n".join(parts)
        elif ct in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",) or name.endswith(".docx"):
            doc = Document(BytesIO(content))
            text = "\n".join(p.text for p in doc.paragraphs)
        elif name.endswith((".txt", ".md")) or ct.startswith("text/"):
            text = _decode_bytes_guess(content)
        else:
            text = _decode_bytes_guess(content)
    except Exception:
        text = _decode_bytes_guess(content)
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[...truncated...]"
    return text
