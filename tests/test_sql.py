"""
"""
from django.test import TestCase
from contento.models import Page
from contento.backends.sql import SQLBackend
from contento.exceptions import CmsPageNotFound, CmsPageAlreadyExisting

class SQLTest(TestCase):
    def setUp(self):
        self.index_page = Page.objects.create(
           label="index",
           url=""
        )
        self.backend = SQLBackend()

    def test_get_page(self):
        page = self.backend.get_page("index")
        self.assertEquals(page.get("label"), "index")

    def test_get_tree(self):
        tree = self.backend.get_tree("/")
        root = tree[0]
        self.assertEquals(root.label, "index")
        self.assertEquals(len(tree), 1)

        self.contacts_page = Page.objects.create(
           label="contacts",
           url="contacts",
           parent = self.index_page
        )

        tree = self.backend.get_tree("/")
        root = tree[0]
        self.assertEquals(len(tree), 1)

        tree = self.backend.get_tree("xxxx")
        self.assertEquals(tree, [])


    def test_move_page(self):
        """
        """
        backend = self.backend
        contacts_page = Page.objects.create(
           label="contacts",
           url="contacts"
        )
        example_page = Page.objects.create(
           label="example",
           url="example"
        )

        backend.move_page("contacts", "example")

        tree = self.backend.get_tree("/example")
        self.assertEquals(tree[0].children[0].label, 'contacts')

        backend.move_page("contacts", None)
        tree = self.backend.get_tree("/example")
        self.assertEquals(len(tree[0].children), 0)


    def test_add_modify_page(self):

        label = "new-page"
        url = "new-page"
        template = "simple_page.html"
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
        page = self.backend.add_page(label, template, url, page_data=page_data, page_content=page_content, language=None, key=None)
        page_2 = self.backend.get_page(label)
        self.assertEquals(page, page_2)

        def fun():
            page = self.backend.add_page(
                label, template, url=url, page_data=page_data, page_content=page_content, language=None, key=None
            )
        self.assertRaises(CmsPageAlreadyExisting, fun)

        label_nested = "nonexisting/new-page"
        page_nested = self.backend.add_page(
            label_nested, template, url=None, page_data=page_data, page_content=page_content, language=None, key=None
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

        page_nested_modified = self.backend.modify_page(
            label_nested, url=None, page_data=page_data, page_content=new_page_content, language=None, key=None
            )
        page_nested_modifield_loaded = self.backend.get_page(label_nested, language=None, key=None)
        self.assertEquals(page_nested_modifield_loaded["content"], new_page_content)


    def test_drop_page(self):
        contacts_page = Page.objects.create(
           label="contacts",
           url="contacts"
        )
        page = self.backend.get_page("contacts")
        self.backend.drop_page("contacts")

        def fun():
            page = self.backend.get_page("contacts")
        self.assertRaises(CmsPageNotFound, fun)

        def fun2():
            self.backend.drop_page("contacts")
        self.assertRaises(CmsPageNotFound, fun2)



    def test_add_page_fragment(self):
        contacts_page = Page.objects.create(
           label="contacts",
           url="contacts",
           content={"region_one":[]}
        )
        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]

        self.assertEquals(len(region_one_items), 0)

        self.backend.add_page_fragment(
            "contacts",
            "region_one", "Text", { "text" : "some text here"},
            language=None, key=None,
            position=None
        )
        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        self.assertEquals(len(region_one_items), 1)


    def test_drop_page_fragment(self):

        contacts_page = Page.objects.create(
           label="contacts",
           url="contacts",
           content={"region_one":[]}
        )

        self.backend.add_page_fragment(
            "contacts",
            "region_one", "Text", { "text" : "some text here"},
            language=None, key=None,
            position=None
        )

        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        self.assertEquals(len(region_one_items), 1)

        self.backend.drop_page_fragment(
            "contacts",
            "region_one", position=0,
            language=None, key=None,
        )
        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        self.assertEquals(len(region_one_items), 0)


    def test_move_page_fragment(self):

        contacts_page = Page.objects.create(
           label="contacts",
           url="contacts",
           content={"region_one":[]}
        )

        self.backend.add_page_fragment(
            "contacts",
            "region_one", "Text", { "text" : "some text here"},
            language=None, key=None,
            position=None
        )

        self.backend.add_page_fragment(
            "contacts",
            "region_one", "Text", { "text" : "again. some text here"},
            language=None, key=None,
            position=None
        )

        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        first_item = page["content"]["region_one"][0]
        second_item = page["content"]["region_one"][1]

        self.backend.move_page_fragment(
            "contacts",
            "region_one", position=0, new_position=1,
            language=None, key=None,
        )
        page = self.backend.get_page("contacts")
        region_one_items = page["content"]["region_one"]
        new_first_item = page["content"]["region_one"][0]
        self.assertEquals(second_item, new_first_item)
