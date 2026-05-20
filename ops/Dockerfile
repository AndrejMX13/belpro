FROM python:3.11-alpine

RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash \
    tzdata

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN addgroup -S ops && adduser -S -G ops ops

COPY scripts/ /app/scripts/
COPY entrypoint.sh /app/entrypoint.sh
COPY crontab /etc/crontabs/ops

RUN chmod +x /app/entrypoint.sh /app/scripts/*.sh /app/scripts/*.py \
 && chown -R ops:ops /app \
 && mkdir -p /backups && chown ops:ops /backups \
 && chown ops:ops /etc/crontabs/ops

USER ops
WORKDIR /app
CMD ["/app/entrypoint.sh"]
