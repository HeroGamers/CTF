#!/bin/sh

cd /app
su -s /bin/sh nobody -c "gunicorn --bind 127.0.0.1:8000 -k uvicorn.workers.UvicornWorker app:app --workers 2 --timeout 30" &

su -s /bin/sh git -c "/app/gitea/gitea web --config /data/gitea/conf/app.ini" &

wait