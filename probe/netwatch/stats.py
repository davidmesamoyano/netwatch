"""Cálculo de latencia, jitter y pérdida a partir de una ronda de muestras.

Funciones puras (sin red ni estado): así se pueden probar fácilmente con pytest.
"""
from dataclasses import dataclass
from statistics import mean
from typing import Optional, Sequence


@dataclass(frozen=True)
class Summary:
    latency_ms: Optional[float]  # media de las muestras correctas; None si todas fallaron
    jitter_ms: Optional[float]   # variación media entre muestras consecutivas
    loss_ratio: float            # 0.0 = sin pérdida, 1.0 = todo perdido
    up: bool                     # True si al menos una muestra respondió


def summarize(samples_ms: Sequence[Optional[float]]) -> Summary:
    """Resume una ronda de muestras. Cada muestra es un RTT en ms o None si falló."""
    if not samples_ms:
        raise ValueError("Se necesita al menos una muestra")

    ok = [s for s in samples_ms if s is not None]
    loss = 1 - len(ok) / len(samples_ms)

    if not ok:
        return Summary(latency_ms=None, jitter_ms=None, loss_ratio=loss, up=False)

    # Jitter simplificado (idea de RFC 3550): media de |diferencia| entre muestras seguidas.
    diffs = [abs(b - a) for a, b in zip(ok, ok[1:])]
    jitter = mean(diffs) if diffs else 0.0

    return Summary(latency_ms=mean(ok), jitter_ms=jitter, loss_ratio=loss, up=True)
