from django import template
from django.forms import widgets

register = template.Library()

@register.inclusion_tag('formfield.html')
def formfield(field):
    widget = field.field.widget
    type_ = None
    if isinstance(widget, widgets.Input):
        type_ = 'input'
    elif isinstance(widget, widgets.Textarea):
        type_ = 'textarea'
    elif isinstance(widget, widgets.Select):
        type_ = 'select'
    elif isinstance(widget, widgets.CheckboxInput):
        type_ = 'checkbox'
    elif isinstance(widget, widgets.RadioInput):
        type_ = 'radio'

    return {'field': field, 'form': field.form, 'type': type_}
