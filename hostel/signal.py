from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from .sms import send_sms,send_invoice




