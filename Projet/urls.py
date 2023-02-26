"""Projet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appenv import views
from appenv import api_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('temperature/', views.temperature_view, name="temperature"),
    path('humidity/', views.humidity_view, name="humidity"),
    path("devices/", views.devices_view, name="devices"),
    path("logout/", views.logout_view, name="logout"),

    path("add_device/", views.add_device, name="add_device"),

    path('get_device_info/<int:id_device>/', views.get_device_info, name='get_device_info'),
    path('get_all_devices_info/', views.get_all_devices_info, name='get_all_devices_info'),

    path('change_device_status/<int:id_device>/', views.change_device_status, name='change_device_status'),
    path('delete_device/<int:id_device>/', views.delete_device, name='delete_device'),

    # REST API
    path('hello/', api_views.HelloView.as_view(), name='hello'),
    path('get_device/', api_views.GetDeviceView.as_view(), name='get_device'),
    path('get_current_temperature/', api_views.GetCurrentTemperature.as_view(), name='get_current_temperature'),
    path('get_current_humidity/', api_views.GetCurrentHumidity.as_view(), name='get_current_humidity'),
    path('get_temperature_30min/', api_views.GetTemperature30min.as_view(), name='get_temperature_30min'),
    path('get_humidity_30min/', api_views.GetHumidity30min.as_view(), name='get_humidity_30min'),
    path('get_temperature_1day/', api_views.GetTemperature1day.as_view(), name='get_humidity_1day'),
    path('get_humidity_1day/', api_views.GetHumidity1day.as_view(), name='get_humidity_1day'),

]
