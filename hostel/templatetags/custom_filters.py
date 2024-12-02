# hostel/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def length_is(value, arg):
    """Check if the length of value is equal to the argument (arg)."""
    try:
        return len(value) == int(arg)
    except TypeError:
        return False  # Return False if value is not iterable (like an int)
