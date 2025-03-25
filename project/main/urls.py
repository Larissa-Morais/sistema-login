from django.urls import path
from .views import home, login_view, register_view, login_page, register_page

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register-page/', register_page, name='register_page'),
    path('login/', login_view, name='login'),
    path('login-page/', login_page, name='login_page'),
    path('home/', home, name='home'),
]