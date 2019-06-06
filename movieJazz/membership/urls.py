from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'membership'
urlpatterns = [
    path(r'', views.profile, name = 'profile'),
    path(r'memberships', views.updateMembership, name = 'updateMembership'),
    path(r'memberships/purchase/<int:theType>', views.purchase, name = 'purchase'),
    path(r'transactions', views.transactions, name = 'transactions')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)