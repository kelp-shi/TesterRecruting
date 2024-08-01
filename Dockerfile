# Use a more recent Python image
FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=True

# Set the working directory
WORKDIR /app

# Copy local code to the container image
COPY . .

# Install build dependencies and MySQL client
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install production dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "testerRecruiting.wsgi:application"]