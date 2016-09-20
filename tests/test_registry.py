from django.test import TestCase
import os
from contento.registry import Registry
from contento.page_node import PageNode

class RegistryTestCase(TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_process_node(self):
        """
        """
        node = PageNode("Test", "test", {}, None)
        child_node = PageNode("Test", "test", {}, None)

        out = self.registry.process_node(node, "")

        #self.assertTrue("/test" in out)
        #self.assertTrue("/test/b" in out)


    # def test_build(self):
    #     """
    #     """
    #     node = {
    #         "url" : "test",
    #         "children" : [
    #             {
    #                 "url" : "b"
    #             }
    #         ]
    #     }
    #     reg = Registry(build=False)
    #
    #     #TODO: COMPLETE TEST
    #     self.assertTrue(True)
