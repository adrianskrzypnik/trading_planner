from rest_framework import serializers
from .models import WorkoutSession, WorkoutExercise

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'name', 'sets', 'repetitions', 'weight']

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutSession
        fields = ['id', 'workout_plan', 'date', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        session = WorkoutSession.objects.create(user=self.context['request'].user, **validated_data)
        for ex in exercises_data:
            WorkoutExercise.objects.create(session=session, **ex)
        return session
