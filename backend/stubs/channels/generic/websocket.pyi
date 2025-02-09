"""Type stubs for channels.generic.websocket package."""

from collections.abc import Callable
from typing import Any
from typing import TypeVar

T = TypeVar("T", bound="AsyncJsonWebsocketConsumer")

class AsyncJsonWebsocketConsumer:
    """Base class for async JSON WebSocket consumers."""

    channel_layer: Any
    channel_name: str
    scope: dict[str, Any]

    async def accept(self) -> None: ...
    async def close(self, code: int | None = None) -> None: ...
    async def send_json(self, content: dict[str, Any]) -> None: ...
    @classmethod
    def as_asgi(cls: type[T]) -> Callable[..., Any]: ...
