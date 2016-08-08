from django.test import TestCase
import os
from contento.registry import Registry

class RegistryTestCase(TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_process_node(self):
        """
        """
        node = {
            "slug" : "test",
            "children" : [
                {
                    "slug" : "b"
                }
            ]
        }

        out = self.registry.process_node(node, "")
        self.assertTrue("/test" in out)
        self.assertTrue("/test/b" in out)


    def test_build(self):
        """
        """
        node = {
            "slug" : "test",
            "children" : [
                {
                    "slug" : "b"
                }
            ]
        }
        reg = Registry(build=False)

        #TODO: COMPLETE TEST
        self.assertTrue(True)
