from django.test import TestCase

class AnimalTestCase(TestCase):
    def setUp(self):
        print 2

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        print 3
