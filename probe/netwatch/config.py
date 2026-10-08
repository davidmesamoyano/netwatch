"""Carga y valida la configuración de la sonda desde un fichero YAML."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml

VALID_KINDS = {"simulada", "real"}


@dataclass(frozen=True)
class Target:
    name: str
    host: str
    port: int
    kind: str  # "simulada" (sede con tc netem) o "real" (destino de Internet)


@dataclass(frozen=True)
class Config:
    interval_seconds: float = 15
    samples: int = 5
    timeout_seconds: float = 2
    targets: List[Target] = field(default_factory=list)


def load_config(path: str | Path) -> Config:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

    targets = []
    for raw in data.get("targets", []):
        kind = raw.get("kind", "real")
        if kind not in VALID_KINDS:
            raise ValueError(f"Destino {raw.get('name')}: kind debe ser uno de {VALID_KINDS}")
        targets.append(Target(name=raw["name"], host=raw["host"], port=int(raw.get("port", 80)), kind=kind))

    if not targets:
        raise ValueError("La configuración no tiene ningún destino en 'targets'")

    names = [t.name for t in targets]
    if len(names) != len(set(names)):
        raise ValueError("Hay destinos con el mismo nombre")

    cfg = Config(
        interval_seconds=float(data.get("interval_seconds", 15)),
        samples=int(data.get("samples", 5)),
        timeout_seconds=float(data.get("timeout_seconds", 2)),
        targets=targets,
    )
    if cfg.samples < 2:
        raise ValueError("samples debe ser al menos 2 para poder calcular el jitter")
    return cfg
