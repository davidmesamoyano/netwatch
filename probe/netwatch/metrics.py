"""Métricas que la sonda publica para que Prometheus las recoja en /metrics."""
from prometheus_client import Counter, Gauge, Histogram

LABELS = ["target", "kind"]

LATENCY = Gauge("netwatch_latency_ms", "Latencia media de la última ronda (ms)", LABELS)
JITTER = Gauge("netwatch_jitter_ms", "Jitter de la última ronda (ms)", LABELS)
LOSS = Gauge("netwatch_packet_loss_ratio", "Proporción de muestras perdidas en la última ronda (0-1)", LABELS)
UP = Gauge("netwatch_target_up", "1 si el destino respondió en la última ronda, 0 si no", LABELS)

# El histograma guarda cada muestra individual. Con él se calculan percentiles
# y el SLO de la semana 3 (p. ej. "99 % de las mediciones por debajo de 50 ms").
RTT = Histogram(
    "netwatch_rtt_seconds",
    "Tiempo de conexión TCP de cada muestra (s)",
    LABELS,
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2),
)
SAMPLES = Counter("netwatch_samples_total", "Muestras tomadas", LABELS + ["result"])
