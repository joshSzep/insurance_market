from datetime import date
from decimal import Decimal

import pytest

from marketplace.models.bid import Bid
from marketplace.models.quote import Quote


@pytest.fixture
def sample_quote() -> Quote:
    """Create a sample quote for testing."""
    return Quote.objects.create(
        consumer_name="John Doe",
        consumer_email="john@example.com",
        consumer_phone="555-0123",
        coverage_type="auto",
        coverage_amount=Decimal("50000.00"),
        coverage_start_date=date(2025, 3, 1),
        coverage_details={"vehicle": "Tesla Model 3"},
    )


@pytest.fixture
def active_quote(sample_quote: Quote) -> Quote:
    """Create a quote that is in active bidding state."""
    sample_quote.start_bidding()
    return sample_quote


@pytest.fixture
def sample_bid(active_quote: Quote) -> Bid:
    """Create a sample bid for testing."""
    return Bid.objects.create(
        quote=active_quote,
        carrier_id="carrier123",
        carrier_name="Best Insurance Co",
        amount=Decimal("1000.00"),
        coverage_details={"deductible": 500},
        terms_and_conditions="Standard terms apply",
    )


@pytest.fixture
def selected_bid(sample_bid: Bid) -> Bid:
    """Create a bid that has been selected by the consumer."""
    sample_bid.select()
    return sample_bid
