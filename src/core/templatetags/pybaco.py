from django import template

from baco import Baco, base16


register = template.Library()


@register.filter(name='hex_to_base62')
def hex_to_base62(value):
    return Baco.to_62(value, base16)


@register.filter(name='hex_to_base62_first_6')
def hex_to_base62_first_6(value):
    return Baco.to_62(value, base16)[:6]

