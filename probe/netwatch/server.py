"""Servidor HTTP de la sonda.

- /metrics -> métricas para Prometheus
- /healthz -> "¿estás vivo?" para Docker y Kubernetes
"""
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


class Health:
    """Recuerda cuándo terminó la última ronda de mediciones.

    La sonda está sana si ha completado una ronda hace menos de `max_age_seconds`.
    Si el bucle de medición se queda colgado, /healthz empieza a responder 503
    y Kubernetes reinicia el contenedor.
    """

    def __init__(self, max_age_seconds: float):
        self.max_age_seconds = max_age_seconds
        self._last_round = time.monotonic()  # al arrancar le damos un margen
        self._lock = threading.Lock()

    def mark_round_done(self) -> None:
        with self._lock:
            self._last_round = time.monotonic()

    def is_healthy(self) -> bool:
        with self._lock:
            return time.monotonic() - self._last_round < self.max_age_seconds


def make_handler(health: Health):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/metrics":
                self._send(200, generate_latest(), CONTENT_TYPE_LATEST)
            elif path == "/healthz":
                if health.is_healthy():
                    self._send(200, b"ok\n")
                else:
                    self._send(503, b"la sonda no ha completado ninguna ronda reciente\n")
            else:
                self._send(404, b"no encontrado\n")

        def _send(self, status: int, body: bytes, content_type: str = "text/plain; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):  # no llenar el log con cada petición
            pass

    return Handler


def start_server(port: int, health: Health) -> ThreadingHTTPServer:
    """Arranca el servidor en un hilo aparte para no bloquear las mediciones."""
    server = ThreadingHTTPServer(("0.0.0.0", port), make_handler(health))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server
