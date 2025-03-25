from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import LoginSerializer, RegisterSerializer

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
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data
        return Response({"status": "Login realizado com sucesso!"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API para realizar o registro
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Nome de usuário já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
