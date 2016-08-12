from contento.exceptions import RendererConfigError
from django.utils.module_loading import import_string
from django.template import Context, Template, loader
from .base import BaseRenderer
import uuid

class LeafletMap(BaseRenderer):
    required_fields = ["lat", "lon"]
    json_schema = {
        "title": "LeafletMap",
    	"properties": {
    		"lat": {
    			"type": "number",
                "propertyOrder": 1
            },
            "lon": {
    			"type": "number",
                "propertyOrder": 2
            },
            "wrapper_class": {
    			"type": "string",
                "propertyOrder": 3
            }
    	},
    	"required": ["lat", "lon"]
    }

    def render(self, content, context={}):
        required_data = self.get_required_fields(content)
        template = loader.get_template("contento/leaflet_map.html")
        ctx = Context(context)
        ctx["map_context"] = required_data
        ctx["map_context"]["wrapper_id"] = "map-"+str(uuid.uuid4())
        ctx["map_context"]["markers"] = content.get("markers", [])
        ctx["map_context"]["wrapper_class"] = content.get("wrapper_class", [])
        return template.render(context)
