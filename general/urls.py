from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yachts/', views.yacht_page, name='yacht_page'),
    path('yacht/<int:pk>/', views.yacht_detail, name='yacht_detail'),
    path('yacht/<int:yacht_id>/book/', views.book_yacht, name='book_yacht'),
    path('profile/', views.profile, name='profile'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('custom-admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('custom-admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('custom-admin/bookings/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('custom-admin/bookings/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('custom-admin/users/', views.admin_users, name='admin_users'),
] 