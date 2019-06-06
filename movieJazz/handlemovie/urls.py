from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'handlemovie'
urlpatterns = [
    path(r'/', views.movies, name = 'movies'),
    path(r'/raw', views.rawMovies, name = 'rawMovies'),
    path(r'/<int:movieId>', views.specificMovie, name='specificMovie'),
    path(r'/search', views.search, name = 'search'),
    path(r'/<int:movie_id>/review', views.review, name = 'review')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)