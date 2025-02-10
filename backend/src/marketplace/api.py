from datetime import date
from decimal import Decimal
from typing import Any

from django.http import HttpRequest
from ninja import Router
from ninja import Schema
from ninja.errors import HttpError

from marketplace.models.quote import Quote
from marketplace.models.quote import QuoteStatus

router = Router()


class QuoteRequest(Schema):
    consumer_name: str
    consumer_email: str
    consumer_phone: str
    coverage_type: str
    coverage_amount: Decimal
    coverage_start_date: date
    coverage_details: dict[str, Any]


class QuoteResponse(Schema):
    id: int
    status: str
    consumer_name: str
    coverage_type: str
    coverage_amount: Decimal
    coverage_start_date: date
    created_at: date


@router.get("/health")
def health_check(request: HttpRequest) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/quotes", response=QuoteResponse)
def create_quote(request: HttpRequest, quote_data: QuoteRequest) -> dict[str, Any]:
    """Create a new quote request."""
    try:
        quote = Quote.objects.create(
            consumer_name=quote_data.consumer_name,
            consumer_email=quote_data.consumer_email,
            consumer_phone=quote_data.consumer_phone,
            coverage_type=quote_data.coverage_type,
            coverage_amount=quote_data.coverage_amount,
            coverage_start_date=quote_data.coverage_start_date,
            coverage_details=quote_data.coverage_details,
            status=QuoteStatus.PENDING.value,
        )
        return {
            "id": quote.pk,
            "status": quote.status,
            "consumer_name": quote.consumer_name,
            "coverage_type": quote.coverage_type,
            "coverage_amount": quote.coverage_amount,
            "coverage_start_date": quote.coverage_start_date,
            "created_at": quote.created_at.date(),
        }
    except Exception as err:
        raise HttpError(400, str(err)) from err
