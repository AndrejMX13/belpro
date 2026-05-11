FROM python:3.11-slim@sha256:a5b427ace4900267d93db34138e512325c6fa6af84ad5e4ed5f3b36258cc4142
# python:3.11-slim as of 2026-05-09

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    wget \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    faster-whisper==1.1.1 \
    requests==2.32.3

COPY transcribe.py .

RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 8001
CMD ["python", "transcribe.py"]
