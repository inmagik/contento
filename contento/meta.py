import re
import json
from django.utils.module_loading import import_string
from contento.settings import CONTENTO_TEXT_PROCESSORS, CONTENTO_RENDERERS
from django.template import loader
from contento import renderers as core_renderers


def get_regions_from_template(template, load=False):
    exp = '{%\s+region\s+"(?P<region_name>\w+)"\s%}'
    reg = re.compile(exp)
    out = []
    if load:
        tpl = loader.get_template(template)
        template = open(tpl.origin.name, 'r').read()

    for match in reg.finditer(template):
        out.append(match.group('region_name'))
    out = list(set(out))
    return out


def get_contento_renderers():

    RENDERERS = []
    for x in dir(core_renderers):
        o = getattr(core_renderers, x);
        try:
            sub = issubclass(o, core_renderers.base.BaseRenderer)
        except:
            continue
        if sub:
            RENDERERS.append("contento.renderers.%s" % x)

    extra_renderers =  CONTENTO_RENDERERS or []
    return RENDERERS + extra_renderers

def get_contento_renderers_schemas():
    rs = get_contento_renderers()
    out = {}
    for r in rs:
        klass = import_string(r)
        json_schema = getattr(klass, "json_schema")
        if json_schema:
            out[r] = json_schema
    return out
