# oculus
CESNET Oculus Earth remote sensing visualization software


# Certbot

```Dockerfile
# frontned/Dockerfile

# ...
# Stage 2: Nginx
FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /data

COPY --from=builder /app/dist /usr/share/nginx/html

# Uncomment line below
COPY ./nginx/default_httpOnly.conf /etc/nginx/conf.d/default.conf

# Comment line below
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

Build `nginx` and `certbot` container: 

```bash
docker compose build --no-cache certbot
docker compose build --no-cache nginx
```

Then run: 

```bash
docker compose run --rm --entrypoint "certbot certonly --webroot -w /var/www/html --email jirimatejka@cesnet.cz -d oculus.cesnet.cz --agree-tos --no-eff-email" certbot
```

Change `frontend/Dockerfile` again:

```Dockerfile
# frontned/Dockerfile

# ...
# Stage 2: Nginx
FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /data

COPY --from=builder /app/dist /usr/share/nginx/html

# Comment line below
# COPY ./nginx/default_httpOnly.conf /etc/nginx/conf.d/default.conf

# Uncomment line below
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

Build `nginx` and `certbot` container again: 

```bash
docker compose build --no-cache certbot
docker compose build --no-cache nginx
```

Then 

```bash
docker compose up
```

...and enjoy. Hopefully

