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


    def process_page(self, page, language=None, key=None, parent_node=None):
        out = []
        node = PageNode(
            page.label,
            page.get('url'),
            page.get("data", {}),
            parent=parent_node,
            language=language,
            key=key
        )

        #TODO: !order
        node.children = []
        for child in page.children.filter(language=language, key=key):
            child_nodes = self.process_page(children, language, key, parent_node=node)
            children.extend(child_nodes)

        out.append(node)

        return out


    def get_tree(self, base_path, language=None, key=None):

        try:
            root_page = Page.objects.get(fullpath=base_path)
            return self.process_page(root_page)
        except:
            return []
