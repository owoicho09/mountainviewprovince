FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Install Nginx
RUN apt-get update && apt-get install -y nginx
RUN nginx -v
# Set up Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

# Expose port for Gunicorn (8000) and HTTP (Nginx will listen on 80)
EXPOSE 8000
EXPOSE 80

# Start Gunicorn and Nginx (using supervisord or directly in CMD)
CMD ["sh", "-c", "gunicorn accommodation.wsgi:application --bind 0.0.0.0:$PORT & nginx -g 'daemon off;'"]
