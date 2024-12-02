from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hostel.models import Booking,Notification,Hostel,HostelType,Review
from studentauth.models import CustomUser, StudentProfile




def landing_page(request):
    review = Review.objects.filter(active=True)


    context = {
        'review':review

    }

    return render(request, 'studentdashboard/landing_page.html', context)




def dashboard(request):
    user = request.user
    booking = Booking.objects.filter(user=user, payment_status='Paid').last()  # Fix .objects
    hostels = Hostel.objects.filter(active=True,rating='top')  # Fix .objects and filter for all active hostels
    female_hostels = Hostel.objects.filter(active=True, gender='female')
    male_hostels = Hostel.objects.filter(active=True, gender='male')




    user = request.user
    school = getattr(user, 'school', None)


    if booking:  # Check if a booking exists
        notifications = Notification.objects.filter(user=user, seen=False,booking=booking)

        context = {
            'booking': booking,
            'notifications': notifications,
            'hostels': hostels
        }

        return render(request, 'studentdashboard/empty.html', context)

    else:
        context = {

            'hostels': hostels,
            'female_hostels':female_hostels,
            'male_hostels':male_hostels,


            'school':school

        }
        return render(request,'studentdashboard/empty.html', context)

def notification(request):
    notification = Notification.objects.filter(user=request.user, seen='False')

    context = {
        'notification': notification

    }

    return render(request, 'studentdashboard/notification.html', context)





@login_required
def bookings(request):
    booking = Booking.objects.filter(user=request.user).order_by('-date')

    context = {
        'booking': booking,


    }

    return render(request, 'studentdashboard/bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id,user=request.user)
    context = {
        'booking':booking

    }
    return render(request,'studentdashboard/bookingdetails.html',context)


@login_required
def personalInformation(request):
    profile = StudentProfile.objects.get(user=request.user)

    context = {
        'profile':profile

    }

    return render(request, 'studentdashboard/personalinformation.html', context)