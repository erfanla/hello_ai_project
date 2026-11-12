"""The only errors that services raise.

Routes do not catch them. One handler in `app/main.py` turns them into pages:
NotFound -> 404, NotAllowed -> 403, InvalidState -> 409.
"""


class ServiceError(Exception):
    """Base class for all service errors."""


class NotFound(ServiceError):
    """The thing does not exist, or the User may not see it."""


class NotAllowed(ServiceError):
    """The User may see the thing, but may not do this action."""


class InvalidState(ServiceError):
    """The action does not fit the current state (for example: already done)."""
