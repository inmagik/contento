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
