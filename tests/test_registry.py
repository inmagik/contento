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
        out = self.registry.process_node(child_node, "")

        #self.assertTrue("/test" in out)
        #self.assertTrue("/test/b" in out)

    def test_build(self):
        """
        """
        node = PageNode("Test", "test", {}, None)
        child_node = PageNode("Child", "child", {}, node)

        reg = Registry(build=False)

        #TODO: COMPLETE TEST
        self.assertTrue(True)
