from chat import consumers

from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^wss$', consumers.ChatConsumer),
]
