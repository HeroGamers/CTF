FROM python:alpine
RUN apk --no-cache add chromium chromium-chromedriver tini build-base libffi-dev
RUN pip install flask && pip install selenium==4.10.0
RUN pip install flask_session

WORKDIR /app
COPY *.py .
COPY ./templates/index.html ./templates/index.html

ENV H_SITEKEY H_SITEKEY
ENV H_SECRET H_SECRET
ENV SECRET_KEY SECRET_KEY
ENV FLAG hkcert23{FLAG}
ENV HOSTNAME wishlist-ftxfca.hkcert23.pwnable.hk:28015

USER nobody
EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python","server.py"]