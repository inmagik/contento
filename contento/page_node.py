from contento.backends.helpers import get_path_from_meta
from django.urls import reverse

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
        labelKeyKwargs = {
            "label" : self.label
        }
        if self.key:
            labelKeyKwargs["key"] = self.key

        return {
            "label" : self.label,
            "language" : self.language,
            "key" : self.key,
            "order" : self.order,
            "url" : self.url,
            "viewUrl" : reverse(
                "contento-cms",
                kwargs = {"page_url" : self.get_path() }
            ),
            "editUrl" : reverse(
                "dashboard-edit-page-base",
                kwargs = labelKeyKwargs
            ),
            "dropUrl" : reverse(
                "dashboard-drop-page",
                kwargs = labelKeyKwargs
            ),
            "addChildUrl" : reverse(
                "dashboard-add-page-with-parent",
                kwargs = {"parent" : self.get_meta_path()  }
            ),
            "data" : self.data,
            "children" : [x.serialize() for x in self.children]
        }
