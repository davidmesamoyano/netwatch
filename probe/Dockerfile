# ---------- Etapa 1: instalar dependencias ----------
FROM python:3.12-slim AS builder
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Etapa 2: imagen final, solo lo necesario ----------
FROM python:3.12-slim

# No ejecutar como root dentro del contenedor
RUN useradd --create-home --uid 10001 netwatch

# Copiamos de la etapa 1 solo las dependencias ya instaladas
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    NETWATCH_CONFIG=/app/config.yaml \
    NETWATCH_PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY netwatch/ netwatch/
COPY config.example.yaml config.yaml

USER netwatch
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)" || exit 1

CMD ["python", "-m", "netwatch.main"]
