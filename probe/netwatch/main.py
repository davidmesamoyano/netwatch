"""Punto de entrada de la sonda NetWatch.

Bucle: cada `interval_seconds` mide todos los destinos en paralelo, actualiza las
métricas y deja un resumen en el log.
Métricas en http://0.0.0.0:PORT/metrics y estado de salud en /healthz.
"""
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor

from netwatch import metrics
from netwatch.config import Config, Target, load_config
from netwatch.measure import take_samples
from netwatch.server import Health, start_server
from netwatch.stats import summarize

log = logging.getLogger("netwatch")


def probe_target(target: Target, cfg: Config) -> None:
    samples = take_samples(target.host, target.port, cfg.samples, cfg.timeout_seconds)
    s = summarize(samples)
    labels = {"target": target.name, "kind": target.kind}

    for rtt in samples:
        result = "ok" if rtt is not None else "fail"
        metrics.SAMPLES.labels(**labels, result=result).inc()
        if rtt is not None:
            metrics.RTT.labels(**labels).observe(rtt / 1000)

    metrics.UP.labels(**labels).set(1 if s.up else 0)
    metrics.LOSS.labels(**labels).set(s.loss_ratio)
    if s.up:
        metrics.LATENCY.labels(**labels).set(s.latency_ms)
        metrics.JITTER.labels(**labels).set(s.jitter_ms)
        log.info("%-15s latencia=%7.1f ms  jitter=%6.1f ms  pérdida=%3.0f %%",
                 target.name, s.latency_ms, s.jitter_ms, s.loss_ratio * 100)
    else:
        log.warning("%-15s CAÍDO (todas las muestras fallaron)", target.name)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(os.getenv("NETWATCH_CONFIG", "config.yaml"))
    port = int(os.getenv("NETWATCH_PORT", "8000"))

    # Sana si ha terminado una ronda en los últimos 3 intervalos (mínimo 60 s)
    health = Health(max_age_seconds=max(3 * cfg.interval_seconds, 60))
    start_server(port, health)
    log.info("NetWatch arrancado: %d destinos, métricas en :%d/metrics y salud en /healthz", len(cfg.targets), port)

    with ThreadPoolExecutor(max_workers=len(cfg.targets)) as pool:
        while True:
            started = time.monotonic()
            # list() espera a que terminen todos y propaga cualquier excepción inesperada
            list(pool.map(lambda t: probe_target(t, cfg), cfg.targets))
            health.mark_round_done()
            time.sleep(max(0, cfg.interval_seconds - (time.monotonic() - started)))


if __name__ == "__main__":
    main()
