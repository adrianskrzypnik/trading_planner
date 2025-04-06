from rest_framework import serializers
from .models import User  # Zaimportuj swój model użytkownika

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2']

    def validate(self, data):
        # Sprawdzanie czy hasła są identyczne
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Hasła muszą być identyczne.'})

        # Sprawdzenie, czy hasło nie składa się wyłącznie z cyfr
        if data['password1'].isdigit():
            raise serializers.ValidationError({'password1': 'Hasło nie może składać się wyłącznie z cyfr.'})

        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
