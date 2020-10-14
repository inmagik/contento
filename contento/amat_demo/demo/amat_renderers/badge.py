from contento.renderers.text import Text
import markdown
from django.utils.module_loading import import_string
from django.template import Context, Template, loader



class Badge(Text):
    def render(self, content, context={}):

        required_data = self.get_required_fields(content)
        text = markdown.markdown(required_data.get("text"))
        title = content.get("title", "")
        columns = content.get("columns", 3)

        template = loader.get_template("amat_renderers/badge.html")
        ctx = Context(context)
        ctx["text"] = text
        ctx["title"] = title
        ctx["columns"] = columns
        
        return template.render(ctx)
