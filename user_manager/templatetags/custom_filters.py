from django import template

register = template.Library()

@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)


@register.filter
def char_count(value):
    if not isinstance(value, str):
        return 0
    return len(value)