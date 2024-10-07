"""Checkout app tests"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages


class TestCheckoutView(TestCase):
    """
    Test case for the checkout view.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.client = Client()
        self.checkout_url = reverse('checkout')

    def test_redirect_if_cart_is_empty(self):
        """
        Test if the checkout view redirects to the cart view
        when the cart is empty.
        """
        response = self.client.get(self.checkout_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_cart'))
        self.assertEqual(str(messages[0]), "There are no items in your cart")
