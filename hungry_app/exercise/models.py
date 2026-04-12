from django.db import models
from django.contrib.auth.models import User


class ExerciseEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    duration = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.exercise_name