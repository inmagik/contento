from django.test import TestCase
import os
from contento.backends.files import FlatFilesBackend
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured
from contento.settings import CONTENTO_FLATFILES_BASE

class FlatFilesBackendTestCase(TestCase):
    def setUp(self):
        self.backend = FlatFilesBackend()

    def test_page_not_found(self):
        """
        """
        #self.assertTrue(os.path.isdir(self.path))
        def fun():
            page = self.backend.get_page("/not.existing-page")
        self.assertRaises(CmsPageNotFound, fun)

    def test_get_page(self):
        """
        """
        page_data = self.backend.get_page("/")
        self.assertTrue('page' in page_data)
        self.assertTrue('content' in page_data)
        self.assertEquals(page_data["content"]["region_one"][0]["type"], "Text")


    def test_get_path(self):
        path = self.backend.get_path("section")
        self.assertEquals(path, os.path.join(CONTENTO_FLATFILES_BASE, "section"))

        path = self.backend.get_path("")
        self.assertEquals(path, CONTENTO_FLATFILES_BASE + "/")

    def test_get_page_path(self):
        path = self.backend.get_page_path("section")
        self.assertEquals(path, os.path.join(CONTENTO_FLATFILES_BASE, "section.yml"))

        path = self.backend.get_page_path("/")
        self.assertEquals(path, CONTENTO_FLATFILES_BASE + "/_root.yml")

    def test_tree(self):
        """
        """
        tree = self.backend.get_tree("/")
        print tree
