from decimal import Decimal

import pytest
from django.db.utils import IntegrityError
from django.utils import timezone

from marketplace.models.bid import Bid
from marketplace.models.bid import BidStatus


@pytest.mark.django_db
def test_bid_creation(sample_bid: Bid) -> None:
    """Test basic bid creation."""
    assert sample_bid.id is not None
    assert sample_bid.status == BidStatus.ACTIVE.value
    assert sample_bid.carrier_name == "Best Insurance Co"
    assert sample_bid.amount == Decimal("1000.00")


@pytest.mark.django_db
def test_bid_str_representation(sample_bid: Bid) -> None:
    """Test the string representation of a bid."""
    expected = f"Bid {sample_bid.id} - Best Insurance Co - $1000.00 - active"
    assert str(sample_bid) == expected


@pytest.mark.django_db
def test_select_bid(sample_bid: Bid) -> None:
    """Test selecting a bid."""
    sample_bid.select()

    assert sample_bid.status == BidStatus.PENDING_CONFIRMATION.value
    assert sample_bid.selected_at is not None
    assert sample_bid.confirmation_deadline is not None

    # Check 30 second window
    time_diff = sample_bid.confirmation_deadline - sample_bid.selected_at
    assert time_diff.total_seconds() == 30


@pytest.mark.django_db
def test_confirm_bid(selected_bid: Bid) -> None:
    """Test confirming a selected bid."""
    selected_bid.confirm()

    assert selected_bid.status == BidStatus.CONFIRMED.value
    assert selected_bid.confirmed_at is not None


@pytest.mark.django_db
def test_confirm_bid_fails_if_not_selected(sample_bid: Bid) -> None:
    """Test that confirming an unselected bid fails."""
    with pytest.raises(ValueError, match="Bid is not pending confirmation"):
        sample_bid.confirm()


@pytest.mark.django_db
def test_confirm_bid_fails_if_expired(selected_bid: Bid) -> None:
    """Test that confirming an expired bid fails."""
    # Move confirmation deadline to the past
    selected_bid.confirmation_deadline = timezone.now() - timezone.timedelta(seconds=1)

    with pytest.raises(ValueError, match="Confirmation deadline has passed"):
        selected_bid.confirm()


@pytest.mark.django_db
def test_reject_bid(sample_bid: Bid) -> None:
    """Test rejecting a bid."""
    sample_bid.reject()
    assert sample_bid.status == BidStatus.REJECTED.value


@pytest.mark.django_db
def test_is_confirmation_expired(selected_bid: Bid) -> None:
    """Test checking if confirmation period has expired."""
    assert selected_bid.is_confirmation_expired() is False

    # Move deadline to the past
    selected_bid.confirmation_deadline = timezone.now() - timezone.timedelta(seconds=1)
    assert selected_bid.is_confirmation_expired() is True


@pytest.mark.django_db
def test_bid_amount_must_be_positive(active_quote) -> None:
    """Test that bid amount must be positive."""
    with pytest.raises(IntegrityError):
        Bid.objects.create(
            quote=active_quote,
            carrier_id="carrier123",
            carrier_name="Best Insurance Co",
            amount=Decimal("-1000.00"),
            coverage_details={"deductible": 500},
            terms_and_conditions="Standard terms apply",
        )
