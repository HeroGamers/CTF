FROM alpine:3.21 AS builder
RUN apk add --no-cache gcc musl-dev
WORKDIR /src
COPY readflag.c .
RUN gcc readflag.c -o readflag

FROM python:3.12-alpine3.21
RUN pip install fastapi uvicorn pandas gunicorn
WORKDIR /app
COPY app.py .
COPY ctf_results.csv .
COPY --from=builder --chown=root:root /src/readflag /readflag
RUN chmod +s /readflag
COPY flag.txt /flag.txt
RUN chmod 600 /flag.txt

# Install dependencies
RUN apk add --no-cache git openssh ca-certificates tzdata sqlite wget curl bash

# Create a git user for Gitea
RUN addgroup -S git && adduser -S -G git git

# Set up Gitea by copying files from the Gitea image
RUN mkdir -p /app/gitea /usr/local/bin
COPY --from=docker.gitea.com/gitea:1.23.6 /usr/local/bin/gitea /usr/local/bin/gitea
COPY --from=docker.gitea.com/gitea:1.23.6 /app/gitea/gitea /app/gitea/gitea
RUN chmod +x /usr/local/bin/gitea /app/gitea/gitea

# Create required directories for Gitea and set ownership
RUN mkdir -p /data/gitea/conf /data/git /data/gitea/log && \
    chmod -R 755 /data/gitea /data/git && \
    chown -R git:git /data/gitea /data/git /app/gitea

COPY --chown=git:git app.ini /data/gitea/conf/app.ini
COPY --chown=git:git gitea.db /data/gitea/gitea.db

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

CMD ["/entrypoint.sh"]