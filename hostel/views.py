from django.shortcuts import render,redirect,get_object_or_404
from .models import Hostel,HostelType,Room,Booking,BedSpace,Notification,HostelFeatures,Block,Review
from studentauth.models import StudentProfile,CustomUser
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlockSerializer, RoomSerializer,HostelTypeSerializer,HostelSerializer
from django.db.models.functions import Coalesce

from django.http import JsonResponse
from django.urls import reverse
from .sms import send_sms,send_invoice,send_balance_invoice
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .remita import RemitaPayment
from django.conf import settings
from django.db.models import Sum,Value

from datetime import timedelta
from django.utils import timezone
import uuid
import random
import logging
import os

# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    hostels = Hostel.objects.filter(active=True).annotate(
        total_bedspaces=Coalesce(Sum('blocks__rooms__avilable_bedspace'), Value(0))
    )



    context = {
        'hostels': hostels,
    }

    return render(request,'hostel/index.html',context)


def detail_page(request, slug):
    hostels = get_object_or_404(Hostel,slug=slug)
    blocks = Block.objects.filter(hostel=hostels)

    blocks_with_bedspaces = []

    for block in blocks:
        # Calculate the total bedspaces for the current block
        total_bedspaces = block.rooms.aggregate(
            total_available_bedspaces=Sum('avilable_bedspace')
        )['total_available_bedspaces'] or 0

        blocks_with_bedspaces.append({
            'block': block,
            'total_bedspaces': total_bedspaces
        })

    room_block_type = HostelType.objects.filter(block__in=blocks)
    total_available_bed_space =  (hostel_type.total_available_bed_space() for hostel_type in room_block_type)
    rooms = Room.objects.filter(block__in=blocks, is_available=True)
    room_count = rooms.count()

    user = request.user
    try:
        school = user.school
    except AttributeError:
        school = None
    hostel_type = HostelType.objects.filter(hostel=hostels)


    context = {
        'hostels': hostels,
        'blocks':blocks,
        'rooms':rooms,
        'room_block_type':room_block_type,
        'total_available_bed_space':total_available_bed_space,
        'room_count':room_count,
        'school':school,
        'hostel_type': hostel_type,
        'blocks_with_bedspaces':blocks_with_bedspaces

    }

    return render(request, 'hostel/detail.html', context)



def block_rooms(request, slug):
    block = get_object_or_404(Block, slug=slug)
    hostel_types = HostelType.objects.filter(block=block).annotate(
        total_available_bedspaces=Sum('room__avilable_bedspace')
    )
    hostel_data = []
    for hostel_type in hostel_types:
        rooms = Room.objects.filter(hostel_type=hostel_type, is_available=True)
        hostel_data.append({
            'hostel_type': hostel_type,
            'total_available_bedspaces': hostel_type.total_available_bedspaces or 0,

            'rooms': rooms,
        })
    # Total bed spaces across all hostel types
    total_bedspaces = hostel_types.aggregate(Sum('total_available_bedspaces'))['total_available_bedspaces__sum'] or 0
    initial_payment = 0
    remaining_balance = 0
    rooms = Room.objects.filter(block=block)
    for room in rooms:
        room.available_bedspace = max(room.capacity - room.current_occupancy, 0)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        hostel_type_id = request.POST.get('hostel_type_id')
        room_id = request.POST.get('selected_room_category')
        rate_price = float(request.POST.get('rate_price'))
        rate_type = request.POST.get('rate_type')
        flexible_plan_type = request.POST.get('flexible_plan', None)

        hostel_type = HostelType.objects.get(atid=hostel_type_id)


        #calculate flexible rate
        if flexible_plan_type == 'true':
           flexible_plan_type = 'flexible plan'
           initial_payment = rate_price  # Adjust price for flexible plan
           rate_price = rate_price / 0.3
           remaining_balance = rate_price - initial_payment



        room = Room.objects.filter(fid=room_id, is_available=True).select_related('hostel_type', 'hostel').first()
        if not room:
            return JsonResponse({'success': False, 'message': 'Room fully booked.'}, status=404)
        print('-------',room)

        hostel = room.hostel

        booking = Booking.objects.create(
            hostel=hostel,
            block=block,
            hostel_type=hostel_type,
            room=room,
            rate_type=rate_type,
            rate_price=rate_price,
            flexible_plan_type=flexible_plan_type,
            initial_payment=initial_payment,
            remaining_balance=remaining_balance,
            payment_due_date=(timezone.now() + timedelta(days=30)) if rate_type == 'flexible plan' else None,
            payment_status='Processing',

        )



        return JsonResponse({'success': True, 'redirect_url': f'/bookingForm/{booking.booking_id}'})


    context = {
        'block': block,
        'rooms': rooms,
        'hostel_data':hostel_data,
        'hostel_types':hostel_types,
        'total_bedspaces':total_bedspaces
    }
    return render(request, 'hostel/selectroomPage.html', context)




def room_type_page(request, hid):
    # Fetch the hostel using the hostel ID
    hostel = get_object_or_404(Hostel, hid=hid)
    hostel_typess = HostelType.objects.filter(hostel=hostel).annotate(
        total_available_bedspaces=Sum('room__avilable_bedspace')
    )

    hostel_data = []
    for hostel_type in hostel_typess:
        rooms = Room.objects.filter(hostel_type=hostel_type, is_available=True)
        hostel_data.append({
            'hostel_type': hostel_type,
            'rooms': rooms,
        })

    # Total bed spaces across all hostel types
    total_bedspaces = hostel_typess.aggregate(Sum('total_available_bedspaces'))['total_available_bedspaces__sum'] or 0
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
        'hostel_data': hostel_data,
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







def bookingForm(request, booking_id):

    booking = Booking.objects.get(booking_id=booking_id)
    flexible_plan_type = booking.flexible_plan_type

    block = booking.block
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        school = request.POST.get('institution')
        gender = request.POST.get('gender')

        booking.fullname=fullname
        booking.email=email
        booking.phone=phone
        booking.school=school
        booking.gender=gender



        booking.save()

        if block.gender == gender:
            return redirect(reverse('hostel:checkout', args=[booking.booking_id]))
        else:
           messages.warning(request,f'This is a {block.gender} Block, your gender selection does not match this block')

    context = {
        'booking':booking,
        'flexible_plan_type': flexible_plan_type,

    }

    return render(request,'hostel/bookingForm.html', context)






def checkout(request, booking_id):

    booking = Booking.objects.get(booking_id=booking_id)
    paystack_public_key = os.getenv('PAYSTACK_PUBLIC_KEY')
    flexible_plan_type = booking.flexible_plan_type
    rate_type = booking.rate_type

    context = {
        'booking':booking,
        'rate_type':rate_type,
        'flexible_plan_type':flexible_plan_type,
        'paystack_public_key':paystack_public_key

    }

    return render(request,'hostel/checkout.html', context)

def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')



    if success_id and booking_total:
        success_id = success_id.rstrip('/')
        booking_total = booking_total.rstrip('/')

        try:
            booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)

            if booking.rate_price == Decimal(booking_total):
                if booking.payment_status == 'Processing':
                    booking.payment_status = 'Paid'
                    booking.is_active = True
                    room = booking.room
                    room.current_occupancy += 1
                    room.save()
                    booking.save()
                    print(booking.payment_status)
                    if booking.payment_status == 'Paid':
                        invoice_data = {
                            'booking_id': booking.booking_id,
                            'amount':booking_total,
                            'name': booking.fullname,
                            'date':booking.date,
                            'rate_price':booking.rate_price,
                            'payment_status':booking.payment_status,
                            'rate_type':booking.rate_type,
                            'outstanding':booking.remaining_balance,
                            'initial_payment':booking.initial_payment,
                            'hostel_type':booking.hostel_type,
                            'flexible_plan_type':booking.flexible_plan_type

                        }
                        send_invoice(booking.email,invoice_data)

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


def Review(request):
    if request.method == 'POST':
        fullname = request.method.get('fullname')
        rating = request.method.get('rating')
        review = request.method.get('review')

        Review.objects.create(
            fullname=fullname,
            rating=rating,
            review=review

        )
        return JsonResponse({'data': 'Review Submitted', 'icon': 'success'})

def pay_outstanding_balance(request,booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    fullname = booking.email
    paystack_public_key = os.getenv('PAYSTACK_PUBLIC_KEY')

    print('--',fullname)
    context = {
        'booking':booking,
        'paystack_public_key':paystack_public_key

    }
    return render(request,'hostel/pay_outstanding_balance.html', context)


def outstanding_payment_success(request, booking_id):
    # Fetch booking_id from the URL if not passed explicitly
    booking_id = request.GET.get('booking_id', booking_id)
    booking_total = request.GET.get('booking_total')

    if booking_total:
        try:
            # Ensure booking_total is converted to a Decimal
            booking_total = Decimal(booking_total)

            # Retrieve the booking object
            booking = Booking.objects.get(booking_id=booking_id)
            if booking.remaining_balance == booking_total:
                # Update the booking's remaining balance
                booking.remaining_balance = Decimal('0.00')
                booking.save()
                if booking.payment_status == 'Paid':
                    invoice_data = {
                        'booking_id': booking.booking_id,
                        'amount': booking_total,
                        'name': booking.fullname,
                        'date': booking.date,
                        'rate_price': booking.rate_price,
                        'payment_status': booking.payment_status,
                        'rate_type': booking.rate_type,
                        'outstanding': booking_total,
                        'initial_payment': booking.initial_payment,
                        'hostel_type': booking.hostel_type

                    }
                    send_balance_invoice(booking.email, invoice_data)

            else:
                messages.warning(request, 'Payment manipulation detected. Please try again.')

            # Prepare the context for rendering the success page
            context = {
                'booking': booking,
                'booking_total':booking_total
            }
            return render(request, 'hostel/outstanding_payment_success.html', context)

        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
            return redirect('error_page')  # Replace with the appropriate error page

        except ValueError:
            messages.error(request, 'Invalid payment amount.')
            return redirect('error_page')  # Replace with the appropriate error page
    else:
        messages.error(request, 'Missing payment details.')


#API FOR RETURN ING STUDENTS

@api_view(['GET'])
def get_hostels(request):
    try:
        hostels = Hostel.objects.filter(active=True)
        serializer = HostelSerializer(hostels, many=True)
        return Response({'hostels': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_blocks(request):
    hostel_id = request.GET.get('hostel_id')
    if not hostel_id:
        return Response({'error': 'Hostel ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        hostel = Hostel.objects.get(hid=hostel_id)
        blocks = Block.objects.filter(hostel=hostel)
        serializer = BlockSerializer(blocks, many=True)
        return Response({'blocks': serializer.data}, status=status.HTTP_200_OK)
    except Hostel.DoesNotExist:
        return Response({'error': 'Hostel not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_hostel_types(request):
    block_id = request.GET.get('block_id')
    if not block_id:
        return Response({'error': 'Block ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        block = Block.objects.get(bid=block_id)
        hostel_type = HostelType.objects.filter(block=block)
        serializer = HostelTypeSerializer(hostel_type, many=True)
        return Response({'hostel_type': serializer.data}, status=status.HTTP_200_OK)
    except HostelType.DoesNotExist:
        return Response({'error': 'HostelType not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_rooms(request):
    block_id = request.GET.get('block_id')
    if not block_id:
        return Response({'error': 'Block ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        block = Block.objects.get(bid=block_id)
        rooms = Room.objects.filter(block=block, is_available=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response({'rooms': serializer.data}, status=status.HTTP_200_OK)
    except Block.DoesNotExist:
        return Response({'error': 'Block not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)