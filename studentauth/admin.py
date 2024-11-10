from django.contrib import admin
from .models import CustomUser, StudentProfile
from hostel.models import Booking,Hostel
from django.contrib.admin import SimpleListFilter

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    search_fields =['fullname', 'student_id']
    list_display =['student_id', 'email', 'phone', 'gender']




class PaymentStatusFilter(SimpleListFilter):
    title = 'Payment Status'
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return [
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Paid', 'Paid'),
            ('Declined', 'Declined'),
            ('In-review', 'In-review'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__booking__payment_status=self.value())
        return queryset


class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['fullname', 'user__student_id']
    list_display = ['fullname', 'user_gender','get_hostel_from_booking','get_payment_status']
    list_filter = ['gender','hostel',PaymentStatusFilter]

    def get_hostel_from_booking(self, obj):
        # Fetch the latest booking for this user and return the related hostel name
        booking = Booking.objects.filter(user=obj.user).first()  # Fetch the first (or latest) booking
        if booking and booking.hostel:
            return booking.hostel.name  # Assuming the Hostel model has a 'name' field
        return "No Hostel Booked"

    get_hostel_from_booking.short_description = 'Booked Hostel'

    def get_payment_status(self, obj):
        # Use filter() to handle multiple bookings
        bookings = Booking.objects.filter(user=obj.user)
        if bookings.exists():
            # Get the first booking
            booking = bookings.first()
            return booking.payment_status
        return 'No Booking'

    get_payment_status.short_description = 'Payment Status'


    def user_studentId(self, obj):
        return obj.user.student_id
    user_studentId.short_description = 'Student ID'

    def user_fullname(self, obj):
        return obj.user.fullname

    user_fullname.short_description = 'FullName'

    def user_gender(self, obj):
        return obj.user.gender



    user_gender.short_description = 'Gender'

    ordering = ['user']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
