from rest_framework import serializers

class UsernameValidator:
    def __call__(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username deve ter ao menos 3 caracteres.")