# NetWatch

Monitorización de calidad de red (latencia, jitter y pérdida de paquetes) sobre Kubernetes, con todo el ciclo DevOps: Docker, Ansible, Terraform, Helm, GitHub Actions, Jenkins, Prometheus y Grafana.

> 🚧 Proyecto en construcción. Estado actual: **semana 1** (sonda + Docker + Prometheus en local).

## Qué hace

Una sonda escrita en Python mide continuamente la calidad de red hacia varios destinos:

- **Sedes simuladas** (Valencia, Madrid y un enlace por satélite): contenedores nginx cuya red se degrada con `tc netem` para imitar enlaces reales.
- **Destinos reales** de Internet (DNS públicos de Cloudflare y Google).

Para cada destino calcula la latencia media, el jitter y la pérdida, y lo publica en formato Prometheus en `/metrics`.

| Sede | Latencia | Jitter | Pérdida |
|---|---|---|---|
| Valencia | 5 ms | 1 ms | 0 % |
| Madrid | 20 ms | 3 ms | 0 % |
| Satélite | 600 ms | 50 ms | 2 % |

## Arranque rápido (local)

Requisitos: Docker con Docker Compose.

```bash
docker compose -f deploy/compose/docker-compose.yml up --build
```

- Métricas de la sonda: http://localhost:8000/metrics
- Prometheus: http://localhost:9090 (prueba la consulta `netwatch_latency_ms`)

Demo de "caos": degrada en caliente el enlace de Madrid y mira cómo cambia la latencia.

```bash
./sites/degrade.sh netwatch-site-madrid-1 300ms 50ms 10%
```

## Métricas

| Métrica | Qué mide |
|---|---|
| `netwatch_latency_ms` | Latencia media de la última ronda |
| `netwatch_jitter_ms` | Variación media entre muestras consecutivas |
| `netwatch_packet_loss_ratio` | Proporción de muestras perdidas (0-1) |
| `netwatch_target_up` | 1 si el destino responde, 0 si está caído |
| `netwatch_rtt_seconds` | Histograma de cada muestra (para percentiles y SLO) |
| `netwatch_samples_total` | Muestras tomadas, por resultado (`ok` / `fail`) |

## Desarrollo

```bash
cd probe
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest          # tests
ruff check .    # estilo
```

## Decisiones técnicas

- **TCP en lugar de ICMP (ping):** medir el tiempo del handshake TCP no necesita permisos de root dentro del contenedor, y el retardo y la pérdida de `tc netem` le afectan igual.
- **Jitter:** media de la diferencia absoluta entre muestras consecutivas (versión simplificada de la idea de la RFC 3550).
- **Sedes con `tc netem`:** permite reproducir enlaces malos de forma controlada y repetible, y "romperlos" en directo para la demo.

## Hoja de ruta

- [x] Semana 1 – Sonda en Python, sedes simuladas, Docker, Docker Compose, Prometheus local y tests
- [ ] Semana 2 – Ansible (preparar la máquina), Terraform (clúster kind + Prometheus, Grafana y Jenkins), Helm chart propio
- [ ] Semana 3 – CI con GitHub Actions, CD con Jenkins, paneles de Grafana (red, SLO, pipelines), alertas en Telegram, demo y documentación
