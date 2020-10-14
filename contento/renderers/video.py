from contento.exceptions import RendererConfigError
from django.utils.module_loading import import_string
from django.template import Context, Template, loader
from .base import BaseRenderer
import uuid

class Video(BaseRenderer):
    required_fields = ["movie_url"]
    json_schema = {
        "title": "Video",
    	"properties": {
    		"width": {
    			"type": "number",
                "propertyOrder": 1
            },
            "height": {
    			"type": "number",
                "propertyOrder": 2
            },
            "movie_url": {
    			"type": "string",
                "propertyOrder": 3
            },
            "fullscreen": {
    			"type": "boolean",
                "propertyOrder": 4
            },
            "wrapper_class": {
    			"type": "string",
                "propertyOrder": 5
            }
    	},
    	"required": ["movie_url"]
    }


    def get_provider_context(self, movie_url):
        if movie_url.find("youtube") != -1:
            pieces = movie_url.split("watch?v=")
            if len(pieces) == 2:
                return {"youtube_id" : pieces[1]}

        if movie_url.find("vimeo.com") != -1:
            pieces = movie_url.split("vimeo.com/")
            if len(pieces) == 2:
                return {"vimeo_id" : pieces[1]}

        return {}

    def render(self, content, context={}):
        required_data = self.get_required_fields(content)
        template = loader.get_template("contento/video.html")

        ctx = Context(context)
        ctx["video_context"] = content
        ctx["video_context"]["wrapper_id"] = "video-"+str(uuid.uuid4())
        ctx["video_context"].update(self.get_provider_context(content["movie_url"]))


        return template.render(context)
