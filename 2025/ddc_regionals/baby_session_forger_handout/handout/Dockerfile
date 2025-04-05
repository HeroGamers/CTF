FROM ubuntu:24.04

RUN apt-get update && apt-get upgrade -y && apt-get install python3-flask -y

RUN mkdir /app

WORKDIR /app

COPY app.py /app
COPY flag.txt /app

CMD ["flask", "run", "-p", "80", "-h", "0.0.0.0"]
