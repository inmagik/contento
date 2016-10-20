from rest_framework.views import APIView
from rest_framework.response import Response
from contento.meta import get_contento_renderers_schemas

class RenderersMetaView(APIView):

    def get(self, request, *args, **kwargs):
        out = get_contento_renderes_schemas()
        return Response(out)
