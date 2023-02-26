from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# from djongo import models
# from pynamodb.models import Model
from django.db.models.deletion import CASCADE


class Device(models.Model):
    device_id = models.PositiveIntegerField(primary_key=True)
    device_name = models.CharField(max_length=50)
    # device_type = models.IntegerField()
    TYPE_CHOICES = [
        (11, 'dht11'),
    ]
    device_type = models.IntegerField(choices=TYPE_CHOICES)
    gpio = models.PositiveIntegerField()
    active = models.BooleanField(null=True, default=True)


class Temperature(models.Model):
    device = models.ForeignKey(Device, on_delete=CASCADE, null=False)
    temperature = models.FloatField()
    sample_time = models.DateTimeField(auto_now_add=True)


class Humidity(models.Model):
    device = models.ForeignKey(Device, on_delete=CASCADE, null=False)
    humidity = models.FloatField()
    sample_time = models.DateTimeField(auto_now_add=True)


