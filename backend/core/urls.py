from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercises.views import WorkoutPlanViewSet
from workouts.views import WorkoutSessionViewSet

router = DefaultRouter()
router.register(r'plans', WorkoutPlanViewSet, basename='plans')
router.register(r'sessions', WorkoutSessionViewSet, basename='sessions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('users.urls')),
]
