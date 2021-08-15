from django.test import TestCase


# Create your tests here.
class FirstTest(TestCase):

    def test_dummy(self):
        dummy = 1
        assert dummy == 1
