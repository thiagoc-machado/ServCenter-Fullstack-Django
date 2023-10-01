
FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "servcenter.wsgi:application"]

