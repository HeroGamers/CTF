FROM ubuntu:latest

USER root
WORKDIR /opt

RUN apt-get update --fix-missing && \
    apt-get install -y socat

COPY swappy .
RUN chmod +x swappy
EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./swappy,pty,raw,echo=0,stderr,setsid,sigint"]