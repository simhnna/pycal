import pytz
from django import template

register = template.Library()

@register.assignment_tag
def get_timezone():
    return pytz.common_timezones
