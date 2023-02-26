from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import *
from django.contrib.auth.forms import PasswordResetForm
from django.urls.resolvers import LocalePrefixPattern
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
# from django_echarts.starter.sites import DJESite
# from django_echarts.entities import Copyright
from appenv.fonctions import *
from appenv.models import *
from appenv.forms import *
from datetime import datetime
import json
from django.db.models.functions import Cast
from django.db.models import TextField

base_url = 'BASE_URL'
token_headers = {'Authorization': 'Token xxxxxxxxxxxx'}


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            if user is not None:
                login(request, user)
                url = '/dashboard/'
                return redirect(url)
            else:
                form = AuthenticationForm()
                messages.error(
                    request, "Username or password is incorrect")
                return redirect(request.META.get('HTTP_REFERER'), {'form': form})
        except Exception:
            messages.error(request, "Le groupe n'existe pas")
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'title': 'Se connecter', 'form': form})


def logout_view(request):
    messages.success(request, "You have successfully logged out")
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def dashboard_view(request):
    r = requests.get(base_url + '/get_device/', headers=token_headers)
    list_device = r.json()
    dashboard_data = []

    for device in list_device:
        if device["status"]:
            id_device = device["id"]
            request_param = {'id_device': id_device}

            r = requests.get(base_url + '/get_current_temperature/', params=request_param, headers=token_headers)
            if r.status_code != 200:
                current_temperature = None
                formatted_timestamp = datetime.now()
            else:
                temperature_object_curr = r.json()
                current_temperature = temperature_object_curr['temperature']
                timestamp = temperature_object_curr['sample_time']
                dt = datetime.fromisoformat(timestamp)
                formatted_timestamp = dt.strftime("%d/%m/%Y %H:%M:%S")

            r = requests.get(base_url + '/get_current_humidity/', params=request_param, headers=token_headers)
            if r.status_code != 200:
                current_humidity = None
                formatted_timestamp = datetime.now()
            else:
                humidity_object_curr = r.json()
                current_humidity = humidity_object_curr['humidity']

            dashboard_data.append({
                "is_active": True,
                "device_id": id_device,
                "device_name": device["name"],
                "last_update_time": formatted_timestamp,
                "current_temperature": current_temperature,
                "current_humidity": current_humidity,
            })
        else:
            dashboard_data.append({
                "is_active": False,
                "device_name": device["name"],
            })

    return render(request, "home/dashboard.html", {'dashboard_data': dashboard_data})


@login_required(login_url='/login/')
def temperature_view(request):
    # get devices
    r = requests.get(base_url + '/get_device/', headers=token_headers)
    list_device = r.json()
    temperature_data = []

    for device in list_device:
        if device["status"]:
            id_device = device["id"]
            request_param = {'id_device': id_device}

            r = requests.get(base_url + '/get_current_temperature/', params=request_param, headers=token_headers)
            if r.status_code != 200:
                current_temperature = None
                formatted_timestamp = datetime.now()
            else:
                temperature_object_curr = r.json()
                current_temperature = temperature_object_curr['temperature']
                timestamp = temperature_object_curr['sample_time']
                dt = datetime.fromisoformat(timestamp)
                formatted_timestamp = dt.strftime("%d/%m/%Y %H:%M:%S")

            r = requests.get(base_url + '/get_temperature_30min/', params=request_param, headers=token_headers)
            temperature_objects_30min = r.json()

            r = requests.get(base_url + '/get_temperature_1day/', params=request_param, headers=token_headers)
            temperature_objects_1day = r.json()

            temperature_data.append({
                "is_active": True,
                "device_id": id_device,
                "device_name": device["name"],
                "last_update_time": formatted_timestamp,
                "current_temperature": current_temperature,
                "temperature_objects_30min": temperature_objects_30min,
                "temperature_objects_1day": temperature_objects_1day,
            })
        else:
            temperature_data.append({
                "is_active": False,
                "device_name": device["name"],
            })

    return render(request, 'home/temperature.html', {"temperature_data": temperature_data})


@login_required(login_url='/login/')
def humidity_view(request):
    # get devices
    r = requests.get(base_url + '/get_device/', headers=token_headers)
    list_device = r.json()
    humidity_data = []

    for device in list_device:
        if device["status"]:
            id_device = device["id"]
            request_param = {'id_device': id_device}

            r = requests.get(base_url + '/get_current_humidity/', params=request_param, headers=token_headers)
            if r.status_code != 200:
                current_humidity = None
                formatted_timestamp = datetime.now()
            else:
                humidity_object_curr = r.json()
                current_humidity = humidity_object_curr['humidity']
                timestamp = humidity_object_curr['sample_time']
                dt = datetime.fromisoformat(timestamp)
                formatted_timestamp = dt.strftime("%d/%m/%Y %H:%M:%S")

            r = requests.get(base_url + '/get_humidity_30min/', params=request_param, headers=token_headers)
            humidity_objects_30min = r.json()

            r = requests.get(base_url + '/get_humidity_1day/', params=request_param, headers=token_headers)
            humidity_objects_1day = r.json()

            humidity_data.append({
                "is_active": True,
                "device_id": id_device,
                "device_name": device["name"],
                "last_update_time": formatted_timestamp,
                "current_humidity": current_humidity,
                "humidity_objects_30min": humidity_objects_30min,
                "humidity_objects_1day": humidity_objects_1day,
            })
        else:
            humidity_data.append({
                "is_active": False,
                "device_name": device["name"],
            })

    return render(request, 'home/humidity.html', {"humidity_data": humidity_data})


@login_required(login_url='/login/')
def devices_view(request):
    devices = Device.objects.all()
    return render(request, 'home/devices.html', {'devices': devices})


@login_required(login_url='/login/')
def get_device_info(request, id_device=-1):
    info = None
    if id_device != -1:
        device = Device.objects.get(device_id=id_device)
        info = {
            "type": device.device_type,
            "gpio": device.gpio,
            "status": device.active
        }

    return JsonResponse(info, safe=False)


@login_required(login_url='/login/')
def get_all_devices_info(request):
    info = []
    devices = Device.objects.all()
    for d in devices:
        info.append({
            "id": d.device_id,
            "type": d.device_type,
            "gpio": d.gpio,
            "status": d.active
        })
    return JsonResponse(info, safe=False)


@login_required(login_url='/login/')
def add_device(request):
    if not has_group(request.user, "admin"):
        messages.error(request, 'You have no right to take this action')
        return redirect('/devices/')

    if request.method == 'POST' and 'submit_device' in request.POST:
        # try:
        device_form = DeviceForm(request.POST)
        # if device_form.is_valid():
        device_form.save()
        messages.success(request, 'The device is added')
        return redirect('/devices/')
        # else:
        #     messages.error(request, 'Error to add the device')
    # except Exception:
    #     messages.error(request, 'Error to add the device')
    device_form = DeviceForm()

    return render(request, "home/addDevice.html", {'device_form': device_form})


@login_required(login_url='/login/')
def change_device_status(request, id_device=-1):
    if not has_group(request.user, "admin"):
        # messages.error(request, 'You have no right to take this action')
        info = {
            "success": False,
        }
        return JsonResponse(info, safe=False)
    else:
        info = None
        if id_device != -1:
            device = Device.objects.get(device_id=id_device)
            device.active = not device.active
            device.save()
            info = {
                "success": True,
                "status": device.active,
            }

        return JsonResponse(info, safe=False)


@login_required(login_url='/login/')
def delete_device(request, id_device=-1):
    if not has_group(request.user, "admin"):
        messages.error(request, 'You have no right to take this action')
    else:
        info = None
        if id_device != -1:
            device = Device.objects.get(device_id=id_device)
            device.delete()
            messages.success(request, "The device has been deleted")
        else:
            messages.error(request, "Error in deleting the device")
    return redirect('/devices/')
