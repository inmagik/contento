from django.test import TestCase
import os
from contento.backends.files import FlatFilesBackend
from contento.exceptions import CmsPageNotFound, CmsPageAlreadyExisting, FlatFilesBaseNotConfigured
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
        self.assertTrue('data' in page_data)
        self.assertTrue('content' in page_data)
        self.assertEquals(page_data["content"]["region_one"][0]["type"], "Text")

        page_data = self.backend.get_page("")
        self.assertTrue('data' in page_data)
        self.assertTrue('content' in page_data)
        self.assertEquals(page_data["content"]["region_one"][0]["type"], "Text")

        page_data = self.backend.get_page("/contacts")
        self.assertTrue('data' in page_data)
        self.assertTrue('content' in page_data)

        page_data = self.backend.get_page("contacts")
        self.assertTrue('data' in page_data)
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


    def test_add_modify_page(self):
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")

        label = "new-page"
        url = "new-page"
        page_data = {
            "menu_title": "New",
            "published": True,
            "template": "simple_page.html"
        }
        page_content = {
            "region_one" : {
                "type": "Text",
                "data" : {
                    "text": "Hi. this is some text from the cms. It's the new page."
                }
            }
        }

        #testing adding
        page = backend.add_page(label, url, page_data, page_content=page_content, language=None, key=None)
        page_2 = backend.get_page(label)
        self.assertEquals(page, page_2)

        def fun():
            page = backend.add_page(
                label, url=url, page_data=page_data, page_content=page_content, language=None, key=None
            )
        self.assertRaises(CmsPageAlreadyExisting, fun)

        #testing adding nested page (intermediate folder could not exist)
        label_nested = "nonexisting/new-page"
        page_nested = backend.add_page(
            label_nested, url=None, page_data=page_data, page_content=page_content, language=None, key=None
            )

        #testing modification
        new_page_content = {
            "region_one" : {
                "type": "Text",
                "data" : {
                    "text": "Hi. Text is changed."
                }
            }
        }

        page_nested_modified = backend.modify_page(
            label_nested, url=None, page_data=page_data, page_content=new_page_content, language=None, key=None
            )
        page_nested_modifield_loaded = backend.get_page(label_nested, language=None, key=None)
        self.assertEquals(page_nested_modifield_loaded["content"], new_page_content)

    def test_drop_page(self):
        """
        """
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")
        page = backend.get_page("contacts")
        backend.drop_page("contacts")

        def fun():
            page = backend.get_page("contacts")
        self.assertRaises(CmsPageNotFound, fun)

        def fun2():
            backend.drop_page("contacts")
        self.assertRaises(CmsPageNotFound, fun2)



    def test_add_page_fragment(self):
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")

        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]

        self.assertEquals(len(region_one_items), 3)

        backend.add_page_fragment(
            "contacts",
            "region_one", "Text", { "text" : "some text here"},
            language=None, key=None,
            position=None
        )
        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        self.assertEquals(len(region_one_items), 4)


    def test_drop_page_fragment(self):
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")

        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]

        self.assertEquals(len(region_one_items), 3)

        backend.drop_page_fragment(
            "contacts",
            "region_one", position=2,
            language=None, key=None,
        )
        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        self.assertEquals(len(region_one_items), 2)


    def test_move_page_fragment(self):
        temp_dir = tempfile.gettempdir()
        try:
            shutil.rmtree(temp_dir+"/cms_pages")
        except:
            pass
        shutil.copytree(CONTENTO_FLATFILES_BASE, temp_dir+"/cms_pages/")
        backend = FlatFilesBackend(temp_dir+"/cms_pages")

        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        first_item = page["content"]["region_one"][0]
        second_item = page["content"]["region_one"][1]


        backend.move_page_fragment(
            "contacts",
            "region_one", position=0, new_position=2,
            language=None, key=None,
        )
        page = backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        new_first_item = page["content"]["region_one"][0]
        self.assertEquals(second_item, new_first_item)
