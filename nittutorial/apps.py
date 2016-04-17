from django.apps import AppConfig
from django import template

class NittutorialConfig(AppConfig):
    name = 'nittutorial'

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})