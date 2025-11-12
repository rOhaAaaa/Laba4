FROM grafana/k6:0.49.0
WORKDIR /app
COPY k6-script.js /app/k6-script.js
ENTRYPOINT ["k6","run","/app/k6-script.js"]
