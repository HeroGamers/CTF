FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    chromium \
    chromium-driver 

WORKDIR /app

COPY src/requirements.txt /
RUN pip3 install -r /requirements.txt

COPY src/ /app

COPY nginx.conf /etc/nginx/sites-available/default  
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod 600 /etc/supervisor/conf.d/supervisord.conf

ENV CHROME_OPTIONS="--headless --disable-gpu --no-sandbox --disable-dev-shm-usage"

RUN sh -c "echo 'DDC{f4ke_fl4g_test}' > /root/$(openssl rand -hex 12).txt"

ENV PYTHONUSERBASE="/tmp"
ENV TMPDIR=/tmp
RUN mkdir -p /tmp/.cache/selenium
RUN chmod -R 777 /tmp/.cache

RUN mkdir -p /app/static/receipts /var/backups/receipts
COPY backup.py /root/backup.py
RUN chmod 700 /root/backup.py

RUN mkdir -p /app/static/receipts /var/backups/receipts
COPY backup.py /root/backup.py
RUN chmod 700 /root/backup.py

COPY backup_loop.sh /root/backup_loop.sh
RUN chmod 700 /root/backup_loop.sh

RUN useradd -m ctfuser
RUN chown -R ctfuser:ctfuser /app

EXPOSE 80

CMD ["/usr/bin/supervisord"]
