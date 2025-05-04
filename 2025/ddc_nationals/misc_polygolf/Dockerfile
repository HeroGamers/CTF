FROM python:3.12-alpine3.21
RUN pip install flask pycryptodome
RUN apk add --no-cache deno
WORKDIR /app
COPY app.py .
COPY templates templates
CMD ["python3", "app.py"]