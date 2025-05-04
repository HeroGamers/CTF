FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg curl supervisor \
 && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc \
    | gpg --dearmor -o /usr/share/keyrings/mongodb-server-8.0.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg] \
    http://repo.mongodb.org/apt/debian bookworm/mongodb-org/8.0 main" \
    | tee /etc/apt/sources.list.d/mongodb-org-8.0.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    mongodb-org \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /data/db /var/log/supervisor \
 && chown -R mongodb:mongodb /data/db

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
