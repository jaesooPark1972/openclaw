# 📧 OpenClaw Gmail Integration Guide

## 1. Overview
This guide documents the successful integration of Gmail capabilities into the OpenClaw Telegram Bot. The agent can now read, summarize, and answer questions about the user's recent emails in real-time.

## 2. Prerequisites
The following environment variables must be present in `d:\OpenClaw\.env`:

```ini
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_GMAIL_REFRESH_TOKEN=...  # Critical for offline access
```

## 3. Authentication Infrastructure
To obtain the `GOOGLE_GMAIL_REFRESH_TOKEN`, we used a robust local OAuth flow:

1.  **Google Cloud Console**:
    *   Project: `greatparkjaesoo`
    *   **Authorized Redirect URI**: `http://localhost:8090/` (Exact match required)
2.  **Local Script**: `d:\OpenClaw\mcp_servers\final_auth.py` (or `interactive_oauth.py`)
    *   Runs a local server on port **8090**.
    *   Scopes requested:
        *   `https://www.googleapis.com/auth/gmail.readonly`
        *   `https://www.googleapis.com/auth/drive.readonly` (Bonus: Google Drive access)

## 4. Implementation Logic (`run_openclaw_telegram.py`)

The integration uses a **Prompt Injection** pattern rather than a traditional tool call, ensuring higher reliability with the Ollama model.

### 4.1 Keyword Interception
The bot listens for specific keywords in the user's message:
*   `mail`
*   `gmail`
*   `메일` (Korean)

### 4.2 Dynamic Context Injection
When keywords are detected:
1.  **Force Reload .env**: `load_dotenv(..., override=True)` ensures the latest token is used without restarting the bot.
2.  **Fetch Emails**: Uses `googleapiclient` to fetch the 3 most recent messages.
3.  **Injector**: Formats the emails into a string (Sender, Subject, Snippet).
4.  **System Prompt Override**:
    *   The prompt sent to the LLM is modified to include the email data.
    *   **Anti-Refusal Instruction**: Clearly instructs the LLM: *"Do NOT say you cannot check email. Answer based on the data provided."*

```python
# Code Snippet Logic
if "mail" in prompt:
    # ... fetch emails ...
    final_prompt = (
        f"[SYSTEM: Here are your emails...]\n{email_data}\n\n"
        f"User: {prompt}"
    )
```

## 5. Troubleshooting History

### Issue 1: `redirect_uri_mismatch`
*   **Cause**: Google Cloud Console had `localhost:8080`, but script used `8090` (or vice versa).
*   **Fix**: Standardized on port **8090** and ensured exact trailing slash match in Console.

### Issue 2: "I cannot check email" (LLM Refusal)
*   **Cause**: The model (Exaone/Llama) has safety training to refuse personal data access.
*   **Fix**: Strong system prompt engineering applied in the injection step to override this behavior.

### Issue 3: `[Gmail] Token missing` after auth
*   **Cause**: The Python process cached the old `.env` state (empty token) even after the file was updated.
*   **Fix**: Added `load_dotenv("d:/OpenClaw/.env", override=True)` inside the keyword handler to force a fresh read every time.

## 6. Future Expansion
The current token includes **Google Drive** scopes. To add Drive features:
1.  Add keywords: `drive`, `doc`, `파일`, `문서`.
2.  Use `googleapiclient.discovery.build('drive', 'v3', ...)` to file search/read.
3.  Inject file summaries into the context similarly to emails.
