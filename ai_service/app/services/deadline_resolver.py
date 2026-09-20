from datetime import date, datetime, timedelta

from app.models.action import Action, ActionStatus


def resolve_deadline(
    deadline_text: str | None,
    reference_date: date,
) -> date | None:
    if not deadline_text:
        return None

    text = deadline_text.strip().lower()

    if "tomorrow" in text:
        return reference_date + timedelta(days=1)

    if "today" in text:
        return reference_date

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    for weekday_name, weekday_number in weekdays.items():
        if weekday_name in text:
            difference = weekday_number - reference_date.weekday()

            # If the weekday is today, use today.
            if difference == 0:
                return reference_date

            # If the weekday has already occurred this week,
            # interpret it as the most recent occurrence.
            if difference < 0:
                return reference_date + timedelta(days=difference)

            # If the weekday is still ahead this week,
            # use the upcoming occurrence.
            return reference_date + timedelta(days=difference)

    if "this week" in text:
        return None

    return None


def apply_deadline_status(
    action: Action,
    reference_date: date,
) -> Action:
    resolved_date = resolve_deadline(
        action.deadline_text,
        reference_date,
    )

    if resolved_date is None:
        action.status = ActionStatus.OPEN
        return action

    action.deadline = datetime.combine(
        resolved_date,
        datetime.min.time(),
    )

    if action.status == ActionStatus.COMPLETED:
        return action

    if resolved_date < reference_date:
        action.status = ActionStatus.OVERDUE
    else:
        action.status = ActionStatus.OPEN

    return action