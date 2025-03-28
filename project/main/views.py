from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import LoginSerializer, RegisterSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Função para renderizar a página de login
def login_page(request):
    return render(request, 'login.html')

# Função para renderizar a página de registro
def register_page(request):
    return render(request, 'register.html')

# Função para renderizar a página inicial
def home(request):
    return render(request, 'home.html')

# API para realizar o login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"status": "Login realizado com sucesso!"}, status=200)
    else:
        return Response({"error": "Credenciais inválidas!"}, status=400)
    
# API para realizar o registro
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Nome de usuário já cadastrado."}, status=400)

    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Cadastro realizado com sucesso!"})
    
    return JsonResponse(serializer.errors, status=400)
