FROM ubuntu
RUN apt-get update && apt-get install -y socat qemu-system && rm -rf /var/lib/apt/lists/*
COPY src /challenge
WORKDIR /challenge
EXPOSE 1337
RUN chmod +x start.sh
CMD socat tcp-l:1337,reuseaddr,fork EXEC:"./start.sh",pty,stderr,echo=0,raw