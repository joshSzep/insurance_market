import asyncio
from typing import Any

from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from marketplace.models.bid import Bid
from marketplace.models.quote import Quote
from marketplace.models.quote import QuoteStatus


async def send_quote_update(quote_id: int, status: str, message: str) -> None:
    """Send quote update to WebSocket group asynchronously."""
    channel_layer = get_channel_layer()
    room_group_name = f"quote_{quote_id}"

    await channel_layer.group_send(
        room_group_name,
        {
            "type": "quote_update",
            "status": status,
            "message": message,
        },
    )


async def send_bid_update(bid: Bid) -> None:
    """Send bid update to WebSocket group asynchronously."""
    channel_layer = get_channel_layer()
    room_group_name = f"quote_{bid.quote.pk}"

    await channel_layer.group_send(
        room_group_name,
        {
            "type": "bid_update",
            "bid": {
                "bid_id": bid.pk,
                "carrier_name": bid.carrier_name,
                "amount": str(bid.amount),
                "status": bid.status,
                "created_at": bid.created_at.isoformat(),
            },
        },
    )


@receiver(post_save, sender=Quote)
def handle_quote_update(
    sender: type[Quote],
    instance: Quote,
    created: bool,
    **kwargs: Any,
) -> None:
    """Handle quote status updates and notify WebSocket clients."""
    # Prepare status message based on quote state
    message = "Quote status updated"
    match instance.status:
        case QuoteStatus.BIDDING.value:
            message = "Bidding period has started"
        case QuoteStatus.SELECTING.value:
            message = "Bidding period has ended"
        case QuoteStatus.CONFIRMING.value:
            message = f"Waiting for {instance.selected_bid.carrier_name} to confirm"
        case QuoteStatus.CONFIRMED.value:
            message = f"Quote confirmed with {instance.selected_bid.carrier_name}"
        case QuoteStatus.EXPIRED.value:
            message = "Quote expired without selection"
        case QuoteStatus.FAILED.value:
            message = "Selected carrier failed to confirm"

    # Schedule async task to send update
    asyncio.create_task(
        send_quote_update(
            quote_id=instance.pk,
            status=instance.status,
            message=message,
        ),
    )


@receiver(post_save, sender=Bid)
def handle_bid_update(
    sender: type[Bid],
    instance: Bid,
    created: bool,
    **kwargs: Any,
) -> None:
    """Handle bid updates and notify WebSocket clients."""
    # Schedule async task to send update
    asyncio.create_task(send_bid_update(instance))
