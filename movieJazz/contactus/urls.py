from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'contactus'
urlpatterns = [
    path('', views.contact, name = 'contact'),
    path('questions', views.questions, name = 'questions'),
    path('answer', views.ansQuestion, name = 'ansQuestion')
]