# Generated by Django 5.1.6 on 2025-02-09 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("carrier_id", models.CharField(max_length=100)),
                ("carrier_name", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("coverage_details", models.JSONField(default=dict)),
                ("terms_and_conditions", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "active"),
                            ("selected", "selected"),
                            ("pending_confirmation", "pending_confirmation"),
                            ("confirmed", "confirmed"),
                            ("expired", "expired"),
                            ("rejected", "rejected"),
                        ],
                        default="active",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("selected_at", models.DateTimeField(blank=True, null=True)),
                ("confirmation_deadline", models.DateTimeField(blank=True, null=True)),
                ("confirmed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "bids",
            },
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("consumer_name", models.CharField(max_length=255)),
                ("consumer_email", models.EmailField(max_length=254)),
                ("consumer_phone", models.CharField(max_length=20)),
                ("coverage_type", models.CharField(max_length=100)),
                (
                    "coverage_amount",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                ("coverage_start_date", models.DateField()),
                ("coverage_details", models.JSONField(default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("bidding", "bidding"),
                            ("selecting", "selecting"),
                            ("confirming", "confirming"),
                            ("confirmed", "confirmed"),
                            ("expired", "expired"),
                            ("failed", "failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("bidding_start", models.DateTimeField(null=True)),
                ("bidding_end", models.DateTimeField(null=True)),
                ("retry_count", models.IntegerField(default=0)),
                ("last_retry_at", models.DateTimeField(blank=True, null=True)),
                (
                    "original_quote",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="retry_quotes",
                        to="marketplace.quote",
                    ),
                ),
                (
                    "selected_bid",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="selected_quotes",
                        to="marketplace.bid",
                    ),
                ),
            ],
            options={
                "db_table": "quotes",
            },
        ),
        migrations.AddField(
            model_name="bid",
            name="quote",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="marketplace.quote",
            ),
        ),
        migrations.AddIndex(
            model_name="quote",
            index=models.Index(fields=["status"], name="quotes_status_b396a9_idx"),
        ),
        migrations.AddIndex(
            model_name="quote",
            index=models.Index(fields=["created_at"], name="quotes_created_c74d71_idx"),
        ),
        migrations.AddIndex(
            model_name="quote",
            index=models.Index(
                fields=["consumer_email"], name="quotes_consume_573971_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bid",
            index=models.Index(
                fields=["quote", "status"], name="bids_quote_i_9d84cf_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bid",
            index=models.Index(
                fields=["carrier_id", "created_at"], name="bids_carrier_e5ce44_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="bid",
            index=models.Index(fields=["amount"], name="bids_amount_3a682b_idx"),
        ),
        migrations.AddConstraint(
            model_name="bid",
            constraint=models.CheckConstraint(
                condition=models.Q(("amount__gt", 0)), name="bid_amount_positive"
            ),
        ),
    ]
