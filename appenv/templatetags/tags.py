from django import template
from django.template.defaulttags import register

register = template.Library()


@register.filter
def get_value(dictionary, key):
    return dictionary.get(str(key))
