import urllib.error
import urllib.request

import netwatch.metrics  # noqa: F401  (registra las métricas de NetWatch)
from netwatch.server import Health, start_server


def get(port, path):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=2) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def test_healthz_sana():
    server = start_server(0, Health(max_age_seconds=60))
    port = server.server_address[1]
    assert get(port, "/healthz") == (200, "ok\n")
    server.shutdown()


def test_healthz_caida_si_no_hay_rondas_recientes():
    server = start_server(0, Health(max_age_seconds=0))
    port = server.server_address[1]
    status, _ = get(port, "/healthz")
    assert status == 503
    server.shutdown()


def test_metrics_y_404():
    server = start_server(0, Health(max_age_seconds=60))
    port = server.server_address[1]
    status, body = get(port, "/metrics")
    assert status == 200 and "netwatch_latency_ms" in body
    assert get(port, "/otra")[0] == 404
    server.shutdown()
