from django.utils.module_loading import import_string
from contento.settings import CONTENTO_BACKEND


class Tree(object):
    """
    """
    def __init__(self, root, language=None):
        self.root = root
        self.language = language
        self.backend = import_string(CONTENTO_BACKEND)()
        self.data = self.build_tree()

    def build_tree(self):
        page_tree = self.backend.get_tree(self.root)
        return page_tree
