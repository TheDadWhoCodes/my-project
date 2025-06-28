from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/download', views.convert_url_text, name='convert_url_text')
]