from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name='LoginView'),
    path('logout/', views.LogoutView, name='LogoutView'),
    path('register/', views.RegisterView, name='RegisterView'),
    path('check_auth/', views.CheckAuthenticationView, name='CheckAuthentication'),
    path('clients/', views.Clients, name='Clients'),
    path('client/', views.ClientInfo, name='ClientInfoWithoutID'),
    path('client/<client_id>/', views.ClientInfo, name='ClientInfoWithID'),
    path('expert/', views.ExpertInfo, name='ExpertInfo'),
    path('experts/', views.Experts, name='Experts'),
    path('user/', views.UserInfoAdmin, name='UserInfoAdmin')
]