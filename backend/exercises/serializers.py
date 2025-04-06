from rest_framework import serializers
from .models import WorkoutPlan, PlanExercise

class PlanExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanExercise
        fields = ['id', 'name', 'sets', 'repetitions']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = PlanExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'title', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        plan = WorkoutPlan.objects.create(user=self.context['request'].user, **validated_data)
        for ex in exercises_data:
            PlanExercise.objects.create(workout_plan=plan, **ex)
        return plan
