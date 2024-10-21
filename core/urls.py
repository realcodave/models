from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.aboutUs, name='about'), 
    path('logout/', views.userLogout, name='logout'), 
    path('casting/', views.casting, name='casting'), 
    path('dashboard/', views.model_dashboard, name='dashboard'), 
    path('profile/', views.model_profile, name='profile'), 
    path('fetch_model_profile/', views.fetch_model_profile, name='fetch_model_profile'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register')
]