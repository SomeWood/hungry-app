from django.urls import path
from . import views

urlpatterns = [
    path('', views.weight_log, name='weight_log'),
    path('add/', views.add_weight_entry, name='add_weight_entry'),
    path('delete/<int:entry_id>/', views.delete_weight_entry, name='delete_weight_entry'),
]
