from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk_test>/', views.customers, name='customers'),
    path('create_order/<str:pk>/', views.createOrder, name='create-order'),
    path('update/<str:pk>/', views.updateOrder, name='update-order'),
    path('delete/<str:pk>/', views.deleteOrder, name='delete-order'),
    path('login/',views.LoginPage, name='login'),
    path('logout/',views.Logout, name='logout'),
    path('register/',views.Register, name='register'),
    path('users/', views.UserPage, name='users'),
    path('settings/', views.AccountSetting, name='settings'),


]
