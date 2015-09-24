import pytz
from django import template

register = template.Library()


@register.assignment_tag
def get_timezone():
    return pytz.common_timezones


@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder):
    attrs = {'placeholder': placeholder, 'required': '', 'class': 'form-control'}

    return field.as_widget(attrs=attrs)


@register.filter(name='add_placeholder_unrequired')
def add_placeholder_unrequired(field, placeholder):
    attrs = {'placeholder': placeholder, 'class': 'form-control'}

    return field.as_widget(attrs=attrs)


@register.filter(name='add_css')
def add_css(field):
    attrs = {'class': 'form-control'}
    return field.as_widget(attrs=attrs)


@register.filter(name='has_group')
def has_group(user, group):
    return user.groups.filter(name=group).exists()

@register.filter('fieldtype')
def fieldtype(field):
        return field.field.widget.__class__.__name__
