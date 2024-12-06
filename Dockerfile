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

# Define the port environment variable (use 8000 as default)
ENV PORT 8000

# Use supervisord to manage Gunicorn and Nginx processes
RUN apt-get install -y supervisor

# Create supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start both Gunicorn and Nginx with supervisord
CMD ["/usr/bin/supervisord"]
