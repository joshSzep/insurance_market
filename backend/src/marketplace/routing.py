from django.urls import re_path

from marketplace.consumers import QuoteBiddingConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/quotes/(?P<quote_id>\d+)/$",
        QuoteBiddingConsumer.as_asgi(),
    ),
]
