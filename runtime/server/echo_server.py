from __future__ import annotations

import json
import os
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


RUNTIME_ROOT = Path(os.environ.get("ECHO_RUNTIME_ROOT", Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0, str(RUNTIME_ROOT))

from lib.dry_run_validator import DryRunValidationError, validate_dry_run  # noqa: E402


def _json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


class EchoRequestHandler(BaseHTTPRequestHandler):
    server_version = "EchoRuntime/0.1"

    def do_GET(self) -> None:
        route = urlparse(self.path).path.rstrip("/") or "/"

        if route == "/":
            self._send_json(
                HTTPStatus.OK,
                {
                    "service": "echo-personal-assistant",
                    "mode": "local-docker-dry-run",
                    "endpoints": ["/health", "/dry-run"],
                },
            )
            return

        if route == "/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "service": "echo-personal-assistant",
                    "runtime_root": str(RUNTIME_ROOT),
                },
            )
            return

        if route == "/dry-run":
            try:
                result = validate_dry_run(RUNTIME_ROOT)
            except DryRunValidationError as exc:
                self._send_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {
                        "status": "error",
                        "message": "DRY_RUN_FAILED",
                        "error": str(exc),
                    },
                )
                return

            self._send_json(HTTPStatus.OK, result)
            return

        self._send_json(
            HTTPStatus.NOT_FOUND,
            {
                "status": "error",
                "message": "Not found",
                "endpoints": ["/health", "/dry-run"],
            },
        )

    def log_message(self, format: str, *args) -> None:
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        body = _json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    host = os.environ.get("ECHO_HOST", "127.0.0.1")
    port = int(os.environ.get("ECHO_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), EchoRequestHandler)
    print(f"Echo runtime server listening on http://{host}:{port}")
    print(f"Runtime root: {RUNTIME_ROOT}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
