"""
Definition of urls for djangoapp.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.urls import path,include
from . import views
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    #url('',app.views.index),
    path('', include('landing.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
