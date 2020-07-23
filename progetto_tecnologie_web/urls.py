from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from user_management import urls as um_urls
from lessons_management import urls as lm_urls
from . import views, settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #BASE SITE
    path('', views.landingPage, name='home'),
    path('prenotazioni/', views.reservationPage, name='prenotazioni'),
    path('chi_siamo/', views.chi_siamoPage, name='chi_siamo'),
    path('tariffe/', views.pricesPage, name='tariffe'),
    path('contatti/', views.contacts, name="contatti"),
    #USER_MANAGEMENT
    path('user_management/', include(um_urls)),
    #LESSONS_MANAGEMENT
    path('lessons/', include(lm_urls)),
    # PASSWORD RESET URL
    url('^', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
