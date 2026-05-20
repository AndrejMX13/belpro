FROM python:3.11-alpine

RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash \
    tzdata

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY scripts/ /app/scripts/
COPY entrypoint.sh /app/entrypoint.sh
COPY crontab /etc/crontabs/root

RUN chmod +x /app/entrypoint.sh /app/scripts/*.sh /app/scripts/*.py

WORKDIR /app
CMD ["/app/entrypoint.sh"]
