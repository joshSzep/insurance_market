from datetime import timedelta
from enum import Enum

from django.db import models
from django.utils import timezone


class BidStatus(str, Enum):
    ACTIVE = "active"  # Bid is active and can be selected
    SELECTED = "selected"  # Bid was selected by consumer
    PENDING_CONFIRMATION = "pending_confirmation"  # Waiting for carrier confirmation
    CONFIRMED = "confirmed"  # Carrier confirmed the bid
    EXPIRED = "expired"  # Bid expired (quote closed)
    REJECTED = "rejected"  # Carrier rejected or failed to confirm


class Bid(models.Model):
    # Relationships
    quote = models.ForeignKey(
        "Quote",
        on_delete=models.CASCADE,
        related_name="bids",
    )

    # Carrier Information
    carrier_id = models.CharField(max_length=100)
    carrier_name = models.CharField(max_length=255)

    # Bid Details
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    coverage_details = models.JSONField(default=dict)
    terms_and_conditions = models.TextField()

    # Bid Status
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in BidStatus],
        default=BidStatus.ACTIVE.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    selected_at = models.DateTimeField(null=True, blank=True)
    confirmation_deadline = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "bids"
        indexes = [
            models.Index(fields=["quote", "status"]),
            models.Index(fields=["carrier_id", "created_at"]),
            models.Index(fields=["amount"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="bid_amount_positive",
                condition=models.Q(amount__gt=0),
            ),
        ]

    def __str__(self) -> str:
        return f"Bid {self.pk} - {self.carrier_name} - ${self.amount} - {self.status}"

    def select(self) -> None:
        """Mark this bid as selected by the consumer."""
        self.status = BidStatus.PENDING_CONFIRMATION.value
        self.selected_at = timezone.now()
        self.confirmation_deadline = self.selected_at + timedelta(seconds=30)
        self.save()

    def confirm(self) -> None:
        """Confirm this bid by the carrier."""
        if self.status != BidStatus.PENDING_CONFIRMATION.value:
            raise ValueError("Bid is not pending confirmation")

        if timezone.now() > self.confirmation_deadline:
            raise ValueError("Confirmation deadline has passed")

        self.status = BidStatus.CONFIRMED.value
        self.confirmed_at = timezone.now()
        self.save()

    def reject(self) -> None:
        """Reject or expire this bid."""
        self.status = BidStatus.REJECTED.value
        self.save()

    def is_confirmation_expired(self) -> bool:
        """Check if the confirmation period has expired."""
        if self.status != BidStatus.PENDING_CONFIRMATION.value:
            return False

        if not self.confirmation_deadline:
            return False

        return timezone.now() > self.confirmation_deadline
