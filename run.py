"""
MeetOps Executive Productivity Agent - Runner Script
"""

import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR if (BASE_DIR / "app").exists() else BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.action_engine import extract_actions, group_actions


def print_brief(use_llm: bool = False):
    print("=" * 65)
    print("               MEETOPS - DAILY EXECUTIVE BRIEF               ")
    print("=" * 65)
    mode = "LLM Extractor (LangChain + Groq)" if use_llm else "Deterministic Baseline"
    print(f"Mode: {mode}\n")

    actions = extract_actions(use_llm=use_llm)
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


def start_server(port: int = 8000):
    import uvicorn

    print(f"Starting MeetOps API on http://127.0.0.1:{port} ...")
    print(f"Swagger Documentation: http://127.0.0.1:{port}/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--server" in args:
        start_server()
    elif "--llm" in args:
        print_brief(use_llm=True)
    elif "--test" in args:
        import pytest
        sys.exit(pytest.main(["-q", str(BACKEND_DIR / "tests")]))
    else:
        print_brief(use_llm=False)
        print("\nTip: Run with '--server' to start the web API (uvicorn).")
        print("Tip: Run with '--llm' to use LLM extraction (requires GROQ_API_KEY).")
        print("Tip: Run with '--test' to run pytest.")
