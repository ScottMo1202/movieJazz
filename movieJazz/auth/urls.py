from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'auth'
urlpatterns = [
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('register', views.register, name = 'register')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)