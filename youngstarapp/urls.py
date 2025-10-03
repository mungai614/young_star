# core/urls.py
from django.urls import path
from . import views
from .views import admin_dashboard
from .views import loan_inquiry_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add-contribution/', views.add_contribution, name='add_contribution'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('loan-inquiry/', loan_inquiry_view, name='loan_inquiry'),

]
