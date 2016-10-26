from contento.render_helpers import apply_text_processors
from .base import BaseRenderer
import markdown


class Text(BaseRenderer):
    required_fields = ["text"]
    json_schema = {

        "title": "Text",
    	#"type": "object",
    	"properties": {
    		"text": {
    			"type": "string",
                #  "format": "html"
    		}
    	},
    	"required": ["text"]
    }

    def render(self, content, context={}):
        required_data = self.get_required_fields(content)
        text = markdown.markdown(required_data.get("text"))
        return apply_text_processors(text)
