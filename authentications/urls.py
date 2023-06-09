from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('Login/', views.loginUser, name="Login"),
    path('Logout/', views.LogoutUser, name="Logout"),
    path('', views.dashboard, name='dashboard'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('reset-instruction/', views.reset_instruction, name='reset-instruction'),
    path('edit/', views.edit, name='edit'),
    
    # for users to change their password
    path('password-change/',PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(),name='password_change_done'),
    
]
