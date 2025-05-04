FROM node:23-alpine

ENV NODE_ENV=production

RUN addgroup -S nonroot && adduser -S nonroot -G nonroot

WORKDIR /app
COPY ./app/package.json package.json
COPY ./app/package-lock.json package-lock.json
RUN npm ci --omit=dev && npm cache clean --force

RUN echo "DDC{fake-flag}" > /flag.txt

COPY ./app .

USER nonroot
EXPOSE 80
CMD [ "node", "app.js" ]
