from django.utils.module_loading import import_string
from contento.settings import CONTENTO_TEXT_PROCESSORS
import re


def load_renderer(content_type):
    pieces = content_type.split(".")
    if len(pieces) < 2:
        content_type = "contento.renderers." + content_type

    return import_string(content_type)()


def render(content_type, content_data, page_context={}):
    """
    """
    try:
        renderer = load_renderer(content_type)
        return renderer.render(content_data, context=page_context)
    except Exception, e:
        return render_error(content_type, content_data, str(e))



def apply_text_processors(text):
    """
    applies processors defined in CONTENTO_TEXT_PROCESSORS
    Used by renderers that output texts.
    """
    for processor_name in CONTENTO_TEXT_PROCESSORS:
        processor = import_string(processor_name)()
        text = processor.process(text)
    return text


def render_error(content_type, content_data, msg):
    return "<div class='alert alert-danger'>Cannot render content <b>%s</b>:<pre>%s</pre>Error:<pre>%s</pre></div>" % (content_type, content_data, msg)


def get_regions_from_template(template):
    exp = '{%\s+region\s+"(?P<region_name>\w+)"\s%}'
    reg = re.compile(exp)
    out = []
    for match in reg.finditer(template):
        out.append(match.group('region_name'))
    out = list(set(out))
    return out
