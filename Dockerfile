FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl tini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1 FLASK_ENV=production

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=6 \
  CMD curl -fsS http://127.0.0.1:8080/ || exit 1

ENTRYPOINT ["/usr/bin/tini","--"]

CMD ["gunicorn","app:app","-b","0.0.0.0:8080","--workers","4","--threads","2","--timeout","180","--keep-alive","5"]
