from app.models.action import ActionOwnership


def determine_ownership(
    owner: str | None,
    executive_name: str = "Arjun Malhotra",
) -> ActionOwnership:

    if not owner:
        return ActionOwnership.UNCLEAR

    if owner.strip().lower() == executive_name.strip().lower():
        return ActionOwnership.MY_ACTION

    return ActionOwnership.WAITING_ON_OTHER