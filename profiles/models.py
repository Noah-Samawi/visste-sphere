"""Profile Models"""

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Subscription(models.Model):
    """
    A user subscription model for maintaining user subscriptions
    """
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('priority', 'Priority'),
    ]

    COLOUR_CHOICES = [
        ('orange', 'Orange'),
        ('green', 'Green'),
        ('cyan', 'Cyan'),
    ]

    SUBSCRIPTION_CHOICES = [
        ('junior_dev', 'Junior Dev'),
        ('mid_dev', 'Mid Dev'),
        ('senior_dev', 'Senior Dev'),
    ]
    image = models.ImageField(null=True, blank=True)
    sku = models.CharField(
        max_length=254,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='junior_dev'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    mentor = models.BooleanField(
        default=False
    )
    tutor_support = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        blank=True
    )
    color = models.CharField(
        max_length=20,
        choices=COLOUR_CHOICES,
        default='orange'
    )
    description = models.TextField(
        default='Junior Dev monthly subscription package'
    )
    free_delivery = models.BooleanField(
        default=True
    )
    product_discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    program_discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    @property
    def total_final_price(self):
        """
        Returns the total price of subscription
        """
        return self.price

    def __str__(self):
        return self.get_name_display()


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    default_phone_number = PhoneNumberField(blank=True, null=True, region=None)
    default_street_address1 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country',
                                   null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    active_subscription = models.ForeignKey(Subscription,
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True,
                                            related_name='active_subscription')
    moderator = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()
