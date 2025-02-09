from datetime import date
from decimal import Decimal

import pytest
from django.utils import timezone

from marketplace.models.quote import Quote
from marketplace.models.quote import QuoteStatus


@pytest.mark.django_db
def test_quote_creation(sample_quote: Quote) -> None:
    """Test basic quote creation."""
    assert sample_quote.id is not None
    assert sample_quote.status == QuoteStatus.PENDING.value
    assert sample_quote.consumer_name == "John Doe"
    assert sample_quote.coverage_amount == Decimal("50000.00")
    assert sample_quote.retry_count == 0


@pytest.mark.django_db
def test_start_bidding(sample_quote: Quote) -> None:
    """Test starting the bidding process."""
    sample_quote.start_bidding()
    
    assert sample_quote.status == QuoteStatus.BIDDING.value
    assert sample_quote.bidding_start is not None
    assert sample_quote.bidding_end is not None
    
    # Check 60 second window
    time_diff = sample_quote.bidding_end - sample_quote.bidding_start
    assert time_diff.total_seconds() == 60


@pytest.mark.django_db
def test_can_retry_initial(sample_quote: Quote) -> None:
    """Test that a new quote can be retried."""
    assert sample_quote.can_retry() is True


@pytest.mark.django_db
def test_can_retry_after_one_hour(sample_quote: Quote) -> None:
    """Test retry after one hour cooldown."""
    # Create first retry
    retry = sample_quote.create_retry()
    assert retry.retry_count == 1
    
    # Should not be able to retry immediately
    assert retry.can_retry() is False
    
    # Move time forward one hour
    retry.last_retry_at = timezone.now() - timezone.timedelta(hours=1, minutes=1)
    assert retry.can_retry() is False  # Still false because retry_count >= 1


@pytest.mark.django_db
def test_create_retry_preserves_data(sample_quote: Quote) -> None:
    """Test that retry preserves original quote data."""
    retry = sample_quote.create_retry()
    
    assert retry.id != sample_quote.id
    assert retry.consumer_name == sample_quote.consumer_name
    assert retry.consumer_email == sample_quote.consumer_email
    assert retry.coverage_amount == sample_quote.coverage_amount
    assert retry.coverage_details == sample_quote.coverage_details
    assert retry.original_quote == sample_quote
    assert retry.retry_count == 1


@pytest.mark.django_db
def test_create_retry_fails_when_not_allowed(sample_quote: Quote) -> None:
    """Test that retry fails when not allowed."""
    # Create first retry
    retry = sample_quote.create_retry()
    
    # Attempt second retry
    with pytest.raises(ValueError, match="Cannot retry this quote"):
        retry.create_retry()


@pytest.mark.django_db
def test_quote_with_selected_bid(sample_quote: Quote, sample_bid) -> None:
    """Test quote with a selected bid."""
    sample_quote.selected_bid = sample_bid
    sample_quote.save()
    
    assert sample_quote.selected_bid.carrier_name == "Best Insurance Co"
    assert sample_quote.selected_bid.amount == Decimal("1000.00")
