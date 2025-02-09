# Register your models here.

from django.contrib import admin

from marketplace.models.bid import Bid
from marketplace.models.quote import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "consumer_name",
        "coverage_type",
        "coverage_amount",
        "status",
        "created_at",
        "retry_count",
    ]
    list_filter = ["status", "coverage_type"]
    search_fields = ["consumer_name", "consumer_email", "id"]
    readonly_fields = [
        "created_at",
        "bidding_start",
        "bidding_end",
        "retry_count",
        "last_retry_at",
    ]
    fieldsets = [
        (
            "Consumer Information",
            {
                "fields": [
                    "consumer_name",
                    "consumer_email",
                    "consumer_phone",
                ],
            },
        ),
        (
            "Coverage Details",
            {
                "fields": [
                    "coverage_type",
                    "coverage_amount",
                    "coverage_start_date",
                    "coverage_details",
                ],
            },
        ),
        (
            "Quote Status",
            {
                "fields": [
                    "status",
                    "created_at",
                    "bidding_start",
                    "bidding_end",
                ],
            },
        ),
        (
            "Retry Information",
            {
                "fields": [
                    "original_quote",
                    "retry_count",
                    "last_retry_at",
                ],
            },
        ),
    ]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "quote",
        "carrier_name",
        "amount",
        "status",
        "created_at",
    ]
    list_filter = ["status", "carrier_name"]
    search_fields = ["carrier_name", "carrier_id", "quote__consumer_name"]
    readonly_fields = [
        "created_at",
        "selected_at",
        "confirmation_deadline",
        "confirmed_at",
    ]
    fieldsets = [
        (
            "Bid Information",
            {
                "fields": [
                    "quote",
                    "carrier_id",
                    "carrier_name",
                    "amount",
                ],
            },
        ),
        (
            "Coverage Details",
            {
                "fields": [
                    "coverage_details",
                    "terms_and_conditions",
                ],
            },
        ),
        (
            "Bid Status",
            {
                "fields": [
                    "status",
                    "created_at",
                    "selected_at",
                    "confirmation_deadline",
                    "confirmed_at",
                ],
            },
        ),
    ]
