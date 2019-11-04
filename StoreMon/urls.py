"""
Definition of urls for StoreMon.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from rest_framework.authtoken import views as auth_views

import app.forms
from app.views import *
from app.router import router


# Uncomment the next lines to enable the admin:
from django.urls import include, path
from django.contrib import admin
admin.autodiscover()

from .loginAPI import CustomAuthToken


urlpatterns = [
    # Examples:
    url(r'^$', app.views.reactRoot),
    url(r'^service-worker.js', app.views.sw),
    # url(r'^contact$', app.views.contact, name='contact'),
    # url(r'^about$', app.views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',
        django.contrib.auth.views.LoginView,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.LogoutView,
        {
            'next_page': '/',
        },
        name='logout'),
    path('api/', include(router.urls)),
    path('gettoken/',  CustomAuthToken.as_view()),
    
    #path('gettoken/', auth_views.obtain_auth_token, name='gettoken')
    #path('api/', include('app.api_urls'))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
]
