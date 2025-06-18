from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
     path('profile/', views.profile, name='profile'),
     path('', views.home, name='home'),
     path('book/', views.book_computer, name='book_computer'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]