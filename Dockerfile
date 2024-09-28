FROM python:3.12

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uwsgi", "--socket", ":8001", "--module", "app.wsgi", "--py-autoreload", "1", "--logto", "/tmp/mylog.log"]