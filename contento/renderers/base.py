from contento.exceptions import RendererConfigError

class BaseRenderer(object):

    required_fields = []

    def get_required_fields(self, content):
        out = {}
        for x in self.required_fields:
            if x not in content:
                raise RendererConfigError("%s is required for configuring %s renderer" % (x, self.__class__.__name__))
            out[x] = content[x]
        return out

    def render(self, content, context={}):
        raise NotImplementedError
