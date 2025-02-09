"""Type stubs for channels.routing package."""

from typing import Any
from typing import Callable

class ProtocolTypeRouter:
    """Router for different protocols."""

    def __init__(self, application_mapping: dict[str, Any]) -> None: ...

class URLRouter:
    """Router for URL-based routing."""

    def __init__(self, routing: list[Any]) -> None: ...
