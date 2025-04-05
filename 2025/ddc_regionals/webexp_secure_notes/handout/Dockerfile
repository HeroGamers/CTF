FROM node:23-alpine3.20
RUN echo "DDC{fake-flag}" > /flag.txt
USER node
WORKDIR /app
COPY ./package.json package.json
COPY ./package-lock.json package-lock.json
RUN npm ci --omit=dev && npm cache clean --force
COPY public ./public
COPY views ./views
COPY app.js ./
EXPOSE 80
CMD ["node", "app.js"]
