"""LogicPilot — FastAPI Backend with all module endpoints."""

import json
import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.groq_client import call_groq, call_groq_stream
from utils.code_runner import run_code

app = FastAPI(title="LogicPilot API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _clean_json(raw: str) -> str:
    """Strip markdown fences from LLM JSON responses."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
    return cleaned.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CODE RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

class CodeRunRequest(BaseModel):
    code: str
    language: str = "python"
    stdin: str = ""


@app.post("/api/run")
async def run_code_endpoint(req: CodeRunRequest):
    stdout, stderr = run_code(req.code, req.language, req.stdin)
    return {"output": stdout, "error": stderr}


# ═══════════════════════════════════════════════════════════════════════════════
# 2. COMPILER CHATBOT (AI Mentor)
# ═══════════════════════════════════════════════════════════════════════════════

class MentorRequest(BaseModel):
    message: str
    code: str = ""
    language: str = "python"
    history: list = []


@app.post("/api/mentor")
async def logic_mentor(req: MentorRequest):
    from modules.logic_engine import SYSTEM_PROMPT

    # Build context from recent history
    history_text = ""
    for msg in req.history[-6:]:
        role = "Student" if msg.get("role") == "user" else "LogicAI"
        history_text += f"{role}: {msg.get('content', '')}\n"

    prompt = (
        f"Code context ({req.language}):\n```\n{req.code}\n```\n\n"
        f"{history_text}"
        f"Student: {req.message}"
    )

    resp = call_groq(SYSTEM_PROMPT, prompt)
    return {"reply": resp}


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DEBUGGER — Start Session
# ═══════════════════════════════════════════════════════════════════════════════

class DebugStartRequest(BaseModel):
    code: str
    error: str


@app.post("/api/debug/start")
async def debug_start(req: DebugStartRequest):
    from modules.debugger import SYSTEM_PROMPT_INIT

    prompt = f"Broken code:\n```\n{req.code}\n```\n\nError/problem: {req.error}"
    raw = call_groq(SYSTEM_PROMPT_INIT, prompt)

    try:
        data = json.loads(_clean_json(raw))
        return {"success": True, "data": data}
    except Exception:
        return {
            "success": True,
            "data": {
                "initial_observation": "",
                "first_question": raw,
                "hint_print_statement": "",
                "bug_category": "unknown",
            },
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DEBUGGER — Continue Conversation
# ═══════════════════════════════════════════════════════════════════════════════

class DebugRespondRequest(BaseModel):
    message: str
    history: list = []


@app.post("/api/debug/respond")
async def debug_respond(req: DebugRespondRequest):
    from modules.debugger import SYSTEM_PROMPT_FOLLOWUP

    context = "\n".join(
        f"{'LogicAI' if m.get('role') == 'assistant' else 'Context' if m.get('role') == 'context' else 'Student'}: {m.get('content', '')}"
        for m in req.history[-6:]
    )
    context += f"\nStudent: {req.message}"

    full_resp = ""
    for chunk in call_groq_stream(SYSTEM_PROMPT_FOLLOWUP, context):
        full_resp += chunk

    return {"reply": full_resp}


# ═══════════════════════════════════════════════════════════════════════════════
# 5. VISUALIZER — Generate Steps
# ═══════════════════════════════════════════════════════════════════════════════

class VisualizeRequest(BaseModel):
    code: str
    language: str = "python"


@app.post("/api/visualize")
async def visualize_code(req: VisualizeRequest):
    from modules.visualizer import SYSTEM_PROMPT

    raw = call_groq(
        SYSTEM_PROMPT,
        f"Visualize this {req.language} code step by step:\n\n```\n{req.code}\n```",
    )

    try:
        data = json.loads(_clean_json(raw))
        return {"success": True, "data": data}
    except Exception:
        return {"success": False, "error": "Failed to parse visualization", "raw": raw[:500]}


# ═══════════════════════════════════════════════════════════════════════════════
# 6. OPTIMIZER — Analyze & Optimize
# ═══════════════════════════════════════════════════════════════════════════════

class OptimizeRequest(BaseModel):
    code: str
    language: str = "python"


@app.post("/api/optimize/analyze")
async def optimize_analyze(req: OptimizeRequest):
    from modules.optimizer import SYSTEM_PROMPT_ANALYZE

    raw = call_groq(
        SYSTEM_PROMPT_ANALYZE,
        f"Analyse this {req.language} code:\n\n```\n{req.code}\n```",
    )

    try:
        data = json.loads(_clean_json(raw))
        return {"success": True, "data": data}
    except Exception:
        return {"success": False, "error": "Failed to parse analysis", "raw": raw[:500]}


# ═══════════════════════════════════════════════════════════════════════════════
# 7. OPTIMIZER — Tutor Chat
# ═══════════════════════════════════════════════════════════════════════════════

class OptChatRequest(BaseModel):
    message: str
    code: str = ""
    analysis_context: str = ""
    history: list = []


@app.post("/api/optimize/chat")
async def optimize_chat(req: OptChatRequest):
    from modules.optimizer import SYSTEM_PROMPT_CHAT

    history_text = "\n".join(
        f"{'Student' if m.get('role') == 'user' else 'LogicAI'}: {m.get('content', '')}"
        for m in req.history[-6:]
    )

    prompt = f"{req.analysis_context}\n\n{history_text}\nStudent: {req.message}"

    full_resp = ""
    for chunk in call_groq_stream(SYSTEM_PROMPT_CHAT, prompt):
        full_resp += chunk

    return {"reply": full_resp}


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
