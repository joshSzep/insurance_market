"""Type stubs for channels package."""

from typing import Any
from typing import Protocol

class ChannelLayer(Protocol):
    """Protocol for channel layer implementations."""

    async def group_add(self, group: str, channel: str) -> None: ...
    async def group_discard(self, group: str, channel: str) -> None: ...
    async def group_send(self, group: str, message: dict[str, Any]) -> None: ...
