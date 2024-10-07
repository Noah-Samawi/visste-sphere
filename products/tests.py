"""Products app tests"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile


from .models import Product, Category


class ProductsPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the products page.
    '''
    def test_all_products_page(self):
        '''
        Test if all products page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products/products.html')


class ProductsDetailPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the product detail page.
    '''

    @classmethod
    def setUpTestData(cls):
        ''' Create test product'''
        cls.category = Category.objects.create(name='Fiction')
        cls.product = Product.objects.create(
            name="Test Name",
            id=10292021102495812,
            description='Test description',
            sale=10,
            price=20.00,
            image_url='https://testimage.com',
            image="beanie.jpg",
            rating=4.5
        )

    def test_product_detail_page(self):
        '''
        Test if all products page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(
            reverse(
                'product_detail',
                kwargs={'product_id': self.product.id}
            )
            )
        self.assertTemplateUsed(response, 'products/product_detail.html')


class AddProductPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the add product page.
    '''

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            password='12345'
        )
        self.moderator.profile.moderator = True
        self.moderator.profile.save()

    def test_add_product_page(self):
        '''
        Test if add product page can be accessed by admin
        and it returns the correct template
        '''

        self.client.login(username='admin', password='12345')
        response = self.client.get(reverse('add_product'))
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_moderator_access(self):
        '''
        Test if user with moderator profile can access the add product page
        '''

        self.client.login(username='moderator', password='12345')
        response = self.client.get(reverse('add_product'))
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_non_admin_access(self):
        '''
        Test if non-admin user is forbidden to access the add product page
        '''

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 403)
