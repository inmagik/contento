from contento.render_helpers import apply_text_processors
from .base import BaseRenderer


class Image(BaseRenderer):
    def render(self, content, context={}):
        src = content.get("src")
        klass = content.get("class", "")
        wrapper_class = content.get("wrapper_class", "")
        return "<div class='%s'><img class='%s' src='%s'/></div>" % (wrapper_class, klass, src)
