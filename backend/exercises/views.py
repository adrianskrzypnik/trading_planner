from rest_framework import viewsets, permissions
from .models import WorkoutPlan
from .serializers import WorkoutPlanSerializer

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)
