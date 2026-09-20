from app.models.action import (
    Action,
    ActionOwnership,
    ActionStatus,
    ActionType,
)
from app.services.action_extractor import create_action


EXECUTIVE = "Arjun Malhotra"


def extract_assignment1_actions() -> list[Action]:
    """
    Deterministic baseline actions derived from explicit Assignment 1 evidence.

    This is not an LLM extractor.
    It establishes the expected Action representation
    before LLM-based extraction is introduced.
    """

    actions: list[Action] = []

    # ---------------------------------------------------------
    # 1. Vendor list
    # ---------------------------------------------------------

    actions.append(
        create_action(
            action_id="action_vendor_list",
            title="Send updated vendor list",
            owner=EXECUTIVE,
            recipient="Raghav Sethi",
            ownership=ActionOwnership.MY_ACTION,
            action_type=ActionType.COMMITMENT,
            source_type="meeting_transcript",
            source_id="meeting_leadership_sync_2026-09-21",
            excerpt=(
                "I told Raghav I’d send him the updated vendor list. "
                "I’ll get that to him by end of day tomorrow."
            ),
            deadline_text="by end of day tomorrow",
            confidence=0.98,
        )
    )

    # ---------------------------------------------------------
    # 2. Meridian Logistics call
    # ---------------------------------------------------------

    actions.append(
        create_action(
            action_id="action_meridian_call",
            title="Reconfirm the new Meridian Logistics call time",
            owner=EXECUTIVE,
            recipient="Priya Nair",
            ownership=ActionOwnership.MY_ACTION,
            action_type=ActionType.FOLLOW_UP,
            source_type="meeting_transcript",
            source_id="meeting_leadership_sync_2026-09-21",
            excerpt=(
                "Client call with Meridian Logistics got pushed. "
                "I need to reconfirm the new time with their team myself."
            ),
            deadline_text=None,
            confidence=0.97,
        )
    )

    # ---------------------------------------------------------
    # 3. Expense variance report
    # ---------------------------------------------------------

    actions.append(
        create_action(
            action_id="action_expense_variance",
            title="Receive and review July expense variance report",
            owner="Divya Rao",
            recipient=EXECUTIVE,
            ownership=ActionOwnership.WAITING_ON_OTHER,
            action_type=ActionType.TASK,
            source_type="meeting_transcript",
            source_id="meeting_leadership_sync_2026-09-21",
            excerpt=(
                "Divya, can you also pull the July expense variance report "
                "before Thursday’s board prep? Yes, I’ll have it ready "
                "Wednesday evening."
            ),
            deadline_text="Wednesday evening",
            confidence=0.96,
        )
    )

    # ---------------------------------------------------------
    # 4. Q3 campaign deck
    # ---------------------------------------------------------

    actions.append(
        create_action(
            action_id="action_campaign_deck_review",
            title="Review Q3 campaign deck",
            owner=EXECUTIVE,
            recipient="Neha Kapoor",
            ownership=ActionOwnership.MY_ACTION,
            action_type=ActionType.TASK,
            source_type="meeting_transcript",
            source_id="meeting_leadership_sync_2026-09-21",
            excerpt=(
                "The campaign deck review — I said Wednesday, "
                "but realistically Thursday morning is safer."
            ),
            deadline_text="Thursday morning",
            confidence=0.94,
        )
    )

    # ---------------------------------------------------------
    # 5. Mumbai office lease
    # ---------------------------------------------------------

    actions.append(
        create_action(
            action_id="action_mumbai_lease",
            title="Confirm ownership of Mumbai office lease renewal signature",
            owner=None,
            recipient=None,
            ownership=ActionOwnership.UNCLEAR,
            action_type=ActionType.FOLLOW_UP,
            source_type="meeting_transcript",
            source_id="meeting_leadership_sync_2026-09-21",
            excerpt=(
                "Mumbai office renewal paperwork needs someone to sign off "
                "this week. Not sure whose desk that’s on right now."
            ),
            deadline_text="this week",
            confidence=0.99,
            notes=[
                "Ownership is explicitly unclear.",
                "Do not assume Facilities owns the task.",
            ],
        )
    )

    return actions


def get_my_actions() -> list[Action]:
    return [
        action
        for action in extract_assignment1_actions()
        if action.ownership == ActionOwnership.MY_ACTION
    ]


def get_waiting_on_others() -> list[Action]:
    return [
        action
        for action in extract_assignment1_actions()
        if action.ownership == ActionOwnership.WAITING_ON_OTHER
    ]


def get_unclear_actions() -> list[Action]:
    return [
        action
        for action in extract_assignment1_actions()
        if action.ownership == ActionOwnership.UNCLEAR
    ]