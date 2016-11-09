from contento.backends.helpers import get_path_from_meta
from django.urls import reverse

class PageNode(object):

    def __init__(self, label, url, data=None, parent=None,
        template=None, content=None, order=0, language=None, key=None, level=0):
        self.label = label
        self.url = url
        self.data = data
        self.parent = parent
        self.order = order
        self.language = language
        self.key = key
        self.content = content
        self.template = template
        self.level = level

        self.children = []

    def get_path(self):
        if not self.parent:
            return self.url

        parent_path = self.parent.get_path()
        if not parent_path or parent_path == "/":
            return "%s" % (self.url)

        return "%s/%s" % (self.parent.get_path(), self.url)



    def add_child(self, child):
        self.children.append(child)

    def get_meta_path(self):
        return get_path_from_meta(self.label, self.language, self.key)

    def serialize(self, with_content=False):
        label_key_kwargs = {
            "label" : self.label
        }
        if self.key:
            label_key_kwargs["key"] = self.key

        out = {
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
                kwargs = label_key_kwargs
            ),
            "dropUrl" : reverse(
                "dashboard-drop-page",
                kwargs = label_key_kwargs
            ),
            "addChildUrl" : reverse(
                "dashboard-add-page-with-parent",
                kwargs = {"parent" : self.get_meta_path()  }
            ),
            "data" : self.data,
            "children" : [x.serialize() for x in self.children]
        }

        if with_content:
            out["content"] = self.content
            out["template"] = self.template

        return out
