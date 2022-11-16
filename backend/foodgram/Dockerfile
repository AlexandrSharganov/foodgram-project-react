FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip freeze > requirements.txt\
    pip3 install -r requirements.txt --no-cache-dir


# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
CMD ["python", "manage.py", "runserver"]