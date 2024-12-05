FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Install Nginx for static/media files
RUN apt-get update && apt-get install -y nginx

# Set up Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Start Nginx and Gunicorn
CMD service nginx start && gunicorn accommodation.wsgi:application --bind 0.0.0.0:8000
