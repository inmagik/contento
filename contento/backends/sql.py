from contento.models import Page

class SQLBackend(object):

    def get_page(self, label, language=None, key=None):
        page = Page.objects.get(
            label=label,
            language=language,
            key = key
        )
        out = {
            "label" : label,
            "language" : language,
            "key" : key,
            "url" : page.url,
            "parent" : page.parent,
            "data" : {
                "published" : True,
                "template" : page.template
            },
            "content" : {}
        }
        return out

    def get_tree(self, base_path, language=None, key=None):
        raise NotImplementedError
