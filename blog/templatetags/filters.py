from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter('addattr')
def addattr(value, args):
    list_attr = {}
    for attr in args.split(','):
        name, val = attr.split(':')
        list_attr[name] = val
    return value.as_widget(attrs=list_attr)


@register.filter('rmattr')
def rmattr(value, attr):
    if attr in value.field.widget.attrs:
        del value.field.widget.attrs[attr]
    return value


@register.filter('markdowntext')
def markdowntext(value):
    html = markdown.markdown(value)
    return mark_safe(html)
