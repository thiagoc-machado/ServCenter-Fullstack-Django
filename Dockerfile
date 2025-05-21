FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "servcenter.wsgi:application", "--bind", "0.0.0.0:8000"]