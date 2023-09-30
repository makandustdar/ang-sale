from django import template

register = template.Library()


@register.simple_tag()
def set_comma(value):
    value = float(value)
    return f'{value:,.0f}'
