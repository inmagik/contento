from contento.exceptions import RendererConfigError
from django.utils.module_loading import import_string
from django.template import Context, Template, loader
from .base import BaseRenderer

def render_param(param, context):

    if type(param) == str or type(param) == unicode:
        template = Template(param)
        context = Context(context)
        return template.render(context)
    return param



class ModelInstanceTemplate(BaseRenderer):

    required_fields = ['template_name', 'model_name', 'model_pk']

    json_schema = {
        "title": "ModelInstanceTemplate",
    	"properties": {
    		"template_name": {
    			"type": "string",
                "propertyOrder": 1
            },
            "model_name": {
    			"type": "string",
                "propertyOrder": 2
            },
            "model_pk": {
    			"type": "string",
                "propertyOrder": 3
            },
    	},
    	"required": ["template_name", "model_name", "model_pk"]
    }

    def render(self, content, context={}):
        required_data = self.get_required_fields(content)
        required_data = {x:render_param(required_data[x], context) for x in required_data}
        template = loader.get_template(required_data["template_name"])
        model_klass = import_string(required_data["model_name"])
        obj = model_klass.objects.get(pk=int(required_data["model_pk"]))

        ctx = Context(context)
        ctx["object"] = obj

        return template.render(ctx)


class QuerysetTemplate(BaseRenderer):

    required_fields = ['template_name', 'model_name']
    json_schema = {
        "title": "QuerysetTemplate",
    	"properties": {
    		"template_name": {
    			"type": "string",
                "propertyOrder": 1
            },
            "model_name": {
    			"type": "string",
                "propertyOrder": 2
            },
            "filters": {
    			"type": "object",
                "propertyOrder": 3
            },
    	},
    	"required": ["template_name", "model_name"]
    }

    def render(self, content, context={}):

        required_data = self.get_required_fields(content)
        required_data = {x:render_param(required_data[x], context) for x in required_data}
        template = loader.get_template(required_data["template_name"])
        filters = content.get("filters", {})

        for f in filters:
            filters[f] = render_param(filters[f], context)

        model_klass = import_string(required_data["model_name"])
        qset = model_klass.objects.filter(**filters)

        ctx = Context(context)
        ctx["objects"] = qset

        return template.render(ctx)
