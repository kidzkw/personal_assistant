FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ECHO_HOST=0.0.0.0
ENV ECHO_PORT=8080

WORKDIR /app

RUN useradd --create-home --uid 10001 echo

COPY README.md README.en.md README.zh-CN.md ./
COPY runtime ./runtime

USER echo

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()"

CMD ["python", "runtime/server/echo_server.py"]
