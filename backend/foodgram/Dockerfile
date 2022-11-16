FROM python:3.8-slim

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]