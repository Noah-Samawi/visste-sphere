"""Cart app tests"""

from django.test import TestCase
from django.urls import reverse


class CartPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the shopping cart page.
    '''
    def test_cart_page(self):
        '''
        Test if shopping cart page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('view_cart'))
        self.assertTemplateUsed(response, 'cart/cart.html')
