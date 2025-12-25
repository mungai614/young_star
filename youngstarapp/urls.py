# core/urls.py
from django.urls import path
from . import views
from .views import admin_dashboard, rules
from .views import loan_inquiry_view
from .views import (
    admin_dashboard,
    loan_inquiry_view,
    member_detail,  # <- ADD THIS
)


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
path('member/<int:user_id>/', member_detail, name='member_detail'),
path('rules/', views.rules, name='rules'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]
