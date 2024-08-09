# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app
ENV PORT 8080

# Set work directory
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files and apply migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Run gunicorn
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"]