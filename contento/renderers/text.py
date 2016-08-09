from contento.render_helpers import apply_text_processors
from .base import BaseRenderer

class Text(BaseRenderer):
    required_fields = ["text"]
    json_schema = {

        #"title": "Example Schema",
    	#"type": "object",
    	"properties": {
    		"text": {
    			"type": "string",
                 "format": "html"
    		}
    	},
    	"required": ["text"]
    }

    def render(self, content, context={}):
        required_data = self.get_required_fields(content)
        return apply_text_processors(required_data.get("text"))
