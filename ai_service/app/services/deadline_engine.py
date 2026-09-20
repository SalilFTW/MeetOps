from datetime import datetime

from app.models.action import ActionStatus


def determine_status(
    deadline: datetime | None,
    current_time: datetime | None = None,
    completed: bool = False,
) -> ActionStatus:

    if completed:
        return ActionStatus.COMPLETED

    if deadline is None:
        return ActionStatus.OPEN

    if current_time is None:
        return ActionStatus.OPEN

    if deadline < current_time:
        return ActionStatus.OVERDUE

    return ActionStatus.OPEN