from django.utils.module_loading import import_string
from contento.settings import CONTENTO_TEXT_PROCESSORS

def render(content, page_context={}):
    """
    """
    klass_string = content.get("type")
    pieces = klass_string.split(".")
    if len(pieces) < 2:
        klass_string = "contento.renderers." + klass_string
    try:
        renderer = import_string(klass_string)()
        return renderer.render(content.get("data", {}), context=page_context)
    except ImportError, e:
        return render_error(content, str(e))



def apply_text_processors(text):
    """
    applies processors defined in CONTENTO_TEXT_PROCESSORS
    Used by renderers that output texts.
    """
    for processor_name in CONTENTO_TEXT_PROCESSORS:
        processor = import_string(processor_name)()
        text = processor.process(text)
    return text


def render_error(content, msg):
    return "<div class='alert alert-danger'>Error rendering content:<pre>%s</pre>Error:<pre>%s</pre></div>" % (content, msg)
