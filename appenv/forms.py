from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.db.models.fields import DateField
from django.db.models.query import QuerySet
from django.forms import widgets
from django.forms.widgets import DateTimeInput
from appenv.models import *
from appenv.fonctions import *


class DeviceForm(forms.ModelForm):
    types = [
        ('11', 'dht11'),
    ]
    type_c_empty = [('', '-- Device type --')] + types

    class Meta:
        model = Device
        fields = ('device_id', 'device_name', 'device_type', 'gpio', 'active')

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['device_id'].widget = forms.NumberInput()
        self.fields['device_name'].widget = forms.TextInput(attrs={'placeholder': 'Name', 'autocomplete': 'off',
                                                                   'maxlength': '14'})
        self.fields['device_type'].choices = [('', '-- Type --'), ] + list(self.fields['device_type'].choices)[1:]
        self.fields['gpio'].widget = forms.NumberInput()
