FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Set up Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port for Gunicorn
EXPOSE 8000

# Start Gunicorn and Nginx (using supervisord or directly in CMD)
CMD ["sh", "-c", "service nginx start && gunicorn accommodation.wsgi:application --bind 0.0.0.0:$PORT"]
