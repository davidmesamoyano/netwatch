#!/bin/sh
# Cambia en caliente la calidad de red de una sede (para la demo de "caos").
# Uso: ./sites/degrade.sh netwatch-site-madrid-1 300ms 50ms 10%
set -e
CONTAINER="$1"; DELAY="${2:-300ms}"; JITTER="${3:-50ms}"; LOSS="${4:-10%}"
docker exec "$CONTAINER" tc qdisc replace dev eth0 root netem delay "$DELAY" "$JITTER" loss "$LOSS"
echo "$CONTAINER -> delay=$DELAY jitter=$JITTER loss=$LOSS"
