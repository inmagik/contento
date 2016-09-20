from django.test import TestCase
import os
from contento.backends.files import FlatFilesBackend
from contento.exceptions import CmsPageNotFound, FlatFilesBaseNotConfigured
from contento.settings import CONTENTO_FLATFILES_BASE
from contento.helpers import get_current_backend
import tempfile
import shutil

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

        page_data = self.backend.get_page("")
        self.assertTrue('page' in page_data)
        self.assertTrue('content' in page_data)
        self.assertEquals(page_data["content"]["region_one"][0]["type"], "Text")

        page_data = self.backend.get_page("/contacts")
        self.assertTrue('page' in page_data)
        self.assertTrue('content' in page_data)

        page_data = self.backend.get_page("contacts")
        self.assertTrue('page' in page_data)
        self.assertTrue('content' in page_data)



    def test_get_meta_from_path(self):

        path = self.backend.get_path("section/a.yml")
        label, lang, key = self.backend.get_meta_from_path(path)
        self.assertEquals(label, "/section/a")
        self.assertEquals(lang, None)
        self.assertEquals(key, None)

        path = self.backend.get_path("section/a__it.yml")
        label, lang, key = self.backend.get_meta_from_path(path)
        self.assertEquals(label, "/section/a")
        self.assertEquals(lang, "it")
        self.assertEquals(key, None)

        path = self.backend.get_path("section/a__it---draft.yml")
        label, lang, key = self.backend.get_meta_from_path(path)
        self.assertEquals(label, "/section/a")
        self.assertEquals(lang, "it")
        self.assertEquals(key, "draft")

        path = self.backend.get_path("section/a---draft.yml")
        label, lang, key = self.backend.get_meta_from_path(path)
        self.assertEquals(label, "/section/a")
        self.assertEquals(lang, None)
        self.assertEquals(key, "draft")

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
        #print [x for x in tree]

    def test_move_page(self):
        """
        """
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")
        backend.move_page("contacts", "/section")
        page = backend.get_page("/section/contacts")
        def fun():
            page = backend.get_page("contacts")
        self.assertRaises(CmsPageNotFound, fun)

        backend.move_page("section/contacts", "/")
        page = backend.get_page("contacts")
