import re
from django.core.urlresolvers import reverse

contento_link = "contento://(?P<url>[\w-]+)"
contento_link_re = re.compile(contento_link)

class InternalLinks(object):
    def process(self, text):
        #print "processing internal links..", text
        def f(matchf):
            match = matchf.groups()
            url = match[0] or "_root"
            try:
                link = reverse('contento-cms', kwargs={"page_url":url})
                return link
            except:
                return "#cms:notfound"

        text = contento_link_re.sub(f, text)
        return text
