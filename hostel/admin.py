from django.contrib import admin
from django import forms

from hostel.models import Hostel,HostelType,HostelGallery,HostelFeatures,Room,Booking,BedSpace,Notification,HostelTypeGallery, Maintenance_request
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

class HostelTypeAdmin(admin.ModelAdmin):
    inlines = [HostelTypeGalleryInline]

    list_display = ('hostel', 'type', 'baze_price', 'semester_rate', 'session_rate')
    prepopulated_fields = {'slug': ('type',)}


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','fullname','hostel', 'hostel_type', 'room', 'rate_type','check_in_tracker','payment_status')
    list_filter = ['payment_status', 'hostel', 'hostel_type']

class RoomAdmin(admin.ModelAdmin):
    list_display = ('hostel_type', 'room_number', 'capacity', 'current_occupancy')



class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('user','issue_category', 'user_room_number', 'hostel_name')

    def user_room_number(self, obj):
        return obj.booking.room.room_number if obj.booking and obj.booking.room else 'N/A'
    user_room_number.short_description = 'Room Number'

    def hostel_name(self, obj):
        return obj.booking.room.hostel.name if obj.booking and obj.booking.room.hostel else 'N/A'
    hostel_name.short_description = 'Hostel'




#admin.site.register(Hostel, HostelAdmin)
admin.site.register(HostelType, HostelTypeAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(BedSpace)
admin.site.register(HostelGallery,HostelGalleryAdmin)
admin.site.register(HostelFeatures, HostelFeatureAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Notification)
admin.site.register(Maintenance_request, MaintenanceAdmin)

