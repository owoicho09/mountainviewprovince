from django.urls import path
from . import views

app_name = 'hostel'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail_page/<slug:slug>',views.detail_page, name='detail_page'),
    path('block/<slug:slug>/', views.block_rooms, name='block_rooms'),

    path('room_type_page/<str:hid>/', views.room_type_page, name='room_type_page'),
    path('shuffle-room/<str:id>/', views.shuffle, name='shuffle_room'),
    path('invoice/<str:id>/',views.invoice,name='invoice'),
    path('bookingForm/<booking_id>', views.bookingForm, name='bookingForm'),
    path('checkout/<booking_id>', views.checkout, name='checkout'),
    path('success/<booking_id>/', views.payment_success, name='success'),
    path('review/', views.Review, name='review'),

    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),
    path('verify-payment/<str:rrr>/', views.verify_payment, name='verify_payment'),
    path('outstanding-payment/<str:booking_id>/', views.pay_outstanding_balance),
    path('outstandng_payment_success/<booking_id>/', views.outstanding_payment_success, name='outstandng_payment_success'),

    #API FOR BOOKING
    path('api/get_hostels/', views.get_hostels),
    path('api/get_blocks/', views.get_blocks),
    path('api/get_hostel_types/', views.get_hostel_types),
    path('api/get_rooms/', views.get_rooms)



]