FROM alpine:3.21

RUN apk add --no-cache chromium nodejs npm

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY adminbot.js .

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

RUN adduser -H -D user
USER user
CMD ["node", "adminbot.js"]