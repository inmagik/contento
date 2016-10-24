from contento.backends.helpers import get_path_from_meta

class PageNode(object):

    def __init__(self, label, url, data=None, parent=None, order=0, language=None, key=None):
        self.label = label
        self.url = url
        self.data = data
        self.parent = parent
        self.order = order
        self.language = language
        self.key = key

        self.children = []

    def get_path(self):
        if not self.parent:
            return self.url
        return "%s/%s" % (self.parent.get_path(), self.url)

    def add_child(self, child):
        self.children.append(child)

    def get_meta_path(self):
        return get_path_from_meta(self.label, self.language, self.key)

    def serialize(self):
        return {
            "label" : self.label,
            "language" : self.language,
            "key" : self.key,
            "order" : self.order,
            "url" : self.url,
            "data" : self.data,
            "children" : [x.serialize() for x in self.children]
        }
