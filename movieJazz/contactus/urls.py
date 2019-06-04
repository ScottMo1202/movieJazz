from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'contactus'
urlpatterns = [
    path(r'', views.contact, name = 'contact'),
    path(r'questions', views.questions, name = 'questions'),
    path(r'answer/<int:question_id>', views.ansQuestion, name = 'ansQuestion')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
