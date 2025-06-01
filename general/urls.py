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
] 