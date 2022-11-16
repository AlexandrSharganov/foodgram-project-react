FROM python:3.8-slim

WORKDIR /app

ADD . .

RUN pip install -r /app/requirements.txt


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]