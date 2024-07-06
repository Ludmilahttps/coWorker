from django import template

register = template.Library()

@register.filter
def make_list(value, arg):
    return range(value, arg)

@register.filter
def range_filter(start, end=None):
    if end is None:
        end = start
        start = 0
    return range(start, end)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)