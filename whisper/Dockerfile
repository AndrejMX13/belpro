FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    faster-whisper==1.1.1 \
    requests==2.32.3

COPY transcribe.py .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8001
CMD ["python", "transcribe.py"]
