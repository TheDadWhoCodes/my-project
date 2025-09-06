from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_bread, name='get_all_bread'),
    path('edit/<int:bread_id>/', views.edit_bread, name='edit_bread'),
    path('delete/<int:bread_id>/', views.delete_bread, name='delete_bread')
]