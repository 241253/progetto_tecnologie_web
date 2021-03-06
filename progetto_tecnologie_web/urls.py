from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from user_management import urls as um_urls
from lessons_management import urls as lm_urls
from user_cart import urls as uc_urls
from booking_management import urls as bm_urls
from . import views, settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #BASE SITE
    path('', views.landingPage, name='landingPage'),
    #HOME PAGE
    path('home/', views.HomePage.as_view(), name='homePage'),
    path('chi_siamo/', views.chi_siamoPage, name='chi_siamo'),
    path('tariffe/', views.pricesPage, name='tariffe'),
    path('contatti/', views.contactView, name="contatti"),
    path('contatti_success/', views.ContattiSuccessView, name='contatti_success'),
    #USER_MANAGEMENT
    path('user_management/', include(um_urls)),
    #LESSONS_MANAGEMENT
    path('lessons_management/', include(lm_urls)),
    #USER_CART
    path('user_cart/', include(uc_urls)),
    #BOOKING_MANAGEMENT
    path('booking_management/', include(bm_urls)),
    # PASSWORD RESET URL
    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
