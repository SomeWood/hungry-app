from django.urls import path
from . import views

urlpatterns = [
    path('', views.exercise_log, name='exercise_log'),
    path('add/', views.add_exercise_entry, name='add_exercise_entry'),
    path('delete/<int:entry_id>/', views.delete_exercise_entry, name='delete_exercise_entry'),
]