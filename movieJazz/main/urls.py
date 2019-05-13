from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('movies', views.movies, name = 'movies'),
    path('users', views.users, name = 'users'),
    path('movies/<int:movieId>', views.specificMovie, name='specificMovie'),
    path('offers', views.offers, name = 'offers'),
    path('offers/<int:offerId>', views.specificOffer, name='specificOffer')
]