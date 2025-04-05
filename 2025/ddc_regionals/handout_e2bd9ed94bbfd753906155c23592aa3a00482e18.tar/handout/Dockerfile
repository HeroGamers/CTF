FROM alpine@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
RUN apk update && apk add socat
COPY main /main
COPY flag.txt /flag.txt
CMD ["socat", "tcp-listen:1337,reuseaddr,fork,su=nobody", "exec:/main"]
