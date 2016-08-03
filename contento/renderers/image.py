from contento.render_helpers import apply_text_processors

class Image(object):
    def render(self, content):
        src = content.get("src")
        klass = content.get("class", "")
        wrapper_class = content.get("wrapper_class", "")
        return "<div class='%s'><img class='%s' src='%s'/></div>" % (wrapper_class, klass, src)
