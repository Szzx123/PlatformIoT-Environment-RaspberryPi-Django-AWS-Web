from django import template
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import request

from appenv.models import *

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False
    
