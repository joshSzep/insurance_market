from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer  # type: ignore
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from marketplace.models.bid import Bid
from marketplace.models.quote import Quote


@dataclass
class BidUpdate:
    bid_id: int
    carrier_name: str
    amount: Decimal
    status: str


class QuoteBiddingConsumer(AsyncJsonWebsocketConsumer):
    """WebSocket consumer for real-time bid updates on a quote."""

    quote_id: str
    room_group_name: str

    async def connect(self) -> None:
        """Handle WebSocket connection."""
        # Get quote_id from URL route
        self.quote_id = self.scope["url_route"]["kwargs"]["quote_id"]
        self.room_group_name = f"quote_{self.quote_id}"

        # Join the quote group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # Send initial quote state
        try:
            quote: Quote = await Quote.objects.aget(pk=self.quote_id)
            bids: QuerySet[Bid] = Bid.objects.filter(quote_id=self.quote_id).order_by(
                "amount"
            )
            bid_list: list[Bid] = [bid async for bid in bids]
            await self.send_quote_state(quote, bid_list)
        except ObjectDoesNotExist:
            await self.close()

    async def disconnect(self, close_code: int) -> None:
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content: dict[str, Any]) -> None:
        """Handle incoming WebSocket messages (not used in this consumer)."""
        pass  # Read-only WebSocket, no incoming messages handled

    async def quote_update(self, event: dict[str, Any]) -> None:
        """Handle quote status updates."""
        await self.send_json(
            {
                "type": "quote_update",
                "quote_id": self.quote_id,
                "status": event["status"],
                "message": event["message"],
            }
        )

    async def bid_update(self, event: dict[str, Any]) -> None:
        """Handle new bid notifications."""
        await self.send_json(
            {
                "type": "bid_update",
                "quote_id": self.quote_id,
                "bid": event["bid"],
            }
        )

    async def send_quote_state(self, quote: Quote, bids: list[Bid]) -> None:
        """Send current quote state to the client."""
        await self.send_json(
            {
                "type": "quote_state",
                "quote_id": quote.pk,
                "status": quote.status,
                "bidding_end": quote.bidding_end.isoformat()
                if quote.bidding_end
                else None,
                "bids": [
                    {
                        "bid_id": bid.pk,
                        "carrier_name": bid.carrier_name,
                        "amount": str(bid.amount),
                        "status": bid.status,
                        "created_at": bid.created_at.isoformat(),
                    }
                    for bid in bids
                ],
            }
        )
