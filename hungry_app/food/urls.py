from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_log, name='food_log'),
    path('add/', views.add_food_entry, name='add_food_entry'),
    path('delete/<int:entry_id>/', views.delete_food_entry, name='delete_food_entry'),
]