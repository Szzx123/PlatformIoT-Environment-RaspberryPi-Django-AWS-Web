import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from appenv.models import *
import datetime


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class GetDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        info = []
        devices = Device.objects.all()
        for d in devices:
            info.append({
                "id": d.device_id,
                "name": d.device_name,
                "type": d.device_type,
                "gpio": d.gpio,
                "status": d.active
            })
        return Response(info)


class GetCurrentTemperature(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        temp_object = Temperature.objects.filter(device__device_id=id_device).last()
        info = {
            "sample_time": str(temp_object.sample_time),
            "temperature": temp_object.temperature
        }

        return Response(info)  # {'sample_time': '2022-12-29 18:25:05.041852+00:00', 'temperature': 20.0}


class GetCurrentHumidity(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        temp_object = Humidity.objects.filter(device__device_id=id_device).last()
        info = {
            "sample_time": str(temp_object.sample_time),
            "humidity": temp_object.humidity
        }

        return Response(info)  # {'sample_time': '2022-12-29 18:25:05.041852+00:00', 'temperature': 20.0}


class GetTemperature30min(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        temp_objects = Temperature.objects.filter(device__device_id=id_device, sample_time__gte=created_time).values_list('sample_time',
                                                                                             'temperature')
        return Response(temp_objects)


class GetHumidity30min(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        humi_objects = Humidity.objects.filter(device__device_id=id_device, sample_time__gte=created_time).values_list('sample_time',
                                                                                          'humidity')
        return Response(humi_objects)


class GetTemperature1day(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        created_time = datetime.datetime.now() - datetime.timedelta(days=1)
        temp_objects = Temperature.objects.filter(device__device_id=id_device, sample_time__gte=created_time).values_list('sample_time',
                                                                                             'temperature')
        return Response(temp_objects)


class GetHumidity1day(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id_device = self.request.query_params.get('id_device')
        created_time = datetime.datetime.now() - datetime.timedelta(days=1)
        humi_objects = Humidity.objects.filter(device__device_id=id_device, sample_time__gte=created_time).values_list(
            'sample_time',
            'humidity')
        return Response(humi_objects)
