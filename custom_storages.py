"""
Custom storage classes for AWS S3 integration.
This module provides StaticStorage and MediaStorage classes for handling
static and media files with AWS S3.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Custom storage class for static files on S3.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files on S3.
    """
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
