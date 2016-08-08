from django.test import TestCase, RequestFactory, Client
from django.http import HttpResponse, Http404
#from contento.views import serve_page

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        # Create an instance of a GET request.
        response = self.client.get('/cms/')
        self.assertEqual(response.status_code, 200)

        #def f():
        #   response = self.client.get('/cms/sss')

        #self.assertRaises(Http404, f)
