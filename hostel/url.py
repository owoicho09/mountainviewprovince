from django.urls import path
from . import views

app_name = 'hostel'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail_page/<slug:slug>',views.detail_page, name='detail_page'),
    path('room_type_page/<str:hid>/', views.room_type_page, name='room_type_page'),
    path('shuffle-room/<str:id>/', views.shuffle, name='shuffle_room'),
    path('invoice/<str:id>/',views.invoice,name='invoice'),

    path('checkout/<booking_id>', views.checkout, name='checkout'),
    path('success/<booking_id>/', views.payment_success, name='success'),

    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),
    path('verify-payment/<str:rrr>/', views.verify_payment, name='verify_payment'),

]