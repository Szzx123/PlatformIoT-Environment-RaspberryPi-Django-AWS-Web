from channels.routing import ProtocolTypeRouter
from django.urls import re_path
from django.urls import path
from appenv import consumers

websocket_urlpatterns = [
    # re_path(r'ws/charts/(?P<room>[0-9]+)/$', consumers.ChartsConsumer.as_asgi()),
    path('ws/temperature_realtime_chart/', consumers.TemperatureChartConsumer.as_asgi()),
    # re_path(r'ws/temperature_realtime_chart/(?P<room_name>\w+)/$', consumers.TemperatureChartConsumer.as_asgi()),

]
