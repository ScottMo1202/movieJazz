from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'membership'
urlpatterns = [
    path('', views.profile, name = 'profile'),
    path('memberships', views.updateMembership, name = 'updateMembership'),
    path('memberships/purchase/<int:theType>', views.purchase, name = 'purchase'),
    path('transactions', views.transactions, name = 'transactions')
]