# myapp/templatetags/number_to_word.py

from django import template
from num2words import num2words  # Library to convert numbers to words (install using pip install num2words)

register = template.Library()

@register.filter
def number_to_words(value):
    try:
        return num2words(value)
    except (ValueError, TypeError):
        return value  # If it fails to convert, return the original number
