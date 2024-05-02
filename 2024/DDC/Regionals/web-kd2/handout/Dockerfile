FROM python:3.10

WORKDIR /app/website

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app/ ./

CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:80", "main:app"]
