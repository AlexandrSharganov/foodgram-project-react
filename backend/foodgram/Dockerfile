FROM python:3.8-slim

WORKDIR /app

ADD . .

RUN pip freeze>requirements.txt\
    pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]