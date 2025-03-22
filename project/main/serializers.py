from rest_framework import serializers
from django.contrib.auth.models import User
from .validators import UsernameValidator

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UsernameValidator()])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Senha incorreta!")
        
        return user
    

class RegisterSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_check']

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user