import yattag
import markdown
import datetime

from django import template
from django.contrib import messages
from django.utils.safestring import mark_safe

from dakis.website import menus as website_menus
from dakis.website.helpers import formrenderer

register = template.Library()


@register.simple_tag(takes_context=True)
def topmenu(context):
    if 'active_topmenu_item' in context:
        current = context['active_topmenu_item']
    else:
        current = context.request.resolver_match.url_name

    doc, tag, text = yattag.Doc().tagtext()
    with tag('ul', klass='nav navbar-nav top-menu'):
        for item in website_menus.menus['topmenu']:
            is_active = current == item.name
            classes = 'active' if is_active else ''
            with tag('li', role='presentation', klass=classes):
                with tag('a', href=item.url()):
                    text(item.label)
    return doc.getvalue()


@register.simple_tag(name='messages', takes_context=True)
def messages_tag(context):
    level_mappig = {
        messages.SUCCESS: 'success',
        messages.INFO: 'info',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
    }

    doc, tag, text = yattag.Doc().tagtext()
    for message in messages.get_messages(context['request']):
        level = level_mappig.get(message.level, 'info')
        with tag('div', klass='alert alert-%s' % level, role='alert'):
            text(str(message))
    return doc.getvalue()


@register.filter(name='markdown')
def markdown_tag(value):
    return mark_safe(markdown.markdown(value, extensions=['markdown.extensions.attr_list']))


@register.filter(name='timedelta')
def timedelta_filter(value):
    value_str = str(datetime.timedelta(seconds=value))
    if '.' in value_str:
        return value_str[:-5]
    return value_str


@register.simple_tag(name='formrenderer', takes_context=True)
def formrenderer_filter(context, form):
    return mark_safe(formrenderer.render_fields(context['request'], form))


@register.filter
def idx(d, key):
    return d[key]

@register.filter(name='cls')
def add_class(field, cls):
    field.field.widget.attrs['class'] = cls
    return field

@register.filter(name='fields')
def join_fields_of_forms(form1, form2, *args, **kwargs):
    fields = []
    for form in [form1, form2]:
        if type(form) == list:
            fields += form
        else:
            fields += form.visible_fields()
            fields += form.hidden_fields()
    return fields


@register.filter
def sort_exp_fields(fields):
    ordered_labels = ['Description', 'Algorithm title', 'Source code repository', 'Branch', 'Executable',
     'Algorithm details', 'Problem title', 'Input parameters', 'Result display discribing parameters',
     'Is major', 'Status', 'Not valid', 'Mistakes',  'Parent']
    sorted_fields = []
    for label in ordered_labels:
        for field in fields:
            if label == str(field.label):
                sorted_fields.append(field)
    return sorted_fields


@register.filter
def format(value):
    try:
        return "%g" % value
    except:
        if value:
            return value
    return '–'


@register.filter
def not_major_exp_children(exp):
    return exp.children.order_by('-created').filter(is_major=False)
