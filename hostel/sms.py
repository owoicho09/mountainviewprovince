import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Booking






def send_sms(to, message):
    url = 'https://api.ng.termii.com/api/sms/send'
    payload = {
        'to': to,
        'from': settings.TERMII_SENDER_ID,
        'sms': message,
        'type': 'plain',
        'channel': 'generic',
        'api_key': settings.TERMII_API_KEY
    }

    try:
        response = requests.post(url, json=payload)

        # Print the response status code and text for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        # Convert response to JSON
        response_data = response.json()

        # Print the full JSON response for inspection
        print(f"Response Data: {response_data}")

        # Check for success based on response content
        if response.status_code == 200:
            # Look for a 'status' field or success message
            if response_data.get('message') == 'Successfully Sent' or response_data.get('status') == 'success':
                print('Message sent successfully')
                return True
            else:
                print(f"Failed to send message: {response_data.get('message', 'No message in response')}")
                return False
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def send_invoice(to, invoice_data):
    subject = 'Your Invoice from Mountain View Province'

    # Render HTML template
    html_message = render_to_string('studentdashboard/invoice.html', {'invoice': invoice_data})

    # Inline CSS

    plain_message = strip_tags(html_message)

    email = EmailMessage(subject, html_message, to=[to])
    email.content_subtype = 'html'

    try:
        email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"-----------Error sending email: {e}")




def send_balance_invoice(to, invoice_data):
    subject = 'Your Invoice from Mountain View Province'

    # Render HTML template
    html_message = render_to_string('studentdashboard/balance_invoice.html', {'invoice': invoice_data})

    # Inline CSS

    plain_message = strip_tags(html_message)

    email = EmailMessage(subject, html_message, to=[to])
    email.content_subtype = 'html'

    try:
        email.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"-----------Error sending email: {e}")







def send_payment_reminder():
    bookings = Booking.objects.filter(
        remaining_balance__gt=0,
        reminder_sent=False
    )
    for booking in bookings:
        # Calculate the threshold date based on the booking's individual booking_date
        threshold_date = booking.date + timedelta(days=1)

        # Dynamically get the base URL from settings for both dev and prod
        base_url = settings.BASE_URL  # Make sure BASE_URL is defined in your settings

        # Construct the payment URL
        payment_url = f"{base_url}/outstanding-payment/{booking.booking_id}/"

            # Send an email reminder
        send_mail(
            subject="Payment Reminder",
            message=f"Dear {booking.fullname},\n\n"
                    f"Your remaining balance of ₦{booking.remaining_balance} is due for your hostel booking. "
                    f"Please complete your payment soon.\n\nThank you."
                    f"Click the link to pay {payment_url}",
            from_email="noreply@hostelbooking.com",
            recipient_list=[booking.email],
        )





