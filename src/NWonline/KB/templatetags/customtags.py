from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

def id(value):
    return "#id_%s" % (value.html_name)

def generate(value, cssClass=""):
    "Generates a form input field including label and error messages"
    html = "<label class=\"%s\" for=\"id_%s\">%s</label> " % (cssClass, value.html_name, value.label)
    if value.errors:
        html += "<span class=\"error\">"
    html += "%s %s" % (force_unicode(value), str(value.errors))
    if value.errors:
        html += "</span>"
        
    return mark_safe(html)

register.filter('generate', generate)
register.filter('id', id)
