from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'buytickets'
urlpatterns = [
    path(r'', views.cart, name = 'cart'),
    path(r'checkout', views.checkout, name = 'checkout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)