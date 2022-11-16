FROM python:3.8-slim

WORKDIR /app

ADD . .

RUN pip install -r /app/requirements.txt --no-cache-dir


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]