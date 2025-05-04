FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN echo "DDC{fake-flag}" > /flag.txt

RUN useradd -m ctf
RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "1", "--worker-class", "gevent", "app:app"]
