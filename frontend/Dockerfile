FROM node:20-bookworm-slim AS build

WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@10.9.2 \
    && npm ci --include=dev --no-audit --no-fund --loglevel=error \
    && test -x node_modules/.bin/vite
COPY . .
RUN ./node_modules/.bin/vite build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
