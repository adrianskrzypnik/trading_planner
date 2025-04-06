from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'is_staff': request.user.is_staff,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'error', 'errors': serializer.errors}, status=400)