"""Home app tests"""

from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    '''
    Test case class for verifying the functionality of the home page.
    '''
    def test_home_page(self):
        '''
        Test if authors page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/home.html')