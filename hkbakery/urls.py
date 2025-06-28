from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_bread, name='get_all_bread')
]