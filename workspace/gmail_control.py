import base64
import os
from email.mime.text import MIMEText
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mcp.server.fastmcp import FastMCP

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]

mcp = FastMCP("gmail-control")

TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", r"F:\AGen\keys\gmail_token.json")
SETUP_HINT = os.getenv("GMAIL_SETUP_HINT", r"python f:\AGen\scripts\setup_gmail.py")


def _decode_body_data(data: str | None) -> str:
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    except Exception:
        return ""


def _extract_text_body(payload: dict[str, Any]) -> str:
    mime_type = payload.get("mimeType", "")
    if mime_type == "text/plain":
        return _decode_body_data(payload.get("body", {}).get("data"))

    for part in payload.get("parts", []) or []:
        text = _extract_text_body(part)
        if text:
            return text

    return _decode_body_data(payload.get("body", {}).get("data"))


def _get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())
        else:
            raise RuntimeError(
                f"Gmail token not ready. Run setup first: {SETUP_HINT}"
            )

    return build("gmail", "v1", credentials=creds)


@mcp.tool()
def health_gmail() -> str:
    """Check whether Gmail API is reachable with current token."""
    try:
        service = _get_service()
        profile = service.users().getProfile(userId="me").execute()
        email = profile.get("emailAddress", "unknown")
        total = profile.get("messagesTotal", "?")
        return f"OK | account={email} | messagesTotal={total}"
    except Exception as exc:
        return f"ERROR | {exc}"


@mcp.tool()
def list_emails(query: str = "is:unread", max_results: int = 10) -> str:
    """List recent emails with id, from, subject, and date."""
    try:
        service = _get_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return "No emails found."

        lines = []
        for msg in messages:
            full = (
                service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"])
                .execute()
            )
            headers = {h["name"]: h.get("value", "") for h in full.get("payload", {}).get("headers", [])}
            lines.append(
                " | ".join(
                    [
                        f"ID={msg['id']}",
                        f"From={headers.get('From', '(Unknown)')}",
                        f"Subject={headers.get('Subject', '(No Subject)')}",
                        f"Date={headers.get('Date', '(No Date)')}",
                    ]
                )
            )

        return "\n".join(lines)
    except HttpError as exc:
        return f"Error listing emails: {exc}"
    except Exception as exc:
        return f"Error listing emails: {exc}"


@mcp.tool()
def read_email(message_id: str) -> str:
    """Read one email by message ID."""
    try:
        service = _get_service()
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )

        payload = msg.get("payload", {})
        headers = {h["name"]: h.get("value", "") for h in payload.get("headers", [])}
        snippet = msg.get("snippet", "")
        body = _extract_text_body(payload)

        if not body:
            body = f"(snippet) {snippet}"

        return (
            f"Subject: {headers.get('Subject', '(No Subject)')}\n"
            f"From: {headers.get('From', '(Unknown)')}\n"
            f"Date: {headers.get('Date', '(No Date)')}\n"
            f"\n{body}"
        )
    except HttpError as exc:
        return f"Error reading email: {exc}"
    except Exception as exc:
        return f"Error reading email: {exc}"


@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send email."""
    try:
        service = _get_service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        sent = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        return f"Email sent. id={sent.get('id', 'unknown')}"
    except HttpError as exc:
        return f"Error sending email: {exc}"
    except Exception as exc:
        return f"Error sending email: {exc}"


@mcp.tool()
def create_draft(to: str, subject: str, body: str) -> str:
    """Create draft email."""
    try:
        service = _get_service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": raw_message}})
            .execute()
        )
        return f"Draft created. id={draft.get('id', 'unknown')}"
    except HttpError as exc:
        return f"Error creating draft: {exc}"
    except Exception as exc:
        return f"Error creating draft: {exc}"


if __name__ == "__main__":
    mcp.run()
