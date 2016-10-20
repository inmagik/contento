from contento.models import Page
from contento.page_node import PageNode

class SQLBackend(object):

    def get_page(self, label, language=None, key=None):
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        out = {
            "url" : page.url,
            "template" : page.template,
            "data" : page.data,
            "content" : page.content
        }
        return out

    def get_tree(self, base_path, language=None, key=None):
        out = []


        return out
