import os.path
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='basename')
@stringfilter
def basename(value):
  return os.path.basename(value)

@register.filter(name='get_value')
def get_value(value, key):
  return value.get(key)

@register.filter(name='get_attr')
def get_attr(value, arg):
  return value.__getattribute__(arg)
