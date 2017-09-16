from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def nav_link(href, text, classes=''):
    classes = ' '.join(['nav-link', classes]).strip()
    template = '<a class="%(classes)s" href="%(href)s">%(text)s</a>'
    return mark_safe(template % {'classes': classes, 'href': href, 'text': text})
