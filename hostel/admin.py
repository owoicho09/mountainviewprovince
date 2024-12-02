from django.contrib import admin
from django import forms
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.admin import SimpleListFilter

from hostel.models import Hostel,Block,HostelType,HostelGallery,HostelFeatures,Room,Booking,BedSpace,Notification,HostelTypeGallery, Maintenance_request,ReminderDays,Review
# Register your models here.


class HostelGalleryInline(admin.TabularInline):

    model = HostelGallery


class HostelGalleryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'hostel')

class HostelTypeGalleryInline(admin.TabularInline):
    model = HostelTypeGallery

class HostelTypeGalleryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'hostel_type')



class HostelFeatureInline(admin.TabularInline):

    model = HostelFeatures

class HostelFeatureAdmin(admin.ModelAdmin):
    list_display = ('hostel_type', 'name')


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        if user is None:
            raise forms.ValidationError('User must be selected.')
        return cleaned_data


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    inlines = [HostelGalleryInline]
    list_display = ('thumbnail', 'name', 'address', 'gender')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('user', 'name', 'address','image', 'description', 'phone', 'email','gender','active','rating', 'hid', 'slug')

    def save_model(self, request, obj, form, change):
        obj.save()  # Ensure the Hostel instance is saved first

class BlockAdmin(admin.ModelAdmin):

    list_display = ('hostel', 'gender', 'name')
    prepopulated_fields = {'slug': ('name',)}


class HostelTypeAdmin(admin.ModelAdmin):
    inlines = [HostelTypeGalleryInline]

    list_display = ('block', 'type', 'baze_price', 'semester_rate', 'session_rate')
    prepopulated_fields = {'slug': ('type',)}



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('fullname','review', 'rating')

class RemainingBalanceFilter(SimpleListFilter):
    title = 'Remaining Balance'  # Display name in the admin filter
    parameter_name = 'remaining_balance'  # Query parameter name

    def lookups(self, request, model_admin):
        # Define filter options
        return [
            ('has_balance', 'Has Remaining Balance'),
            ('no_balance', 'No Remaining Balance'),
        ]

    def queryset(self, request, queryset):
        # Filter the queryset based on the selected option
        if self.value() == 'has_balance':
            return queryset.filter(remaining_balance__gt=0)
        elif self.value() == 'no_balance':
            return queryset.filter(remaining_balance__lte=0)
        return queryset




class ReminderDaysAdmin(admin.ModelAdmin):
    list_display = ('days', 'date')
    search_fields = ('days',)




class BookingAdmin(admin.ModelAdmin):
    list_display = ('fullname','hostel', 'hostel_type', 'room','remaining_balance', 'rate_type','check_in_tracker','payment_status')
    list_filter = ['payment_status',RemainingBalanceFilter, 'hostel', 'hostel_type','reminder_sent','rate_type']
    search_fields = ('fullname', 'email')

    actions = ['send_payment_reminders']  # Add the custom action to the admin panel

    def send_payment_reminders(self, request, queryset):
        reminder_days_setting = ReminderDays.objects.first()  # Assuming only one reminder setting exists
        if not reminder_days_setting:
            self.message_user(request, "Reminder settings are not configured. Please set the reminder days.",
                              level='error')
            return

        reminder_days = reminder_days_setting.days
        current_date = now()

        for booking in queryset:
            if booking.remaining_balance > 0 and not booking.reminder_sent:
                threshold_date = booking.date + timedelta(days=reminder_days)

                base_url = settings.BASE_URL
                payment_url = f"{base_url}/outstanding-payment/{booking.booking_id}"

                send_mail(
                    subject="Payment Reminder",
                    message=f"Dear {booking.fullname},\n\n"
                            f"Your remaining balance of ₦{booking.remaining_balance} is due for your hostel booking. "
                            f"Please complete your payment soon.\n\nThank you.\n"
                            f"Click the link to pay: {payment_url}",
                    from_email="noreply@hostelbooking.com",
                    recipient_list=[booking.email],
                )

                booking.reminder_sent = True
                booking.save()

        self.message_user(request, f"Payment reminders have been sent to {queryset.count()} selected bookings.")


class RoomAdmin(admin.ModelAdmin):
    list_display = ('hostel_type','block', 'room_number', 'capacity', 'current_occupancy')



class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('user','issue_category', 'user_room_number', 'hostel_name')

    def user_room_number(self, obj):
        return obj.booking.room.room_number if obj.booking and obj.booking.room else 'N/A'
    user_room_number.short_description = 'Room Number'

    def hostel_name(self, obj):
        return obj.booking.room.hostel.name if obj.booking and obj.booking.room.hostel else 'N/A'
    hostel_name.short_description = 'Hostel'




admin.site.register(Block, BlockAdmin)
admin.site.register(HostelType, HostelTypeAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(BedSpace)
admin.site.register(HostelGallery,HostelGalleryAdmin)
admin.site.register(HostelFeatures, HostelFeatureAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(ReminderDays, ReminderDaysAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Notification)
admin.site.register(Maintenance_request, MaintenanceAdmin)

