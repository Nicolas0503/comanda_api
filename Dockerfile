FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src ./src

WORKDIR /app/src

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8443/tcp 8443/udp

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8443", "--quic-bind", "0.0.0.0:8443", "--certfile", "/certs/tls.crt", "--keyfile", "/certs/tls.key", "--access-logfile", "-", "--error-logfile", "-"]