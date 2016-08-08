from django.utils.module_loading import import_string
from contento.settings import CONTENTO_BACKEND
from django.core.urlresolvers import reverse_lazy



class Registry(object):
    """
    Content registry.

    """
    def __init__(self, language=None):
        self.language = language
        self.backend = import_string(CONTENTO_BACKEND)()
        self.content_by_url = {}
        self.content_tree = []
        self.build()

    def process_node(self, node, base):
        out = {}
        if not base.endswith("/"):
            base = base + "/"
        url = base + node["slug"]
        out[url] = { x:node[x] for x in node if x != "children"}
        for c in node["children"]:
            out.update(self.process_node(c, url))
        return out

    def build(self):
        tree = self.backend.get_tree("/", language=self.language)
        self.content_tree = tree

        urls = {}
        for node in tree:
            o = self.process_node(node, "/")
            urls.update(o)
        self.content_by_url = urls
