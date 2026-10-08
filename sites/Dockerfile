# "Sede" simulada: un nginx cuya red se degrada con tc netem al arrancar.
FROM nginx:1.27-alpine
RUN apk add --no-cache iproute2-tc
COPY entrypoint.sh /entrypoint.sh
COPY index.html /usr/share/nginx/html/index.html
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
