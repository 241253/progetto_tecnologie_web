"""progetto_tecnologie_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from user_management import urls as um_urls
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #BASE SITE
    path('', views.landingPage, name='home'),
    path('prenotazioni/', views.reservationPage, name='prenotazioni'),
    path('chi_siamo/', views.chi_siamoPage, name='chi_siamo'),
    path('tariffe/', views.pricesPage, name='tariffe'),
    path('contatti/', views.contatti, name="contatti"),
    #USER_MANAGEMENT
    path('user_management/', include(um_urls)),
    # PASSWORD RESET URL
    url('^', include('django.contrib.auth.urls')),
]
