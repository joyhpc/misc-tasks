#!/usr/bin/env python3
"""Small Gmail readonly helper for this temporary workspace.

It uses a Desktop OAuth client secret already present on this machine, asks only
for gmail.readonly, and stores the resulting token outside my-daily.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
DEFAULT_CLIENT_SECRET = Path(
    "/home/ubuntu/dev-tools/client_secret_333150124202-j1a0bu98g78tmvb36jgmupv25vfbi8pe.apps.googleusercontent.com.json"
)
CONFIG_DIR = Path.home() / ".config" / "gmail-readonly"
TOKEN_PATH = CONFIG_DIR / "token.json"
PENDING_PATH = CONFIG_DIR / "pending_oauth.json"
REDIRECT_URI = "http://localhost:1"


def _chmod_private(path: Path) -> None:
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _load_credentials() -> Credentials:
    if not TOKEN_PATH.exists():
        raise SystemExit(f"NOT_AUTHENTICATED: run auth-url first; no token at {TOKEN_PATH}")

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())
        _chmod_private(TOKEN_PATH)

    if not creds.valid:
        raise SystemExit("TOKEN_INVALID: run auth-url again")
    return creds


def _gmail() -> Any:
    return build("gmail", "v1", credentials=_load_credentials(), cache_discovery=False)


def _auth_flow(client_secret: Path) -> Flow:
    return Flow.from_client_secrets_file(
        str(client_secret),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=True,
    )


def auth_url(args: argparse.Namespace) -> None:
    client_secret = Path(args.client_secret).expanduser().resolve()
    if not client_secret.exists():
        raise SystemExit(f"Client secret not found: {client_secret}")

    flow = _auth_flow(client_secret)
    url, state = flow.authorization_url(access_type="offline", prompt="consent")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_PATH.write_text(
        json.dumps(
            {
                "client_secret": str(client_secret),
                "state": state,
                "code_verifier": flow.code_verifier,
                "redirect_uri": REDIRECT_URI,
            },
            indent=2,
        )
    )
    _chmod_private(PENDING_PATH)
    print(url)


def _extract_code_and_state(value: str) -> tuple[str, str | None]:
    if not value.startswith("http"):
        return value, None
    parsed = urlparse(value)
    params = parse_qs(parsed.query)
    if "code" not in params:
        raise SystemExit("No code= parameter found in the pasted URL")
    return params["code"][0], params.get("state", [None])[0]


def auth_code(args: argparse.Namespace) -> None:
    if not PENDING_PATH.exists():
        raise SystemExit(f"No pending OAuth session at {PENDING_PATH}; run auth-url first")

    pending = json.loads(PENDING_PATH.read_text())
    code, returned_state = _extract_code_and_state(args.code_or_url.strip())
    if returned_state and returned_state != pending["state"]:
        raise SystemExit("OAuth state mismatch; run auth-url again")

    flow = Flow.from_client_secrets_file(
        pending["client_secret"],
        scopes=SCOPES,
        redirect_uri=pending["redirect_uri"],
        state=pending["state"],
        code_verifier=pending["code_verifier"],
    )
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    flow.fetch_token(code=code)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(flow.credentials.to_json())
    _chmod_private(TOKEN_PATH)
    PENDING_PATH.unlink(missing_ok=True)
    print(f"OK: Gmail readonly token saved to {TOKEN_PATH}")


def check(_: argparse.Namespace) -> None:
    svc = _gmail()
    profile = svc.users().getProfile(userId="me").execute()
    print(json.dumps({"emailAddress": profile.get("emailAddress"), "messagesTotal": profile.get("messagesTotal")}, ensure_ascii=False, indent=2))


def _headers(message: dict[str, Any]) -> dict[str, str]:
    headers = message.get("payload", {}).get("headers", [])
    return {h.get("name", "").lower(): h.get("value", "") for h in headers}


def search(args: argparse.Namespace) -> None:
    svc = _gmail()
    response = (
        svc.users()
        .messages()
        .list(userId="me", q=args.query, maxResults=args.max, includeSpamTrash=args.include_spam_trash)
        .execute()
    )
    rows = []
    for item in response.get("messages", []):
        msg = (
            svc.users()
            .messages()
            .get(
                userId="me",
                id=item["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Cc", "Date", "Subject"],
            )
            .execute()
        )
        headers = _headers(msg)
        rows.append(
            {
                "id": msg.get("id"),
                "threadId": msg.get("threadId"),
                "date": headers.get("date", ""),
                "from": headers.get("from", ""),
                "to": headers.get("to", ""),
                "subject": headers.get("subject", ""),
                "snippet": msg.get("snippet", ""),
            }
        )
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def _decode_body_part(part: dict[str, Any]) -> str:
    data = part.get("body", {}).get("data")
    if not data:
        return ""
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def _walk_parts(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    text_chunks: list[str] = []
    attachments: list[str] = []
    filename = payload.get("filename")
    if filename:
        attachments.append(filename)

    mime = payload.get("mimeType", "")
    if mime in {"text/plain", "text/html"}:
        decoded = _decode_body_part(payload)
        if decoded:
            text_chunks.append(decoded)

    for part in payload.get("parts", []) or []:
        child_text, child_attachments = _walk_parts(part)
        text_chunks.extend(child_text)
        attachments.extend(child_attachments)
    return text_chunks, attachments


def _iter_attachment_parts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    parts: list[dict[str, Any]] = []
    filename = payload.get("filename")
    attachment_id = payload.get("body", {}).get("attachmentId")
    if filename and attachment_id:
        parts.append(payload)
    for part in payload.get("parts", []) or []:
        parts.extend(_iter_attachment_parts(part))
    return parts


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w.\-()[\] @]+", "_", name.strip(), flags=re.UNICODE)
    return cleaned or "attachment"


def download_attachments(args: argparse.Namespace) -> None:
    svc = _gmail()
    msg = svc.users().messages().get(userId="me", id=args.message_id, format="full").execute()
    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for part in _iter_attachment_parts(msg.get("payload", {})):
        filename = part.get("filename", "")
        if args.pdf_only and not filename.lower().endswith(".pdf"):
            continue
        attachment_id = part.get("body", {}).get("attachmentId")
        data = (
            svc.users()
            .messages()
            .attachments()
            .get(userId="me", messageId=args.message_id, id=attachment_id)
            .execute()
            .get("data", "")
        )
        raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
        target = out_dir / _safe_filename(filename)
        if target.exists():
            stem = target.stem
            suffix = target.suffix
            target = out_dir / f"{stem}_{args.message_id}{suffix}"
        target.write_bytes(raw)
        saved.append(str(target))
    print(json.dumps(saved, ensure_ascii=False, indent=2))


def read(args: argparse.Namespace) -> None:
    svc = _gmail()
    msg = svc.users().messages().get(userId="me", id=args.message_id, format="full").execute()
    headers = _headers(msg)
    text_chunks, attachments = _walk_parts(msg.get("payload", {}))
    result = {
        "id": msg.get("id"),
        "threadId": msg.get("threadId"),
        "date": headers.get("date", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "subject": headers.get("subject", ""),
        "attachments": attachments,
        "body": "\n\n".join(text_chunks).strip(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Gmail readonly OAuth/search helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth-url", help="Print a Google OAuth URL")
    p.add_argument("--client-secret", default=str(DEFAULT_CLIENT_SECRET))
    p.set_defaults(func=auth_url)

    p = sub.add_parser("auth-code", help="Exchange a pasted code or localhost redirect URL")
    p.add_argument("code_or_url")
    p.set_defaults(func=auth_code)

    p = sub.add_parser("check", help="Verify Gmail readonly access")
    p.set_defaults(func=check)

    p = sub.add_parser("search", help="Search Gmail with Gmail query syntax")
    p.add_argument("query")
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--include-spam-trash", action="store_true")
    p.set_defaults(func=search)

    p = sub.add_parser("read", help="Read one message body by id")
    p.add_argument("message_id")
    p.set_defaults(func=read)

    p = sub.add_parser("download-attachments", help="Download message attachments")
    p.add_argument("message_id")
    p.add_argument("--output-dir", default="attachments")
    p.add_argument("--pdf-only", action="store_true")
    p.set_defaults(func=download_attachments)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
