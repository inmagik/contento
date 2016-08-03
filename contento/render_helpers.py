from django.utils.module_loading import import_string
from contento.settings import CONTENTO_TEXT_PROCESSORS

def render(content):
    """
    """
    klass_string = content.get("type")
    pieces = klass_string.split(".")
    if len(pieces) < 2:
        klass_string = "contento.renderers." + klass_string
    renderer = import_string(klass_string)()
    return renderer.render(content.get("data"))


def apply_text_processors(text):
    """
    applies processors defined in CONTENTO_TEXT_PROCESSORS
    Used by renderers that output texts.
    """
    for processor_name in CONTENTO_TEXT_PROCESSORS:
        processor = import_string(processor_name)()
        text = processor.process(text)
    return text
