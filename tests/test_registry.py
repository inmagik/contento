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
        child_node = PageNode("Child", "child", {}, node)

        out = self.registry.process_node(node, "")
        self.assertTrue("/test" in out)

        out = self.registry.process_node(child_node, "")
        self.assertTrue("/test/child" in out)


    def test_build(self):
        """
        """
        node = PageNode("Test", "test", {}, None)
        child_node = PageNode("Child", "child", {}, node)

        reg = Registry(build=False)
        reg.build()

        #TODO: COMPLETE TEST
        #self.assertTrue(True)
