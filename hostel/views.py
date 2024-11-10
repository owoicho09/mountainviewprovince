from django.shortcuts import render,redirect,get_object_or_404
from .models import Hostel,HostelType,Room,Booking,BedSpace,Notification,HostelFeatures
from studentauth.models import StudentProfile,CustomUser
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import reverse
from .sms import send_sms,send_invoice
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .remita import RemitaPayment
from django.conf import settings
import uuid
import random
import logging
import os

# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='studentauth:login')
def index(request):
    hostels = Hostel.objects.filter(active=True)

    if request.user.is_authenticated:
        user_gender = request.user.gender  # Assuming CustomUser has a 'gender' field
        print("User Gender:", request.user.gender)

        # Filter hostels based on user's gender
        if user_gender == 'male':
            hostels = hostels.filter(gender='male')
        elif user_gender == 'female':
            hostels = hostels.filter(gender='female')
        else:
            messages.error(request, 'You have not yet updated your gender, Do so and try again')
            hostels = Hostel.objects.none()
    context = {
        'hostels': hostels
    }

    return render(request,'hostel/index.html',context)


def detail_page(request, slug):
    hostels = get_object_or_404(Hostel,slug=slug)
    user = request.user
    try:
        school = user.school
    except AttributeError:
        school = None
    hostel_type = HostelType.objects.filter(hostel=hostels)


    context = {
        'hostels': hostels,
        'school':school,
        'hostel_type': hostel_type

    }

    return render(request, 'hostel/detail.html', context)

def room_type_page(request, hid):
    # Fetch the hostel using the hostel ID
    hostel = get_object_or_404(Hostel, hid=hid)
    hostel_typess = HostelType.objects.filter(hostel=hostel)
    features = HostelFeatures.objects.filter(hostel_type__in=hostel_typess)
    paystack_public_key = os.getenv('PAYSTACK_PUBLIC_KEY')

    print(f"Looking for Hostel with ID: {hid}")

    user = request.user
    school = getattr(user, 'school', None)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print(request.POST)

        selected_room_category = request.POST.get('selected_room_category')
        rate_type = request.POST.get('rate_type') or request.POST.get('hostel_rate')
        rate_price = request.POST.get('rate_price') or request.POST.get('selected_rate_price')

        print('Selected room ID:', selected_room_category)

        hostel_type = HostelType.objects.get(atid=selected_room_category)

        # Handle rate price based on the school and selected rate type
        if school.lower() == 'baze':
            rate_price = hostel_type.baze_price
        else:
            if rate_type == 'semester':
                rate_price = hostel_type.semester_rate
            elif rate_type == 'session':
                rate_price = hostel_type.session_rate
            else:
                return JsonResponse({'success': False, 'message': 'Invalid rate type selected.'}, status=400)

        try:
            available_rooms = Room.objects.filter(hostel_type=hostel_type, is_available=True)
            if not available_rooms.exists():
                return JsonResponse({'success': False, 'message': f'No rooms available for {hostel_type}.'}, status=404)

            room = random.choice(available_rooms)
            print(f'Selected room ID: {room.id}')

            fullname = getattr(user, 'fullname', None)
            email = getattr(user, 'email', None)
            phone = getattr(user, 'phone', None)
            student_id = getattr(user, 'student_id', None)

            if not fullname or not email:
                return JsonResponse({'success': False, 'message': 'Incomplete student profile information.'}, status=400)

            print(f'User info - Name: {fullname}, Email: {email}, School: {school}')

            booking = Booking.objects.create(
                hostel=hostel,
                hostel_type=hostel_type,
                room=room,
                fullname=fullname,
                email=email,
                phone=phone,
                school=school,
                rate_type=rate_type,
                rate_price=rate_price,
                payment_status='Processing',
            )

            room.current_occupancy += 1
            room.save()

            if user.is_authenticated:
                booking.user = user
                booking.save()

            print('---------', 'success')

            return JsonResponse({'success': True, 'redirect_url': f'/checkout/{booking.booking_id}'})

        except Exception as e:
            print(f"Error creating booking: {e}")
            return JsonResponse({'success': False, 'message': 'An error occurred while processing your booking.'}, status=500)

    context = {
        'hostel': hostel,
        'hostel_type': hostel_typess,
        'features': features,
        'school': school,
        'paystack_public_key': paystack_public_key
    }

    return render(request, 'hostel/room_type_page.html', context)



def shuffle(request, id):
    # Fetch the hostel type object or return 404 if not found
    hostel_type = get_object_or_404(HostelType, atid=id)

    # Fetch a random available room

    rooms = Room.objects.filter(hostel_type=hostel_type, is_available=True).order_by('?')[:1]

    if rooms.exists():
        room = rooms.first()  # Get the first room from the queryset
        data = {
            'room_number': room.room_number,  # Access the room instance
            'price': room.hostel_type.baze_price,
            'occupants': f"{room.current_occupancy}/{room.capacity}",  # Add occupants info

            # Access the price from the hostel type

            # Add any other fields necessary
        }
        return JsonResponse(data)

    # Return an error if no room is found
    return JsonResponse({'error': 'No room found'}, status=404)












@login_required(login_url='studentauth:login')
def checkout(request, booking_id):

    booking = Booking.objects.get(booking_id=booking_id)
    paystack_public_key = os.getenv('PAYSTACK_PUBLIC_KEY')

    print('----------', booking.email)

    print('======',booking.room)

    context = {
        'booking':booking,

        'paystack_public_key':paystack_public_key

    }

    return render(request,'hostel/checkout.html', context)

@login_required(login_url='studentauth:login')
def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')

    print(f"Success ID: {success_id}")
    print(f"Booking Total: {booking_total}")

    if success_id and booking_total:
        success_id = success_id.rstrip('/')
        booking_total = booking_total.rstrip('/')

        try:
            booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)
            print(f"Booking Found: {booking}")
            print('----------', booking.email)


            print('========',booking.payment_status)
            print("Booking Total:", booking_total)

            if booking.rate_price == Decimal(booking_total):
                if booking.payment_status == 'Processing':
                    booking.payment_status = 'Paid'
                    booking.is_active = True
                    booking.save()
                    print(booking.payment_status)
                    if booking.payment_status == 'Paid':
                        invoice_data = {
                            'booking_id': booking.booking_id,
                            'amount':booking_total,
                            'name': booking.fullname

                        }
                        send_invoice(request.user.email,invoice_data)

                    notification = Notification.objects.create(
                        booking=booking,
                        type='Booking Confirmed'
                    )
                    notification.user = request.user if request.user.is_authenticated else None
                    notification.save()

                    messages.success(request, 'Payment successful')
                else:
                    messages.success(request, f'Payment already made, thank you for your patronage {booking.fullname}')
            else:
                messages.warning(request, 'Payment manipulation detected, try again.')
            print('----------',booking.payment_status)
            print('--------',booking.email)

            # Pass the booking to the template
            context = {
                'booking': booking
            }
            return render(request, 'hostel/payment_success.html', context)

        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')

    else:
        messages.error(request, 'Missing payment details.')




def initialize_payment(request):
    print('POST Data:', request.POST)

    if request.method == 'POST':
        order_id = str(uuid.uuid4())   # Generate unique order ID
        amount = request.POST.get('amount')
        payer_name = request.POST.get('name')
        payer_email = request.POST.get('email')
        payer_phone = request.POST.get('phone')

        remita = RemitaPayment(order_id, amount, payer_name, payer_email, payer_phone)
        rrr = remita.initialize_payment()
        print('----------', rrr)
        print('----------', payer_name)
        print('----------', payer_email)
        print('----------', payer_phone)




        if rrr:
            # Redirect to Remita payment page
            remita_payment_url = f"https://remitademo.net/remita/ecomm/finalize.reg?rrr={rrr}&merchantId={settings.REMITA_MERCHANT_ID}"
            return redirect(remita_payment_url)

    return render(request, 'hostel/payment_form.html')

def verify_payment(request, rrr):
    remita = RemitaPayment(None, None, None, None, None)
    payment_status = remita.check_payment_status(rrr)

    if payment_status['status'] == '01':  # Successful payment status
        # Update the booking or any relevant model here
        return redirect('payment_success')
    else:
        return redirect('payment_failed')


def send_message(request):
    user = request.user
    phone = getattr(user, 'phone', None)

    message = 'Transport scheduled at 8:00 AM'

    if send_sms(phone, message):
        return JsonResponse({'success': True, 'message': 'SMS sent successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to send sms'})


def invoice(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id,user=request.user, payment_status='Paid')
    user = booking.user
    print(user)

    context = {
        'booking':booking,


    }
    return render(request,'studentdashboard/invoice.html',context)


