# core/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def tiene_attr(obj, attr):
    return hasattr(obj, attr)

