from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='epub_home'),
    path('/download', views.convert_url_text, name='convert_url_text')
]