from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Device)
admin.site.register(Temperature)
admin.site.register(Humidity)
