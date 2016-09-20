from django.conf.urls import url
from .views import serve_page

class CMSRouter(object):
    """
    Generates urls based on site pages.
    Should handle (some ideas):
    - drafts/public
    - i18n
    """

    #TODO: the name should be parametrized or omitted. Right now we can mount just one tree...
    def mount(self, base_url):
        """
        Register content management on a base_url
        """

        urls = []

        public_pages_url = url(r'%s(?P<page_url>.*)' % base_url, serve_page, name="contento-cms")
        urls.append(public_pages_url)
        return urls
