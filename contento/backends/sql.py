
class SQLBackend(object):

    def get_page(self, label, language=None, key=None):
        raise NotImplementedError

    def get_tree(self, slug, language=None, key=None):
        raise NotImplementedError
