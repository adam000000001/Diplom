from django import template

register = template.Library()

@register.filter
def divisibleby(value, arg):
    try:
        return int(value) / int(arg) * 100
    except (ValueError, ZeroDivisionError):
        return 0