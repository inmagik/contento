from contento.render_helpers import apply_text_processors

class Text(object):
    def render(self, content, context={}):
        return apply_text_processors(content)
