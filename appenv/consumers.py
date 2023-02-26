import json
from asgiref.sync import async_to_sync
from asyncio import sleep
# from time import sleep
from random import randint

from channels.exceptions import StopConsumer
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from appenv.models import *
from channels.layers import get_channel_layer
import requests


class TemperatureChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        for i in range(1000):

            await self.send(json.dumps({'value': randint(20, 30)}))
            await sleep(1)

    async def disconnect(self, close_code):
        print(close_code)
        raise StopConsumer()
