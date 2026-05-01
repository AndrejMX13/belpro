"""Thin HTTP wrapper around Faster-Whisper for local speech-to-text.

Exposes a single endpoint:
  POST /transcribe   — body: raw audio bytes (ogg/mp3/wav)
                       response: plain-text transcript (UTF-8)

Configured via environment variables:
  WHISPER_MODEL     tiny | base | small | medium | large-v3  (default: medium)
  WHISPER_LANGUAGE  BCP-47 language code                      (default: sl)
"""
from __future__ import annotations

import os
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer

from faster_whisper import WhisperModel

MODEL_SIZE: str = os.environ.get("WHISPER_MODEL", "medium")
LANGUAGE: str = os.environ.get("WHISPER_LANGUAGE", "sl")
PORT: int = 8001

print(f"Loading Whisper model '{MODEL_SIZE}' …", flush=True)
_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("Model ready.", flush=True)


class _Handler(BaseHTTPRequestHandler):
    """Handle POST /transcribe requests."""

    def do_POST(self) -> None:  # noqa: N802
        """Transcribe the uploaded audio and return plain-text."""
        if self.path != "/transcribe":
            self._respond(404, b"Not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        audio = self.rfile.read(length)

        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp.write(audio)
            tmp_path = tmp.name

        try:
            segments, _ = _model.transcribe(tmp_path, language=LANGUAGE)
            transcript = " ".join(seg.text for seg in segments).strip()
        finally:
            os.unlink(tmp_path)

        self._respond(200, transcript.encode("utf-8"), "text/plain; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        """Health check — GET /health returns 200 ok."""
        if self.path == "/health":
            self._respond(200, b"ok")
        else:
            self._respond(404, b"Not found")

    def _respond(
        self,
        code: int,
        body: bytes,
        content_type: str = "text/plain",
    ) -> None:
        """Send a simple HTTP response."""
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:  # noqa: N802
        """Route access logs to stdout."""
        print(fmt % args, flush=True)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), _Handler)
    print(f"Whisper service listening on :{PORT}", flush=True)
    server.serve_forever()
