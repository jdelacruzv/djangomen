from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe
import nh3

from blog.richtext import sanitize_rich_text


register = template.Library()


@register.filter
def rich_text(value):
    if not value:
        return ""
    if not nh3.is_html(value):
        return linebreaksbr(value)
    return mark_safe(sanitize_rich_text(value))
