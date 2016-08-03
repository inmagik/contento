from django.test import TestCase
import os
from contento.routers import CMSRouter

class RouterTestCase(TestCase):
    def setUp(self):
        self.router = CMSRouter()

    def test_mount(self):
        """
        """
        self.router.mount("")
        pattern = self.router.urls[0].regex.pattern
        self.assertEquals(pattern, "(?P<slug>.*)")

        self.router.mount("/abc")
        pattern = self.router.urls[1].regex.pattern
        self.assertEquals(pattern, "/abc/(?P<slug>.*)")
