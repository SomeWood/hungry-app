from django.db import models
from django.contrib.auth.models import User


class FoodEntry(models.Model):
    MEAL_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    calories = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.food_name