from django.test import TestCase
import os
from contento.routers import CMSRouter

class RouterTestCase(TestCase):
    def setUp(self):
        self.router = CMSRouter()

    def test_mount(self):
        """
        """
        urls = self.router.mount("")
        pattern = urls[0].regex.pattern
        self.assertEquals(pattern, "(?P<page_url>.*)")

        urls = self.router.mount("abc/")
        pattern = urls[0].regex.pattern
        self.assertEquals(pattern, "abc/(?P<page_url>.*)")
