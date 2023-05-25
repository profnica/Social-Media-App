from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('Login/', views.loginUser, name="Login"),
    path('Logout/', views.LogoutUser, name="Logout"),
]
