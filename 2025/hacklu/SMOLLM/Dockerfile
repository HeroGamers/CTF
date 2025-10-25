FROM ubuntu:noble-20251001@sha256:66460d557b25769b102175144d538d88219c077c678a49af4afca6fbfc1b5252

RUN useradd --create-home ctf && \
    chown -R root:root /home/ctf && \
    chmod a+rx /home/ctf

WORKDIR /home/ctf
# libraries are default from this image, only provided to make local exploitation easier
COPY ld-linux-x86-64.so.2 libc.so.6 ynetd smollm .

EXPOSE 1024
CMD ["sh", "-c", "echo \"$FLAG\" > /home/ctf/flag && ./ynetd -u ctf /home/ctf/smollm"]
