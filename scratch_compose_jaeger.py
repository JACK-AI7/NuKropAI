compose_addition = """
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # Web UI
      - "4318:4318"   # OTLP HTTP receiver
    environment:
      - COLLECTOR_OTLP_ENABLED=true
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\docker-compose.yml", "a", encoding="utf-8") as f:
    f.write(compose_addition)
