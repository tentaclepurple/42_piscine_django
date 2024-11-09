# articles/templatetags/article_extras.py

from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def truncate_chars(value, max_length=20):
    """Truncate text to a specified number of characters with ellipsis."""
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value

@register.filter
def time_since(value):
    """Display the time since the article was created."""
    return timesince(value) + " ago"
