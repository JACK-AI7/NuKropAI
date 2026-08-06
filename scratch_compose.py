compose_addition = """
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\docker-compose.yml", "a", encoding="utf-8") as f:
    f.write(compose_addition)
