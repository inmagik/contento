from rest_framework.views import APIView
from rest_framework.response import Response
from .settings import CONTENTO_RENDERERS
from contento import renderers
from django.utils.module_loading import import_string

class RenderersMetaView(APIView):

    def get_contento_renderers(self):

        if CONTENTO_RENDERERS is None:
            RENDERERS = []
            for x in dir(renderers):
                o = getattr(renderers, x);
                try:
                    sub = issubclass(o, renderers.base.BaseRenderer)
                except:
                    continue
                if sub:
                    RENDERERS.append("contento.renderers.%s" % x)
            return RENDERERS

        return CONTENTO_RENDERERS or []

    def get(self, request, *args, **kwargs):
        rs = self.get_contento_renderers()
        out = {}
        for r in rs:
            klass = import_string(r)
            json_schema = getattr(klass, "json_schema")
            if json_schema:
                out[r] = json_schema

        return Response(out)
