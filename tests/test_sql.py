"""
"""
from django.test import TestCase
from contento.models import Page
from contento.backends.sql import SQLBackend

class SQLTest(TestCase):
    def setUp(self):
        self.index_page = Page.objects.create(
           label="index",
           url=""
        )


        self.backend = SQLBackend()

    def test_get_page(self):
        page = self.backend.get_page("index")
        print page.get("url")
        print page

    def test_get_tree(self):
        tree = self.backend.get_tree("/")
