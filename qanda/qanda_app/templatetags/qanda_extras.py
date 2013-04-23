from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import pprint
import re

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=False)
@stringfilter
def url_target_blank(text):
	return mark_safe(re.sub("<a([^>]+)(?<!target=)>",'<a target="_blank"\\1>', text))


def template_print(value):
	print '>>>>>>>>>>>TEMPLATE_DEBUG_PRINT<<<<<<<<<<<<<<'
	pprint.pprint(value)
	print '>>>>>>>>>>>TEMPLATE_DEBUG_PRINT<<<<<<<<<<<<<<'
	return u''

register.simple_tag(template_print)

# url_target_blank.is_safe = True
# url_target_blank = register.filter(url_target_blank)