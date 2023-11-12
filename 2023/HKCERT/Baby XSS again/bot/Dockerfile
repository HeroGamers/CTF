FROM python:alpine
RUN apk --no-cache add chromium chromium-chromedriver tini build-base libffi-dev
RUN pip install flask && pip install selenium==4.10.0

WORKDIR /app
COPY *.py .

ENV H_SITEKEY your-h_sitekey
ENV H_SECRET your-h_secret
ENV FLAG your-flag
ENV HOSTNAME babyxss-k7ltgk.hkcert23.pwnable.hk:28232

USER nobody
EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python","server.py"]