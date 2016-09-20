from django.utils.module_loading import import_string
from contento.settings import CONTENTO_BACKEND
from django.core.urlresolvers import reverse_lazy
from contento.helpers import get_current_backend



class Registry(object):
    """
    Content registry.

    """
    def __init__(self, language=None, build=True):
        self.language = language
        self.backend = get_current_backend()
        self.content_by_url = {}
        self.content_tree = []
        if build:
            self.build()

    def process_node(self, node, base):
        out = {}
#        print dir(node)
        if not base.endswith("/"):
            base = base + "/"
        url = base + node.get_path()
        out[url] = node    
        for c in node.children:
            out.update(self.process_node(c, base))
        return out

    def build(self):
        tree = self.backend.get_tree("/", language=self.language)
        self.content_tree = tree
        urls = {}
        for node in tree:
            o = self.process_node(node, "/")
            urls.update(o)
        self.content_by_url = urls
