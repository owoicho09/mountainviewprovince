from django.urls import path
from . import views


app_name = 'studentdashboard'

urlpatterns = [
    path('', views.landing_page),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('bookings/', views.bookings, name='bookings'),
    path('booking_detail/<booking_id>/', views.booking_detail, name='booking_detail'),
    path('personal_information/', views.personalInformation, name='personal_information' )

]
