from django import template
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.utils.module_loading import import_string
from ..render_helpers import render
from ..settings import CONTENTO_BACKEND


register = template.Library()

@register.simple_tag(takes_context=True)
def region(context, region_name):
    """
    renders a cms region
    expects a context var with the same name as the region
    """
    region_data = context.get(region_name, [])
    out = ""
    for content in region_data:
        out += render(content.get('type'), content.get('data'), context)

    #TODO: this is too weak. should be delegated to renders
    return mark_safe(out)


@register.simple_tag(takes_context=True)
def pages_tree(context, slug, template_name, depth=None, current_page=None,
    language=None):
    template = get_template(template_name)
    cms_backend = import_string(CONTENTO_BACKEND)()
    tree = cms_backend.get_tree(slug)

    return template.render({"nodes":tree})


@register.simple_tag(takes_context=True)
def fragment(context, content_type, content_data):
    """
    renders a cms fragment
    """
    out = render(content_type, content_data, context)
    return mark_safe(out)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
