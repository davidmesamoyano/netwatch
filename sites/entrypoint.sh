#!/bin/sh
# Aplica latencia, jitter y pérdida a la interfaz de red del contenedor y arranca nginx.
# Necesita la capacidad NET_ADMIN (en docker-compose: cap_add: [NET_ADMIN]).
set -e
DELAY="${DELAY:-0ms}"
JITTER="${JITTER:-0ms}"
LOSS="${LOSS:-0%}"
IFACE="${IFACE:-eth0}"

tc qdisc replace dev "$IFACE" root netem delay "$DELAY" "$JITTER" loss "$LOSS"
echo "Sede ${SITE_NAME:-?}: delay=$DELAY jitter=$JITTER loss=$LOSS en $IFACE"

exec nginx -g 'daemon off;'
