FROM python:3.8-slim

WORKDIR /app

ADD . .

RUN python -m pip install --upgrade pip\
    pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]