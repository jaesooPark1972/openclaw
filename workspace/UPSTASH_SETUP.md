# 🚀 Upstash Vector Setup Guide

**Step 1: Get Your API Keys**
1.  Click here to open the console: [**Upstash Vector Console**](https://console.upstash.com/vector)
2.  Login with **GitHub** or **Google**.
3.  Click the **"Create Index"** button.
4.  **Name:** `antigravity-memory` (or any name you like).
5.  **Region:** Choose the one closest to you (e.g., `AWS - US-East-1` or `AP-Northeast` if available).
6.  **Dimensions:** Default (`1536` for OpenAI) is usually fine.
7.  Click **"Create"**.

**Step 2: Copy Credentials**
Once created, look for the **"Connect"** section or **"REST API"** tab.
You need two things:
*   **REST URL**: (begins with `https://...`)
*   **REST TOKEN**: (long string)

**Step 3: Update `.env` File**
Open `D:\OpenClaw\.env` and find these lines (around line 35):
(Or just paste your new keys over the old ones)

```ini
# ================ CONTEXT7 (UPSTASH) ================
UPSTASH_VECTOR_REST_URL=https://your-new-url.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-new-token-here...
```

**Step 4: Verification**
After updating, tell me **"설정 완료"** or **"Restart"**, and I will verify the connection for you.
