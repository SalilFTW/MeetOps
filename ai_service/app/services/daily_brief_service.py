from datetime import date

from app.models.action import Action, ActionStatus
from app.models.daily_brief import DailyBrief
from app.services.deadline_resolver import apply_deadline_status


EXECUTIVE = "Arjun Malhotra"


def build_daily_brief(
    actions: list[Action],
    reference_date: date,
) -> DailyBrief:

    processed_actions: list[Action] = []

    for action in actions:
        processed_action = apply_deadline_status(
            action=action,
            reference_date=reference_date,
        )

        processed_actions.append(processed_action)

    my_actions = [
        action
        for action in processed_actions
        if action.owner == EXECUTIVE
    ]

    due_today = [
        action
        for action in my_actions
        if action.deadline is not None
        and action.deadline.date() == reference_date
        and action.status != ActionStatus.COMPLETED
    ]

    overdue = [
        action
        for action in my_actions
        if action.status == ActionStatus.OVERDUE
    ]

    waiting_on_others = [
        action
        for action in processed_actions
        if action.ownership.value == "waiting_on_other"
    ]

    unclear_actions = [
        action
        for action in processed_actions
        if action.ownership.value == "unclear"
    ]

    summary = build_summary(
        my_actions=my_actions,
        due_today=due_today,
        overdue=overdue,
        waiting_on_others=waiting_on_others,
        unclear_actions=unclear_actions,
    )

    return DailyBrief(
        executive=EXECUTIVE,
        brief_date=reference_date,
        my_actions=my_actions,
        due_today=due_today,
        overdue=overdue,
        waiting_on_others=waiting_on_others,
        unclear_actions=unclear_actions,
        summary=summary,
    )


def build_summary(
    my_actions: list[Action],
    due_today: list[Action],
    overdue: list[Action],
    waiting_on_others: list[Action],
    unclear_actions: list[Action],
) -> str:

    return (
        f"{len(my_actions)} executive actions, "
        f"{len(due_today)} due today, "
        f"{len(overdue)} overdue, "
        f"{len(waiting_on_others)} waiting on others, "
        f"and {len(unclear_actions)} with unclear ownership."
    )