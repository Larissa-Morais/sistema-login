from django.urls import path
from .views import home, login_view, register_view, login_page, register_page
from django.shortcuts import redirect  # Importe o redirect

# Função que redireciona para a página de login
def redirect_to_login(request):
    return redirect('login_page')  # Redireciona para a página de login

urlpatterns = [
    path('', redirect_to_login),  # Rota principal que redireciona para a página de login
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('login-page/', login_page, name='login_page'),
    path('register-page/', register_page, name='register_page'),
    path('home/', home, name='home'),
]
