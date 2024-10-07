"""Profile app tests"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import UserProfile


class ProfilePageTests(TestCase):
    '''
    Test case class for verifying the functionality of the profile page.
    '''
    @classmethod
    def setUpTestData(cls):
        ''' Create test Profile'''
        cls.user = User.objects.create(
            username='TestUser',
            password='1234pass',
            email='test@user.com',
            id='1',
        )
        cls.user_profile = UserProfile.objects.update(
            default_country='Ireland',
        )

    def test_if_user_profile_created(self):
        '''
        Test if user profile is created
        '''
        user_profile = UserProfile.objects.filter().last()
        self.assertEqual(user_profile.user.username, 'TestUser')

    def test_profile_page(self):
        '''
        Test if the profile page can be accessed
        and it returns the correct template
        '''

        user = User.objects.get(username='TestUser')
        self.client.force_login(user)
        response = self.client.get(
            reverse('profile'))
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_requires_login(self):
        '''
        Test if profile page requires user to be logged in
        '''
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')


class SubscriptionPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the home page.
    '''

    @classmethod
    def setUpTestData(cls):
        ''' Create test Profile'''
        cls.user = User.objects.create(
            username='TestUser',
            password='1234pass',
            email='test@user.com',
            id='1',
        )
        cls.user_profile = UserProfile.objects.update(
            default_country='Ireland',
            id=1
        )

    def test_subscription_page(self):
        '''
        Test if subscription page can be accessed
        '''
        user = User.objects.get(username='TestUser')
        self.client.force_login(user)
        response = self.client.get(reverse('subscriptions'))
        self.assertTemplateUsed(response, 'profiles/subscriptions.html')

    def test_subscription_page_requires_login(self):
        '''
        Test if subscription page requires user to be logged in
        '''
        response = self.client.get(reverse('subscriptions'))
        self.assertRedirects(response,
                             '/accounts/login/?next=/profile/subscriptions')


class MyCoursesPageTests(TestCase):
    '''
    Test case class for verifying the functionality of the home page.
    '''

    @classmethod
    def setUpTestData(cls):
        ''' Create test Profile'''
        cls.user = User.objects.create(
            username='TestUser',
            password='1234pass',
            email='test@user.com',
            id='1',
        )
        cls.user_profile = UserProfile.objects.update(
            default_country='Ireland',
            id=1
        )

    def test_my_courses_page(self):
        '''
        Test if my courses page can be accessed
        '''
        user = User.objects.get(username='TestUser')
        self.client.force_login(user)
        response = self.client.get(reverse('my_courses'))
        self.assertTemplateUsed(response, 'profiles/my_courses.html')

    def test_my_courses_page_requires_login(self):
        '''
        Test if my courses page requires user to be logged in
        '''
        response = self.client.get(reverse('my_courses'))
        self.assertRedirects(response,
                             '/accounts/login/?next=/profile/my_courses')
