import os
from django.test import TestCase
from contento import render_helpers

class RenderHelpersTestCase(TestCase):

    def setUp(self):
        pass

    def test_render_inlines(self):
        """
        """
        text = 'Some text injected here: (: Text|{ "text" : "HELLO! " }  :) with a plugin in the middle.'\
        'And one at the end.. (: Text|{ "text" : " bye! bye" }  :)'
        rendered = render_helpers.render_inlines(text)
        self.assertEquals(rendered, 'Some text injected here: HELLO!  with a plugin in the middle.'\
        'And one at the end..  bye! bye')
