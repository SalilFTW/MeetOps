from app.graph.runner import run_meetops_agent


def main():
    print("=" * 60)
    print("MEETOPS DAILY BRIEF")
    print("=" * 60)

    print("\nRunning MeetOps agent...")

    result = run_meetops_agent(
        use_llm=True,
    )

    brief = result.get("daily_brief")

    if brief is None:
        print("Daily brief was not generated.")
        return

    print("-" * 60)

    print(f"\nExecutive: {brief.executive}")
    print(f"Brief date: {brief.brief_date}")

    print("\nSUMMARY")
    print("-" * 60)
    print(brief.summary)

    print("\nMY ACTIONS")
    print("-" * 60)

    for action in brief.my_actions:
        print(f"- {action.title}")
        print(f"  Deadline: {action.deadline_text}")
        print(f"  Status: {action.status.value}")

    print("\nDUE TODAY")
    print("-" * 60)

    for action in brief.due_today:
        print(f"- {action.title}")

    print("\nOVERDUE")
    print("-" * 60)

    for action in brief.overdue:
        print(f"- {action.title}")

    print("\nWAITING ON OTHERS")
    print("-" * 60)

    for action in brief.waiting_on_others:
        print(f"- {action.title}")

    print("\nUNCLEAR OWNERSHIP")
    print("-" * 60)

    for action in brief.unclear_actions:
        print(f"- {action.title}")

    print("\n" + "=" * 60)
    print("DAILY BRIEF COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()