from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'
urlpatterns = [
    path(r'', views.home, name = 'home'),
    path(r'movies', include('handlemovie.urls')),
    path(r'users', views.users, name = 'users'),
    path(r'offers', views.offers, name = 'offers'),
    path(r'offers/<int:offerId>', views.specificOffer, name='specificOffer'),
    path(r'theaters', views.theaters, name = 'theaters'),
    path(r'theaters/<int:theater_id>', views.specificTheater, name = 'specificTheater'),
    path(r'theaters/<int:theater_id>/tickets', views.tickets, name = 'tickets'),
    path(r'transactions', views.transactions, name = 'transactions')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)