from django import template
from django.template import Variable

register = template.Library()

    
@register.filter(name="display_grade")
def display_grade(value):
    return str(value).replace('.', ',')[:3]
