FROM python:3.14-rc-alpine3.21
RUN pip install flask

WORKDIR /app
COPY . .

RUN adduser -H -D user
USER user
CMD ["python", "app.py"]