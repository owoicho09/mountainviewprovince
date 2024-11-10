from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from .sms import send_sms,send_invoice

@receiver(post_save, sender=Booking)
def send_invoice_on_payment(sender, instance, **kwargs):
    # Check if the payment_status was set to 'Paid'
    if instance.payment_status == 'Paid':
        # Prepare invoice data
        invoice_data = {
            'booking_id': instance.booking_id,
            'amount': instance.rate_price,  # Adjust to match your model's total field
            'name': instance.fullname
        }
        # Send the invoice email
        send_invoice(instance.email, invoice_data)
