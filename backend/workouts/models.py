from django.db import models
from django.contrib.auth import get_user_model
from exercises.models import WorkoutPlan, PlanExercise

User = get_user_model()

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_sessions")
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True, related_name="sessions")
    date = models.DateTimeField(auto_now_add=True)

class WorkoutExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=100)  # kopiujemy nazwę z planu
    sets = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
    weight = models.FloatField(null=True, blank=True)  # użytkownik może dodać wagę

    def __str__(self):
        return f"{self.name} - {self.sets}x{self.repetitions} @ {self.weight or 0}kg"
