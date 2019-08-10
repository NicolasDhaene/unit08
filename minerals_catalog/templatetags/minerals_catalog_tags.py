from django import template

register = template.Library()


@register.filter
def human_read(value):
    return value.replace("_"," ")