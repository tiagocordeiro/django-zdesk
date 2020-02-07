from django import template

register = template.Library()


@register.filter(name='as_percentage_of')
def as_percentage_of(part, whole):
    try:
        return float(part) / whole * 100
    except (ValueError, ZeroDivisionError):
        return ""
