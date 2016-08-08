from contento.render_helpers import apply_text_processors

class TextModified(object):
    def render(self, content, context={}):
        return apply_text_processors("MODIFIED!: --- ::" +content)


from contento.render_helpers import apply_text_processors

class InstanceContext(object):
    def render(self, content, context={}):
        key = content["key"]
        return context["url_data"][key]
