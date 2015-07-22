import pytz
from django import template

register = template.Library()

@register.assignment_tag
def get_timezone():
    return pytz.common_timezones

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder):
    attrs = {}
    attrs['placeholder'] = placeholder
    attrs['required'] =''
    attrs['class'] = 'form-control'

    return field.as_widget(attrs=attrs)

@register.filter(name='add_placeholder_unrequired')
def add_placeholder_unrequired(field, placeholder):
    attrs = {}
    attrs['placeholder'] = placeholder
    attrs['class'] = 'form-control'

    return field.as_widget(attrs=attrs)

@register.filter(name='has_group')
def has_group(user, group):
    return user.groups.filter(name=group).exists()
