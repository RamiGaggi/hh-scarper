from django.test import TestCase


# Create your tests here.
class FirstTest(TestCase):

    def test_dummy(self):
        test = 'dummy'
        self.assertEqual(test, 'dummy')
