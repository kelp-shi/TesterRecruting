from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='mask_password')
def mask_password(password):
    return '*' * len(password)