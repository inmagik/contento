from django.conf.urls import url
from .views import serve_page
from .tree import Tree

class CMSRouter(object):
    """
    Generates urls based on site pages.
    Should handle (some ideas):
    - drafts/public
    - i18n
    """

    def __init__(self):
        self.urls = []

    def mount(self, base_url, base_slug):
        """
        Register content management on a base_url
        """
        if not base_url or not base_url.endswith("/"):
            base_url = base_url + "/"

        tree = Tree(base_slug)



        slug_url = url(r'%s(?P<slug>.*)' % base_url, serve_page, name="contento-cms")
        self.urls.append(slug_url)
