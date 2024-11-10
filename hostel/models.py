from django.db import models
from shortuuid.django_fields import ShortUUIDField
from studentauth.models import CustomUser
import string
from django.utils.text import slugify
import shortuuid
from django.conf import settings
from django.utils.safestring import mark_safe

# Create your models here.
STATUS = (
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled'),
    ('Not Available', 'Not Available'),
    ('Active', 'Active')
)

PAYMENT_STATUS = (
    ('Pending','Pending'),
    ('Processing', 'Processing'),
    ('Paid', 'Paid'),
    ('Declined', 'Declined'),
    ('In-review', 'In-review')

)

BED = (
    ('A,B,C', 'A,B,C'),


)

ISSUE_CATEGORY = (
   ('electrical issue', 'Electrical Issue'),
   ('plumbing', 'Plumbing'),
   ('appliances','Appliances'),
   ('lock/key issue', 'Lock/Key Issue'),
   ('others', 'Others')

)


NOTIFICATION_TYPE = (
    ('Booking Confirmed', 'Booking Confirmed'),
    ('Booking Cancelled', 'Booking Cancelled')

)
GENDER = (
    ('male','Male'),
    ('female', 'Female'),
    ('mixed', 'Mixed')


)


SCHOOL = (
    ('nile','Nile'),
    ('baze', 'Baze'),


)

RATING = (
    ('top', 'Top'),
    ('fair', 'Fair')

)


class Hostel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hostels', null=True,blank=True)
    name = models.CharField(max_length=200)
    hid = ShortUUIDField(unique=True, length=7, max_length=20, alphabet=string.ascii_letters + string.digits, primary_key=True)
    address = models.CharField(max_length=200)
    image = models.FileField(upload_to='hostel_gallery')
    description = models.CharField(max_length=1000,null=True,blank=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True, null=True, blank=True)
    gender = models.CharField(max_length=20,null=True,blank=True,choices=GENDER)
    rating = models.CharField(max_length=20, null=True, blank=True, choices=RATING)



    slug = models.SlugField(unique=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hostel_hostel'

    def thumbnail(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />")
        return "No Image"

    def __str__(self):
        return self.name if self.name else ''

    def hotel_gallery(self):
        return HostelGallery.objects.filter(hostel=self)

class HostelGallery(models.Model):
    hostel = models.ForeignKey(Hostel,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hostel_gallery')
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.ascii_letters + string.digits)

    def __str__(self):
        return self.hostel.name

    def thumbnail(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />")
        return "No Image"

    class Meta:
        verbose_name_plural = 'Hostel Gallery'


class HostelType(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hostel_gallery', null=True,blank=True)
    type = models.CharField(max_length=100)
    baze_price = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    semester_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    session_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    num_of_beds = models.PositiveIntegerField(default=1)
    parlour = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=2)
    atid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.ascii_letters + string.digits)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name_plural = 'Hostel Type'

    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.type) + '-' + str(uniqueid.lower())

        super(HostelType, self).save(*args, **kwargs)

    def hotel_gallery(self):
        return HostelTypeGallery.objects.filter(hostel_type=self)

    def hotel_feature(self):
        return HostelFeatures.objects.filter(hostel_type=self)


class HostelTypeGallery(models.Model):
    hostel_type = models.ForeignKey(HostelType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hostel_type_gallery')
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.ascii_letters + string.digits)

    def __str__(self):
        return self.hostel_type.type

    def thumbnail(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />")
        return "No Image"

    class Meta:
        verbose_name_plural = 'Hostel Type Gallery'

class HostelFeatures(models.Model):
    hostel_type = models.ForeignKey(HostelType,on_delete=models.CASCADE, null=True,blank=True)
    icon = models.CharField(max_length=100,null=True,blank=True)
    icon_type = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Hostel Features'


class Room(models.Model):
    hostel = models.ForeignKey(Hostel,on_delete=models.CASCADE)
    hostel_type = models.ForeignKey(HostelType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=5000)
    bed = models.CharField(max_length=10,null=True, blank=True, choices=BED)
    capacity = models.PositiveIntegerField(null=True, blank=True) #number of students this room can accomodate
    current_occupancy = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    fid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.ascii_letters + string.digits)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.current_occupancy >= self.capacity:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.room_number} '

    class Meta:
        verbose_name_plural = 'Room'


class BedSpace(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, related_name='beds')
    bed_type = models.CharField(max_length=20, choices=BED)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Bed {self.bed_type} in Room  {self.room.fid}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    hostel_type = models.ForeignKey(HostelType, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    school = models.CharField(max_length=20, choices=SCHOOL,null=True,blank=True)


    rate_type = models.CharField(max_length=10, choices=[('semester', 'Semester'), ('session', 'Session')], null=True, blank=True)
    rate_price = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)

    is_active = models.BooleanField(default=True)

    check_in_tracker = models.BooleanField(default=False, help_text='CHECK THIS BOX ONLY WHEN STUDENT CHECKS IN')
    check_out_tracker = models.BooleanField(default=False, help_text='CHECK THIS BOX ONLY WHEN STUDENT CHECKS OUT')

    date = models.DateTimeField(auto_now_add=True)
    stripe_payment = models.CharField(max_length=1000, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)

    success_id = ShortUUIDField(length=10, max_length=505, alphabet=string.ascii_letters + string.digits)
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.ascii_letters + string.digits)


    def __str__(self):
        return f'{self.hostel.name} - {self.booking_id} - {self.payment_status}- {self.room}'


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True, blank=True, related_name="user")
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = self.user.username if self.user else 'No User'
        booking_str = self.booking.booking_id if self.booking else 'No Booking'
        return f"{user_str} - {booking_str}"



class Maintenance_request(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    hostel=models.ForeignKey(Hostel, on_delete=models.SET_NULL,blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True,blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, blank=True, null=True)  # Link to user's booking

    request = models.CharField(max_length=1000,null=True, blank=True)
    issue_category = models.CharField(choices=ISSUE_CATEGORY, max_length=200)
    description = models.TextField(max_length=5000, null=True, blank=True)
    active = models.BooleanField(default=False)
    helpful = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="helpful")
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Maintenance Request"
        ordering = ["-date"]


    def room_number(self):
        return self.booking.room.room_number if self.booking and self.booking.room else 'N/A'

    def __str__(self):
        return f"{self.user}-{self.hostel.name}-{self.booking.room}"
