import hashlib
# from .models import *
import datetime
import os
from datetime import datetime
from functools import partial
from uuid import uuid4
from django.core.exceptions import ValidationError
import requests
from datetime import datetime

from .models import *
from django.db.models import Max
from django.db.models.functions import ExtractMinute
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from random import randint


def has_group(user, name):
    if user.groups.filter(name=name):
        return True
    else:
        return False


def get_current_temperature(request, id_device):
    # if request.is_ajax():  # Pop up transport
    latest_minute = Temperature.objects.aggregate(mx=Max(ExtractMinute('sample_time'))['mx'])
    latest_sheets = Temperature.objects.annotate(
        mn=ExtractMinute('sample_time')
    ).filter(mn=latest_minute)

    latest_temperature = Temperature.objects.last()
    current_temperature = Temperature.objects.get(device__device_id=id_device, sample_time=datetime.now())
    result = current_temperature.temperature
    return result


def send_chart_data():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '0',
        {
            'value': randint(20, 30)
        }
    )





