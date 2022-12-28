'''
Tests for home app
'''
from django.test import TestCase

from home.forms import SearchForm


# Create your tests here.
class SearchFormTest(TestCase):
    '''
    SearchForm
    '''
    def test_form_validation(self):
        '''
        Test validity of form
        '''
        form = SearchForm(data={'query': ''})
        self.assertFalse(form.is_valid())

        form = SearchForm(data={'query': 'test query'})
        self.assertTrue(form.is_valid())
