from django.utils.module_loading import import_string
from contento.settings import CONTENTO_BACKEND
from django.core.urlresolvers import reverse_lazy


class Tree(object):
    """
    """
    def __init__(self, root, language=None):
        self.root = root
        self.language = language
        self.backend = import_string(CONTENTO_BACKEND)()
        self.data = self.build_tree()

    def build_urls(self, node):
        print 2, node
        slug = node.get("url", node.get("slug"))
        #link = reverse('contento-cms', kwargs={"slug":slug})
        #print "l", link
        for n in node["children"]:
            self.build_urls(n)


    def build_tree(self):
        page_tree = self.backend.get_tree(self.root)
        for t  in page_tree:
            self.build_urls(t)
        return page_tree
