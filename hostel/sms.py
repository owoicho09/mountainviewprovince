import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

    html_message = render_to_string('studentdashboard/invoice.html', {'invoice': invoice_data})
    plain_message = strip_tags(html_message)

    email = EmailMessage(subject, html_message, to=[to])
    email.content_subtype = 'html'

    email.send()