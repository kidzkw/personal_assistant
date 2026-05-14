from __future__ import annotations

import json
import os
import base64
import re
import sys
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone


RUNTIME_ROOT = Path(os.environ.get("ECHO_RUNTIME_ROOT", Path(__file__).resolve().parents[1])).resolve()
INBOX_TEXT_ROOT = RUNTIME_ROOT / "inbox" / "text"
INBOX_FILE_ROOT = RUNTIME_ROOT / "inbox" / "files"
sys.path.insert(0, str(RUNTIME_ROOT))

from lib.dry_run_validator import DryRunValidationError, validate_dry_run  # noqa: E402


def _json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _make_inbox_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"inbox_text_{stamp}_{uuid.uuid4().hex[:8]}"


def _make_file_inbox_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"inbox_file_{stamp}_{uuid.uuid4().hex[:8]}"


def _safe_filename(filename: str) -> str:
    name = Path(filename or "pasted-file").name.strip()
    name = re.sub(r"[^A-Za-z0-9._ -]+", "_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:120] or "pasted-file"


def _write_text_inbox_item(payload: dict) -> dict:
    text = str(payload.get("text", "")).strip()
    if not text:
        raise ValueError("text is required")
    if len(text) > 20000:
        raise ValueError("text is too long; keep one inbox item under 20000 characters")

    sensitivity = str(payload.get("sensitivity", "personal")).strip() or "personal"
    source_type = str(payload.get("source_type", "manual_note")).strip() or "manual_note"
    title = str(payload.get("title", "")).strip()

    inbox_id = _make_inbox_id()
    item = {
        "inbox_item": {
            "inbox_id": inbox_id,
            "created_at": _now_iso(),
            "source_type": source_type,
            "input_type": "text",
            "title": title or None,
            "text": text,
            "sensitivity": sensitivity,
            "sync_permission": "local_only",
            "review_state": "inbox",
            "processing_state": "not_processed",
            "note": "Local-only inbox item. This is not confirmed memory.",
        }
    }

    INBOX_TEXT_ROOT.mkdir(parents=True, exist_ok=True)
    path = INBOX_TEXT_ROOT / f"{inbox_id}.json"
    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "ok",
        "message": "INBOX_ITEM_CREATED",
        "inbox_id": inbox_id,
        "path": str(path.relative_to(RUNTIME_ROOT)),
        "review_state": "inbox",
        "processing_state": "not_processed",
    }


def _write_file_inbox_item(payload: dict) -> dict:
    filename = _safe_filename(str(payload.get("filename", "pasted-file")))
    content_type = str(payload.get("content_type", "application/octet-stream")).strip() or "application/octet-stream"
    encoded = str(payload.get("data_base64", "")).strip()
    if not encoded:
        raise ValueError("data_base64 is required")

    try:
        data = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError("data_base64 is not valid base64") from exc

    if not data:
        raise ValueError("file is empty")
    if len(data) > 10 * 1024 * 1024:
        raise ValueError("file is too large; keep one inbox file under 10 MB")

    sensitivity = str(payload.get("sensitivity", "personal")).strip() or "personal"
    source_type = str(payload.get("source_type", "file_drop")).strip() or "file_drop"
    title = str(payload.get("title", "")).strip()

    inbox_id = _make_file_inbox_id()
    item_root = INBOX_FILE_ROOT / inbox_id
    item_root.mkdir(parents=True, exist_ok=False)
    file_path = item_root / filename
    file_path.write_bytes(data)

    meta = {
        "inbox_item": {
            "inbox_id": inbox_id,
            "created_at": _now_iso(),
            "source_type": source_type,
            "input_type": "file",
            "title": title or None,
            "original_filename": filename,
            "stored_filename": filename,
            "content_type": content_type,
            "size_bytes": len(data),
            "file_ref": str(file_path.relative_to(RUNTIME_ROOT)),
            "sensitivity": sensitivity,
            "sync_permission": "local_only",
            "review_state": "inbox",
            "processing_state": "not_processed",
            "note": "Local-only inbox file. This is not confirmed memory.",
        }
    }
    meta_path = item_root / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "status": "ok",
        "message": "INBOX_FILE_CREATED",
        "inbox_id": inbox_id,
        "path": str(meta_path.relative_to(RUNTIME_ROOT)),
        "file_ref": str(file_path.relative_to(RUNTIME_ROOT)),
        "content_type": content_type,
        "size_bytes": len(data),
        "review_state": "inbox",
        "processing_state": "not_processed",
    }


def _list_inbox_items(limit: int = 50) -> dict:
    items = []

    if INBOX_TEXT_ROOT.exists():
        for path in INBOX_TEXT_ROOT.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
                item = data.get("inbox_item", {})
                items.append(
                    {
                        "inbox_id": item.get("inbox_id"),
                        "created_at": item.get("created_at"),
                        "input_type": item.get("input_type"),
                        "title": item.get("title"),
                        "source_type": item.get("source_type"),
                        "sensitivity": item.get("sensitivity"),
                        "review_state": item.get("review_state"),
                        "processing_state": item.get("processing_state"),
                        "preview": str(item.get("text", ""))[:160],
                        "path": str(path.relative_to(RUNTIME_ROOT)),
                    }
                )
            except (OSError, json.JSONDecodeError) as exc:
                items.append({"path": str(path.relative_to(RUNTIME_ROOT)), "error": str(exc)})

    if INBOX_FILE_ROOT.exists():
        for path in INBOX_FILE_ROOT.glob("*/meta.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
                item = data.get("inbox_item", {})
                items.append(
                    {
                        "inbox_id": item.get("inbox_id"),
                        "created_at": item.get("created_at"),
                        "input_type": item.get("input_type"),
                        "title": item.get("title"),
                        "source_type": item.get("source_type"),
                        "sensitivity": item.get("sensitivity"),
                        "review_state": item.get("review_state"),
                        "processing_state": item.get("processing_state"),
                        "preview": item.get("original_filename"),
                        "content_type": item.get("content_type"),
                        "size_bytes": item.get("size_bytes"),
                        "file_ref": item.get("file_ref"),
                        "path": str(path.relative_to(RUNTIME_ROOT)),
                    }
                )
            except (OSError, json.JSONDecodeError) as exc:
                items.append({"path": str(path.relative_to(RUNTIME_ROOT)), "error": str(exc)})

    items.sort(key=lambda item: str(item.get("created_at", "")), reverse=True)
    return {"status": "ok", "items": items[:limit]}


def _home_html() -> bytes:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Echo Runtime</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f4;
      --surface: #ffffff;
      --surface-2: #eef2ec;
      --text: #20231f;
      --muted: #626960;
      --border: #d9dfd5;
      --accent: #1f7a5c;
      --accent-2: #8a5d13;
      --danger: #9b2c2c;
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      line-height: 1.45;
    }

    main {
      width: min(1080px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 48px;
    }

    header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 24px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }

    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
      font-weight: 720;
    }

    .lead {
      max-width: 680px;
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 16px;
    }

    .status-pill {
      min-width: 136px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      padding: 10px 12px;
      font-size: 13px;
      color: var(--muted);
      text-align: right;
    }

    .status-pill strong {
      display: block;
      color: var(--accent);
      font-size: 15px;
      margin-bottom: 2px;
    }

    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 24px;
    }

    section {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      padding: 18px;
    }

    h2 {
      margin: 0 0 12px;
      font-size: 17px;
      line-height: 1.25;
      letter-spacing: 0;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 14px 0 0;
    }

    label {
      display: block;
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 650;
    }

    input, select, textarea {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #ffffff;
      color: var(--text);
      font: 14px/1.45 var(--sans);
      padding: 9px 10px;
    }

    textarea {
      min-height: 112px;
      resize: vertical;
    }

    .dropbox {
      display: grid;
      place-items: center;
      min-height: 190px;
      margin-top: 12px;
      border: 1.5px dashed #aab5a5;
      border-radius: 8px;
      background: #f9faf7;
      padding: 22px;
      text-align: center;
      transition: border-color 140ms ease, background 140ms ease;
    }

    .dropbox.dragging {
      border-color: var(--accent);
      background: #edf8f2;
    }

    .dropbox strong {
      display: block;
      font-size: 18px;
      margin-bottom: 8px;
    }

    .dropbox p {
      max-width: 560px;
      margin: 0 auto;
      color: var(--muted);
      font-size: 14px;
    }

    .file-list {
      display: grid;
      gap: 8px;
      margin: 12px 0 0;
    }

    .file-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 9px 10px;
      background: #ffffff;
      font-size: 13px;
    }

    .file-row span:first-child {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .field-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }

    button, a.button {
      appearance: none;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface-2);
      color: var(--text);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 38px;
      padding: 8px 12px;
      font: 650 14px/1 var(--sans);
      text-decoration: none;
    }

    button.primary {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
    }

    button:hover, a.button:hover {
      border-color: #aab5a5;
    }

    pre {
      min-height: 180px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #101510;
      color: #e8f1e8;
      padding: 14px;
      margin: 12px 0 0;
      font: 13px/1.5 var(--mono);
      white-space: pre-wrap;
      word-break: break-word;
    }

    dl {
      display: grid;
      grid-template-columns: 150px 1fr;
      gap: 8px 12px;
      margin: 0;
      font-size: 14px;
    }

    dt { color: var(--muted); }
    dd { margin: 0; font-family: var(--mono); }

    .wide { grid-column: 1 / -1; }
    .ok { color: var(--accent); }
    .warn { color: var(--accent-2); }
    .error { color: var(--danger); }

    @media (max-width: 760px) {
      main { width: min(100% - 24px, 1080px); padding-top: 20px; }
      header { display: block; }
      h1 { font-size: 28px; }
      .status-pill { margin-top: 16px; text-align: left; }
      .grid { grid-template-columns: 1fr; }
      dl { grid-template-columns: 1fr; }
      .field-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Echo Runtime</h1>
        <p class="lead">Local Docker dry-run server for the personal memory workflow. Use this screen to check the service and validate the fake evidence packet chain.</p>
      </div>
      <div class="status-pill">
        <strong id="service-status">Checking</strong>
        localhost:8080
      </div>
    </header>

    <div class="grid">
      <section>
        <h2>Service</h2>
        <dl>
          <dt>Service</dt>
          <dd>echo-personal-assistant</dd>
          <dt>Mode</dt>
          <dd>local-docker-dry-run</dd>
          <dt>Runtime</dt>
          <dd id="runtime-root">unknown</dd>
        </dl>
        <div class="actions">
          <button type="button" onclick="loadHealth()">Check Health</button>
          <a class="button" href="/health">Open JSON</a>
        </div>
      </section>

      <section>
        <h2>Dry Run</h2>
        <dl>
          <dt>Packet</dt>
          <dd id="packet-id">not loaded</dd>
          <dt>Candidate</dt>
          <dd id="candidate-id">not loaded</dd>
          <dt>Next Spawn</dt>
          <dd id="next-spawn">not loaded</dd>
        </dl>
        <div class="actions">
          <button class="primary" type="button" onclick="runDryRun()">Run Dry Run</button>
          <a class="button" href="/dry-run">Open JSON</a>
        </div>
      </section>

      <section class="wide">
        <h2>Inbox Dropbox</h2>
        <label for="inbox-title">Title</label>
        <input id="inbox-title" type="text" placeholder="Optional short title">
        <div class="field-row">
          <div>
            <label for="source-type">Source</label>
            <select id="source-type">
              <option value="manual_note">manual_note</option>
              <option value="local_text">local_text</option>
              <option value="email_note">email_note</option>
              <option value="chat_note">chat_note</option>
            </select>
          </div>
          <div>
            <label for="sensitivity">Sensitivity</label>
            <select id="sensitivity">
              <option value="personal">personal</option>
              <option value="financial">financial</option>
              <option value="medical">medical</option>
              <option value="relationship">relationship</option>
              <option value="account_security">account_security</option>
            </select>
          </div>
        </div>
        <div id="dropbox" class="dropbox" tabindex="0">
          <div>
            <strong>Drop, paste, or choose a file</strong>
            <p>Use this for screenshots, photos, PDFs, or a small text note. Everything lands in local inbox review, not confirmed memory.</p>
            <div class="actions" style="justify-content: center;">
              <button class="primary" type="button" onclick="document.getElementById('file-input').click()">Choose File</button>
              <button type="button" onclick="sendTypedText()">Send Typed Text</button>
            </div>
          </div>
        </div>
        <input id="file-input" type="file" multiple style="display: none;">
        <div id="file-list" class="file-list"></div>
        <div style="margin-top: 12px;">
          <label for="inbox-text">Optional typed text</label>
          <textarea id="inbox-text" placeholder="You can still type or paste text here, then click Send Typed Text."></textarea>
        </div>
        <div class="actions">
          <button type="button" onclick="loadInbox()">Refresh Inbox</button>
          <a class="button" href="/inbox">Open Inbox JSON</a>
        </div>
      </section>

      <section class="wide">
        <h2>Response</h2>
        <pre id="output">Loading...</pre>
      </section>
    </div>
  </main>

  <script>
    const output = document.getElementById("output");
    const statusEl = document.getElementById("service-status");
    const dropbox = document.getElementById("dropbox");
    const fileInput = document.getElementById("file-input");
    const fileList = document.getElementById("file-list");

    function show(data) {
      output.textContent = JSON.stringify(data, null, 2);
      if (data.runtime_root) document.getElementById("runtime-root").textContent = data.runtime_root;
      if (data.packet_id) document.getElementById("packet-id").textContent = data.packet_id;
      if (data.candidate_id) document.getElementById("candidate-id").textContent = data.candidate_id;
      if (Object.prototype.hasOwnProperty.call(data, "next_spawn_allowed")) {
        document.getElementById("next-spawn").textContent = String(data.next_spawn_allowed);
      }
    }

    async function requestJson(path) {
      const response = await fetch(path, { cache: "no-store" });
      const data = await response.json();
      show(data);
      if (!response.ok) throw new Error(data.error || data.message || response.statusText);
      return data;
    }

    async function loadHealth() {
      try {
        statusEl.textContent = "Checking";
        statusEl.className = "";
        const data = await requestJson("/health");
        statusEl.textContent = data.status === "ok" ? "Healthy" : "Check failed";
        statusEl.className = data.status === "ok" ? "ok" : "error";
      } catch (error) {
        statusEl.textContent = "Offline";
        statusEl.className = "error";
        output.textContent = String(error);
      }
    }

    async function runDryRun() {
      try {
        const data = await requestJson("/dry-run");
        statusEl.textContent = data.status === "ok" ? "Dry Run OK" : "Check failed";
        statusEl.className = data.status === "ok" ? "ok" : "error";
      } catch (error) {
        statusEl.textContent = "Dry Run Failed";
        statusEl.className = "error";
        output.textContent = String(error);
      }
    }

    function commonInboxPayload() {
      return {
        title: document.getElementById("inbox-title").value,
        source_type: document.getElementById("source-type").value,
        sensitivity: document.getElementById("sensitivity").value
      };
    }

    async function sendInboxText(text) {
      const payload = {
        ...commonInboxPayload(),
        text
      };
      try {
        const response = await fetch("/inbox/text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        show(data);
        if (!response.ok) throw new Error(data.error || data.message || response.statusText);
        document.getElementById("inbox-text").value = "";
        statusEl.textContent = "Inbox Saved";
        statusEl.className = "ok";
      } catch (error) {
        statusEl.textContent = "Inbox Failed";
        statusEl.className = "error";
        output.textContent = String(error);
      }
    }

    async function sendTypedText() {
      await sendInboxText(document.getElementById("inbox-text").value);
    }

    function fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          const result = String(reader.result || "");
          resolve(result.includes(",") ? result.split(",")[1] : result);
        };
        reader.onerror = () => reject(reader.error || new Error("File read failed"));
        reader.readAsDataURL(file);
      });
    }

    function formatBytes(bytes) {
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
    }

    function addFileRow(file, state) {
      const row = document.createElement("div");
      row.className = "file-row";
      row.innerHTML = `<span>${file.name || "pasted-file"}</span><span>${state} · ${formatBytes(file.size || 0)}</span>`;
      fileList.prepend(row);
    }

    async function sendFiles(files) {
      for (const file of files) {
        try {
          if (file.size > 10 * 1024 * 1024) {
            addFileRow(file, "too large");
            continue;
          }
          const payload = {
            ...commonInboxPayload(),
            filename: file.name || `pasted-${Date.now()}`,
            content_type: file.type || "application/octet-stream",
            data_base64: await fileToBase64(file)
          };
          const response = await fetch("/inbox/file", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          const data = await response.json();
          show(data);
          if (!response.ok) throw new Error(data.error || data.message || response.statusText);
          addFileRow(file, "saved");
          statusEl.textContent = "Inbox Saved";
          statusEl.className = "ok";
        } catch (error) {
          addFileRow(file, "failed");
          statusEl.textContent = "Inbox Failed";
          statusEl.className = "error";
          output.textContent = String(error);
        }
      }
    }

    async function loadInbox() {
      try {
        const data = await requestJson("/inbox");
        statusEl.textContent = "Inbox Loaded";
        statusEl.className = "ok";
      } catch (error) {
        statusEl.textContent = "Inbox Failed";
        statusEl.className = "error";
        output.textContent = String(error);
      }
    }

    ["dragenter", "dragover"].forEach((eventName) => {
      dropbox.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropbox.classList.add("dragging");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropbox.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropbox.classList.remove("dragging");
      });
    });

    dropbox.addEventListener("drop", (event) => {
      const files = Array.from(event.dataTransfer.files || []);
      if (files.length) sendFiles(files);
    });

    fileInput.addEventListener("change", () => {
      const files = Array.from(fileInput.files || []);
      if (files.length) sendFiles(files);
      fileInput.value = "";
    });

    window.addEventListener("paste", (event) => {
      const files = Array.from(event.clipboardData.files || []);
      if (files.length) {
        sendFiles(files);
        return;
      }
      const text = event.clipboardData.getData("text/plain");
      if (text && document.activeElement === dropbox) {
        sendInboxText(text);
      }
    });

    loadHealth();
  </script>
</body>
</html>
""".encode("utf-8")


class EchoRequestHandler(BaseHTTPRequestHandler):
    server_version = "EchoRuntime/0.1"

    def do_POST(self) -> None:
        route = urlparse(self.path).path.rstrip("/") or "/"

        if route == "/inbox/text":
            try:
                payload = self._read_json_body(max_bytes=25000)
                result = _write_text_inbox_item(payload)
            except ValueError as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"status": "error", "message": "INVALID_INBOX_ITEM", "error": str(exc)})
                return
            except OSError as exc:
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"status": "error", "message": "INBOX_WRITE_FAILED", "error": str(exc)})
                return

            self._send_json(HTTPStatus.CREATED, result)
            return

        if route == "/inbox/file":
            try:
                payload = self._read_json_body(max_bytes=14 * 1024 * 1024)
                result = _write_file_inbox_item(payload)
            except ValueError as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"status": "error", "message": "INVALID_INBOX_FILE", "error": str(exc)})
                return
            except OSError as exc:
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"status": "error", "message": "INBOX_WRITE_FAILED", "error": str(exc)})
                return

            self._send_json(HTTPStatus.CREATED, result)
            return

        self._send_json(
            HTTPStatus.NOT_FOUND,
            {
                "status": "error",
                "message": "Not found",
                "endpoints": ["/", "/api", "/health", "/dry-run", "/inbox", "POST /inbox/text", "POST /inbox/file"],
            },
        )

    def do_GET(self) -> None:
        route = urlparse(self.path).path.rstrip("/") or "/"

        if route == "/":
            self._send_html(HTTPStatus.OK, _home_html())
            return

        if route == "/api":
            self._send_json(
                HTTPStatus.OK,
                {
                    "service": "echo-personal-assistant",
                    "mode": "local-docker-dry-run",
                    "endpoints": ["/", "/health", "/dry-run", "/inbox", "POST /inbox/text", "POST /inbox/file"],
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

        if route == "/inbox":
            self._send_json(HTTPStatus.OK, _list_inbox_items())
            return

        self._send_json(
            HTTPStatus.NOT_FOUND,
            {
                "status": "error",
                "message": "Not found",
                "endpoints": ["/", "/api", "/health", "/dry-run", "/inbox", "POST /inbox/text", "POST /inbox/file"],
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

    def _read_json_body(self, max_bytes: int) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            raise ValueError("request body is required")
        if length > max_bytes:
            raise ValueError(f"request body is too large; max {max_bytes} bytes")
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload

    def _send_html(self, status: HTTPStatus, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
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
