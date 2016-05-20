import pytz
from django import template

register = template.Library()


@register.assignment_tag
def get_timezone():
    return pytz.common_timezones


@register.filter(name='add_css_class')
def add_css_class(field, css_class):
    attrs = {'class': css_class}
    return field.as_widget(attrs=attrs)


@register.filter(name='has_group')
def has_group(user, group):
    return user.groups.filter(name=group).exists()


@register.filter('fieldtype')
def fieldtype(field):
        return field.field.widget.__class__.__name__
