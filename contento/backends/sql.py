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
            "slug" : page.slug,
            "parent" : page.parent,
            "data" : {
                "published" : True,
                "template" : page.template
            },
            "content" : {}
        }
        return out

    def get_tree(self, slug, language=None, key=None):
        raise NotImplementedError
