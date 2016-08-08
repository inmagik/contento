from contento.exceptions import RendererConfigError
from django.utils.module_loading import import_string
from django.template import Context, Template, loader

def render_param(param, context):
    if type(param) == str:
        template = Template(param)
        context = Context(context)
        return template.render(context)
    return param





class ModelInstanceTemplate(object):
    def render(self, content, context={}):
        try:
            template_name = content["template_name"]
        except KeyError:
            raise RendererConfigError("template name is required")

        template = loader.get_template(template_name)

        try:
            model_name = content["model_name"]
        except KeyError:
            raise RendererConfigError("model name is required")

        try:
            model_pk = render_param(content["model_pk"], context)
        except KeyError:
            raise RendererConfigError("model pk is required")

        model_klass = import_string(model_name)
        obj = model_klass.objects.get(pk=model_pk)
        ctx = Context(context)
        ctx["object"] = obj

        return template.render(ctx)


class QuerysetTemplate(object):
    def render(self, content, context={}):
        try:
            template_name = content["template_name"]
        except KeyError:
            raise RendererConfigError("template name is required")
        template = loader.get_template(template_name)

        try:
            model_name = content["model_name"]
        except KeyError:
            raise RendererConfigError("model name is required")

        filters = content.get("filters", {})

        for f in filters:
            filters[f] = render_param(filters[f], context)

        model_klass = import_string(model_name)
        qset = model_klass.objects.filter(**filters)

        ctx = Context(context)
        ctx["objects"] = qset

        return template.render(ctx)
