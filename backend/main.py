# backend/main.py
from __future__ import annotations
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .checklist import RISK_PATTERNS
from .llm import analyze_with_llm
from .utils import extract_text_from_bytes

# 1) Load env first
load_dotenv()

# 2) Single app instance
app = FastAPI(title="Contract Reviewer MVP")

# 3) Single, explicit CORS config (no credentials needed)
ALLOWED_ORIGINS = [
    "http://127.0.0.1:3001",
    "http://localhost:3001",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Models ----
class AnalyzeIn(BaseModel):
    text: str = Field(min_length=30, description="Full contract text")

class AnalyzeOut(BaseModel):
    risks: List[Dict[str, Any]]
    missing_or_unclear: List[Dict[str, Any]]
    fix_suggestions: List[str]
    summary: List[str]
    heuristic_flags: List[Dict[str, str]]

# ---- Helpers ----
def _heuristic_scan(text: str) -> List[Dict[str, str]]:
    t = text.lower()
    flags = []
    for needle, label in RISK_PATTERNS:
        idx = t.find(needle)
        if idx != -1:
            snippet = text[max(0, idx - 60): idx + 60]
            flags.append({"label": label, "snippet": snippet.strip()})
    return flags

# ---- Routes ----
@app.post("/api/analyze", response_model=AnalyzeOut)
async def analyze(payload: AnalyzeIn):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(500, "Missing GROQ_API_KEY env var")
    heur = _heuristic_scan(payload.text)
    data = analyze_with_llm(payload.text, heur)
    return {**data, "heuristic_flags": heur}

@app.post("/api/analyze_file", response_model=AnalyzeOut)
async def analyze_file(file: UploadFile = File(...)):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(500, "Missing GROQ_API_KEY env var")
    blob = await file.read()
    text = extract_text_from_bytes(blob, file.filename, file.content_type)
    if len(text) < 30:
        raise HTTPException(400, "Could not extract enough text from file. Use PDF/DOCX/TXT with selectable text.")
    heur = _heuristic_scan(text)
    data = analyze_with_llm(text, heur)
    return {**data, "heuristic_flags": heur}

@app.get("/")
async def root():
    return {"ok": True, "service": "contract-reviewer"}
