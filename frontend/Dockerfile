# Stage 1: Build frontend
FROM node:20-bullseye AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y git python3 make g++ && rm -rf /var/lib/apt/lists/*
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve s Nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf:ro

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]