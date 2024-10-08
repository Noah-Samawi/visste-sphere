"""Programs app tests"""

from django.test import TestCase
from django.urls import reverse

from products.models import Category
from .models import Program


class ProgramsPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the products page.
    '''
    def test_all_products_page(self):
        '''
        Test if all products page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('programs'))
        self.assertTemplateUsed(response, 'programs/programs.html')


class ProductsDetailPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the product detail page.
    '''

    @classmethod
    def setUpTestData(cls):
        ''' Create test product'''
        cls.category = Category.objects.create(name='Fiction')
        cls.program = Program.objects.create(
            name="Test Name",
            id=10292021102495812,
            description='Test description',
            sale=10,
            price=20.00,
            image_url='https://testimage.com',
            image="beanie.jpg",
            rating=4.5,
            video_url='https://testvideo.com',
        )

    def test_program_detail_page(self):
        '''
        Test if all programs page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('program_detail',
                                   kwargs={'program_id': self.program.id}))
        self.assertTemplateUsed(response, 'programs/program_detail.html')
