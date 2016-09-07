import re
import json
from django.utils.module_loading import import_string
from contento.settings import CONTENTO_TEXT_PROCESSORS


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


def get_inline_renderer_config(inline_definition):
    """
    This method can be used to extract a renderer configuration from an inline definition
    such as:

    some_plugin|{ "some" : 'arg' }

    """
    pieces = inline_definition.split("|")
    #TODO: test length of splitted pieces
    renderer_klass = pieces[0].strip()
    string_args = pieces[1]
    args = json.loads(string_args)
    return renderer_klass, args


def render_inlines(text, page_context={}):
    """
    Replaces all inline renderers definitions with the renderer config.
    Example:

    Some text here (: Text|{ "text" : "hello" }  :) with a plugin in the middle.
    And one at the end (: Text|{ "text" : "bye!" } :)
    """
    inline_definitions = []
    inline_configurations = []
    regex_exp = re.compile("\(:(?P<inline_def>.+?):\)")
    def replacer(match):
        definition = match.group('inline_def')
        renderer_klass, args = get_inline_renderer_config(definition)
        rendered_content = render(renderer_klass, args, page_context)
        return rendered_content

    new_text = regex_exp.sub(replacer, text)


    return new_text
