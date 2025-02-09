from enum import Enum

from django.db import models
from django.utils import timezone

from marketplace.models.bid import Bid


class QuoteStatus(str, Enum):
    PENDING = "pending"  # Initial state when quote is created
    BIDDING = "bidding"  # Active bidding period (60 seconds)
    SELECTING = "selecting"  # Consumer selecting winner
    CONFIRMING = "confirming"  # Waiting for carrier confirmation (30 seconds)
    CONFIRMED = "confirmed"  # Bid confirmed by carrier
    EXPIRED = "expired"  # No bids or no selection made
    FAILED = "failed"  # Winner didn't confirm in time


class Quote(models.Model):
    # Consumer Information
    consumer_name = models.CharField(max_length=255)
    consumer_email = models.EmailField()
    consumer_phone = models.CharField(max_length=20)

    # Coverage Details
    coverage_type = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    coverage_start_date = models.DateField()
    coverage_details = models.JSONField(default=dict)

    # Quote Status
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in QuoteStatus],
        default=QuoteStatus.PENDING.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    bidding_start = models.DateTimeField(null=True)
    bidding_end = models.DateTimeField(null=True)

    # Selected Bid
    selected_bid = models.ForeignKey(
        Bid,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_quotes",
    )

    # Retry Tracking
    original_quote = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retry_quotes",
    )
    retry_count = models.IntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "quotes"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["consumer_email"]),
        ]

    def __str__(self) -> str:
        return f"Quote {self.id} - {self.consumer_name} - {self.status}"

    def start_bidding(self) -> None:
        """Start the bidding period for this quote."""
        self.status = QuoteStatus.BIDDING.value
        self.bidding_start = timezone.now()
        self.bidding_end = self.bidding_start + timezone.timedelta(seconds=60)
        self.save()

    def can_retry(self) -> bool:
        """Check if this quote can be retried."""
        if self.retry_count >= 1:
            return False

        if not self.last_retry_at:
            return True

        hours_since_retry = (timezone.now() - self.last_retry_at).total_seconds() / 3600
        return hours_since_retry >= 1

    def create_retry(self) -> "Quote":
        """Create a retry quote if allowed."""
        if not self.can_retry():
            raise ValueError("Cannot retry this quote")

        retry = Quote.objects.create(
            consumer_name=self.consumer_name,
            consumer_email=self.consumer_email,
            consumer_phone=self.consumer_phone,
            coverage_type=self.coverage_type,
            coverage_amount=self.coverage_amount,
            coverage_start_date=self.coverage_start_date,
            coverage_details=self.coverage_details,
            original_quote=self,
            retry_count=self.retry_count + 1,
        )

        self.last_retry_at = timezone.now()
        self.save()

        return retry
