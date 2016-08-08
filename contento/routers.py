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

    def mount(self, base_url, base_slug):
        """
        Register content management on a base_url
        """

        urls = []

        if(base_url):
            base_url = base_url + "/"

        tree = Tree(base_slug)

        public_pages_url = url(r'%s(?P<page_url>.*)' % base_url, serve_page, name="contento-cms")
        urls.append(public_pages_url)
        return urls
