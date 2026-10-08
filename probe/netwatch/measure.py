"""Medición de red: tiempo de establecimiento de una conexión TCP (handshake).

Usamos TCP en vez de ICMP (ping) porque no necesita permisos de root dentro del
contenedor, y el retardo/pérdida que añade tc netem afecta igual a TCP.
"""
import socket
import time
from typing import List, Optional


def tcp_rtt_ms(host: str, port: int, timeout: float) -> Optional[float]:
    """Devuelve el tiempo en ms que tarda en abrirse una conexión TCP, o None si falla."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except OSError:
        return None
    return (time.perf_counter() - start) * 1000


def take_samples(host: str, port: int, count: int, timeout: float, pause: float = 0.2) -> List[Optional[float]]:
    """Toma `count` muestras seguidas con una pequeña pausa entre ellas."""
    samples = []
    for i in range(count):
        samples.append(tcp_rtt_ms(host, port, timeout))
        if i < count - 1:
            time.sleep(pause)
    return samples
