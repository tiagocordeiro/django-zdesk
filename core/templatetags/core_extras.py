import locale

from django import template

register = template.Library()


@register.filter(name='as_percentage_of')
def as_percentage_of(part, whole):
    try:
        return float(part) / whole * 100
    except (ValueError, ZeroDivisionError):
        return ""


@register.filter(name='currency_display')
def currency_display(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(valor, grouping=True, symbol=None)
    return valor
