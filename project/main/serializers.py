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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_check']

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError("O campo Senha é obrigatório.")

        if len(password) < 6:
            raise serializers.ValidationError("A senha deve ter no mínimo 6 caracteres.")

        if len(password) > 12:
            raise serializers.ValidationError("A senha deve ter no máximo 12 caracteres.")

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("A senha deve conter no mínimo uma letra maiúscula.")

        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            raise serializers.ValidationError("A senha deve conter no mínimo um caractere especial.")

        return password

    def validate(self, data):
        password = data.get('password')
        password_check = data.get('password_check')

        if not password:
            raise serializers.ValidationError({"password": "O campo Senha é obrigatório."})

        if not password_check:
            raise serializers.ValidationError({"password_check": "O campo Confirmar Senha é obrigatório."})

        validated_password = self.validate_password(password)

        if password != password_check:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        data['password'] = validated_password
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
