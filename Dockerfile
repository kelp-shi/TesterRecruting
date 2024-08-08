FROM python:3.12

ENV APP_HOME=/src

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8080"]