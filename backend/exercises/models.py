from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_plans")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class PlanExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.sets}x{self.repetitions})"
