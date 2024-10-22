"""Home views"""
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import os


def home(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')


def privacy(request):
    """ A view to return the privacy page """
    return render(request, 'home/privacy.html')


# Google verification view
def google_verification(request):
    """ A view to return the Google verification file """
    file_path = os.path.join('static', 'google621ef7f3bda07ae5.html')
    with open(file_path, 'r') as file:
        content = file.read()
    return HttpResponse(content, content_type="text/html")


# Error handling views
def handler404(request):
    '''
    Render 404 page
    '''
    return render(request, '400.html', status=404)


def handler500(request):
    '''
    Render 500 page
    '''
    return render(request, '500.html', status=500)


def handler403(request, exception):
    '''
    Render 403 page
    '''
    if isinstance(exception, PermissionDenied):
        return render(request, '403.html', status=403)
    return render(request, '500.html', status=500)
