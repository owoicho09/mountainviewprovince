from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import string
from django.apps import apps

# Create your models here.

SCHOOL = (
    ('nile','Nile'),
    ('baze', 'Baze'),


)


GENDER = (
    ('male','Male'),
    ('female', 'Female'),


)

COUNTRY =(
    ('nigeria', 'NIGERIA'),
    ('ghana','GHANA'),
    ('southafrica', 'SOUTH AFRICA'),

)

IDENTITY_TYPE = (
    ('school id', 'SCHOOL ID'),
    ('acceptance letter', 'ACCEPTANCE LETTER'),
    ('school fees receipt', 'SCHOOL FEES RECEIPT')

)

HOSTEL = (
    ('white house','WHITE HOUSE'),
    ('jabi', 'JABI')

)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.user.id, filename}.{ext}'
    return f"user_{instance.user.id}/{filename}"



class CustomUser(AbstractUser):
    name_regex = RegexValidator(regex=r'^[a-zA-Z\s]+$', message="Full name must contain only letters and spaces.")



    fullname = models.CharField(max_length=100, null=True, blank=True, validators=[name_regex])
    student_id = models.CharField(max_length=100,unique=True, null=True, blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True,unique=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True,unique=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    school = models.CharField(max_length=20, choices=SCHOOL,null=True,blank=True)
    level = models.CharField(max_length=20,null=True, blank=True)
    next_of_kin_fullname = models.CharField(max_length=100, null=True, blank=True)
    kin_phone = models.CharField(max_length=50,null=True, blank=True)
    kin_address = models.CharField(max_length=100, null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid clash
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Custom related name to avoid clash
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='custom_user_permissions',
    )

    def clean(self):
        super().clean()
        if not self.email and not self.phone:
            raise ValidationError('Either email or phone must be provided.')
    

    def __str__(self):
        return self.email

class StudentProfile(models.Model):
    pid = ShortUUIDField(length=7,max_length=15,alphabet=string.ascii_letters + string.digits,primary_key=True)
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE,unique=True)
    fullname = models.CharField(max_length=100,null=True,blank=True)
    student_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True,unique=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(upload_to=user_directory_path, default='default.jpg', null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    country = models.CharField(max_length=20, choices=COUNTRY, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    hostel = models.CharField(max_length=200,choices=HOSTEL, null=True,blank=True)
    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.FileField(upload_to=user_directory_path, null=True, blank=True)


    paid = models.BooleanField(default=False)

    date = models.DateField(auto_now_add=True)

    class meta:
        ordering = 'date'

    def get_booking_model(self):
        return apps.get_model('hostel.Booking')

    def get_hostel_model(self):
        return apps.get_model('hostel.Hostel')

    def __str__(self):

            return f'{self.fullname}'

