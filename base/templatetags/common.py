from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter()
def update_variable(value):
    data = value
    return data


@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


@register.filter()
def dict_to_list(dict_obj):
    return list(dict_obj)
