FROM ubuntu@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782

RUN apt-get update && apt-get upgrade -y && apt-get install socat -y

RUN mkdir /app
WORKDIR /app

COPY flag.txt /app
COPY tiny /app

RUN chmod +x /app/tiny
RUN useradd -ms /bin/bash ctf


USER ctf
EXPOSE 13337
CMD socat tcp-l:13337,reuseaddr,fork exec:./tiny,pty,echo=0,raw,iexten=0