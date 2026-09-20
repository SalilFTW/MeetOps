"""
MeetOps Executive Productivity Agent - Orchestrator & Runner Script
"""

import subprocess
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
AI_DIR = BASE_DIR / "ai_service"
BACKEND_DIR = BASE_DIR / "backend"

sys.path.insert(0, str(AI_DIR))

from app.services.action_engine import extract_actions, group_actions


def print_brief(use_llm: bool = False):
    print("=" * 65)
    print("               MEETOPS - DAILY EXECUTIVE BRIEF               ")
    print("=" * 65)
    mode = "LLM Extractor (LangChain + Groq)" if use_llm else "Deterministic Baseline"
    print(f"Mode: {mode}\n")

    actions = extract_actions(use_llm=use_llm, resolve_duplicates=True)
    groups = group_actions(actions)

    print(f"Total Extracted Actions: {len(actions)}\n")

    sections = [
        ("MY ACTIONS (High Priority Commitments)", "my_actions"),
        ("WAITING ON OTHERS", "waiting_on_others"),
        ("UNCLEAR OWNERSHIP (Needs Review)", "unclear"),
    ]

    for title, key in sections:
        items = groups.get(key, [])
        print(f"--- {title} ({len(items)}) ---")
        if not items:
            print("  (None)\n")
            continue

        for action in items:
            print(f"* [{action.action_type.value.upper()}] {action.title}")
            print(f"  Owner:      {action.owner or 'Unassigned'}")
            if action.recipient:
                print(f"  Recipient:  {action.recipient}")
            print(f"  Deadline:   {action.deadline_text or 'No explicit deadline'}")
            print(f"  Confidence: {action.confidence if action.confidence is not None else 'N/A'}")
            if action.source_evidence:
                ev = action.source_evidence[0]
                print(f"  Source:     {ev.source_type} ({ev.source_id})")
                print(f"  Evidence:   \"{ev.excerpt}\"")
            if action.notes:
                print(f"  Notes:      {', '.join(action.notes)}")
            print()
    print("=" * 65)


def start_ai_service(port: int = 8000):
    import uvicorn

    print(f"Starting Python AI Service on http://127.0.0.1:{port} ...")
    print(f"Swagger Documentation: http://127.0.0.1:{port}/docs")
    uvicorn.run("app.main:app", app_dir=str(AI_DIR), host="127.0.0.1", port=port, reload=True)


def start_js_backend():
    print(f"Starting JavaScript Backend (Node.js/Express) ...")
    subprocess.run(["npm", "start", "--prefix", "backend"], shell=True, check=True)


def run_all_tests():
    print(">>> 1/2: Running Python AI Service Tests (pytest) ...")
    import pytest
    python_exit = pytest.main(["-q", str(AI_DIR / "tests")])

    print("\n>>> 2/2: Running JavaScript Backend Tests (node:test) ...")
    js_proc = subprocess.run(["npm", "test", "--prefix", "backend"], shell=True)

    if python_exit != 0 or js_proc.returncode != 0:
        sys.exit(1)
    print("\n[SUCCESS] All Python and JavaScript test suites passed!")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--ai" in args:
        start_ai_service()
    elif "--backend" in args:
        start_js_backend()
    elif "--test" in args:
        run_all_tests()
    elif "--llm" in args:
        print_brief(use_llm=True)
    else:
        print_brief(use_llm=False)
        print("\nAvailable flags:")
        print("  --ai       Start Python AI Microservice (port 8000)")
        print("  --backend  Start JavaScript Node.js Backend (port 3000)")
        print("  --test     Run both Python & JavaScript test suites")
        print("  --llm      Run LLM extraction brief (requires GROQ_API_KEY)")
