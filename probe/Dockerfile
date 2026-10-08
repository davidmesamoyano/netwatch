FROM python:3.12-slim

# No ejecutar como root dentro del contenedor (buena práctica de seguridad)
RUN useradd --create-home --uid 10001 netwatch
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY netwatch/ netwatch/
COPY config.example.yaml config.yaml

USER netwatch
ENV NETWATCH_CONFIG=/app/config.yaml NETWATCH_PORT=8000 PYTHONUNBUFFERED=1
EXPOSE 8000

# Docker comprueba cada 30 s que la sonda responde en /healthz (python-slim no trae curl)
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)" || exit 1
CMD ["python", "-m", "netwatch.main"]
