"""
OpenClaw Telegram REST API Bridge
- Telegram 메시지/음성 수신 → OpenClaw로 전달
- 모든 명령은 사용자 승인 후 실행
- 승인/거부 버튼 제공
"""

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import requests
import json
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
import uvicorn
import threading

# 환경 변수 로드
load_dotenv(r"D:\OpenClaw\.env")

# 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENCLAW_GATEWAY_URL = "ws://localhost:18789"
OPENCLAW_API_URL = "http://localhost:18789/api"
APPROVAL_TIMEOUT = 300  # 5분 타임아웃

# 승인 대기 중인 명령 저장소
pending_approvals: Dict[str, Dict[str, Any]] = {}

app = FastAPI(title="OpenClaw Telegram Bridge", version="2.0")


class CommandRequest(BaseModel):
    command: str
    source: str = "telegram"
    user_id: str
    chat_id: str
    message_id: Optional[str] = None


class ApprovalResponse(BaseModel):
    approval_id: str
    approved: bool
    reason: Optional[str] = None


# Telegram Bot 설정
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


async def send_approval_request(
    command: str, user_id: str, chat_id: str, approval_id: str
):
    """사용자에게 승인 요청 메시지 전송"""

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ 승인 (실행)", callback_data=f"approve:{approval_id}"
            ),
            InlineKeyboardButton(
                "❌ 거부 (취소)", callback_data=f"reject:{approval_id}"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"""
🔔 **실행 승인 요청**

**명령:**
```
{command}
```

**출처:** Telegram
**시간:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

이 명령을 실행할까요?
"""

    try:
        sent_message = await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )
        return sent_message.message_id
    except Exception as e:
        print(f"❌ 승인 요청 전송 실패: {e}")
        return None


async def execute_command(approval_id: str, command: str, chat_id: str):
    """승인된 명령 실행"""

    try:
        # OpenClaw Gateway에 명령 전송
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENCLAW_GATEWAY_TOKEN', '')}",
            "Content-Type": "application/json",
        }

        payload = {
            "method": "agent.run",
            "params": {
                "agentId": "main",
                "prompt": command,
                "tools": {
                    "exec": {
                        "host": "gateway",
                        "security": "full",
                        "ask": "on",  # 항상 승인 요청
                    }
                },
            },
        }

        # OpenClaw API 호출
        response = requests.post(
            f"{OPENCLAW_API_URL}/invoke", headers=headers, json=payload, timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            # 실행 결과 Telegram으로 전송
            result_message = f"""
✅ **명령 실행 완료**

**원본 명령:**
```
{command}
```

**실행 결과:**
```
{json.dumps(result, indent=2, ensure_ascii=False)[:1000]}
```
"""
            await bot.send_message(
                chat_id=chat_id, text=result_message, parse_mode="Markdown"
            )
        else:
            error_msg = f"""
❌ **명령 실행 실패**

**상태 코드:** {response.status_code}
**오류:** {response.text}
"""
            await bot.send_message(
                chat_id=chat_id, text=error_msg, parse_mode="Markdown"
            )

    except Exception as e:
        error_msg = f"""
❌ **실행 중 오류 발생**

**오류:** {str(e)}
"""
        await bot.send_message(chat_id=chat_id, text=error_msg, parse_mode="Markdown")
    finally:
        # 승인 목록에서 제거
        if approval_id in pending_approvals:
            del pending_approvals[approval_id]


@app.post("/api/command")
async def receive_command(request: CommandRequest, background_tasks: BackgroundTasks):
    """
    Telegram에서 받은 명령을 승인 대기열에 추가
    """
    approval_id = f"approval_{datetime.now().timestamp()}_{request.user_id}"

    # 승인 대기 목록에 저장
    pending_approvals[approval_id] = {
        "command": request.command,
        "user_id": request.user_id,
        "chat_id": request.chat_id,
        "message_id": request.message_id,
        "timestamp": datetime.now(),
        "status": "pending",
    }

    # 사용자에게 승인 요청
    message_id = await send_approval_request(
        command=request.command,
        user_id=request.user_id,
        chat_id=request.chat_id,
        approval_id=approval_id,
    )

    if message_id:
        pending_approvals[approval_id]["approval_message_id"] = message_id
        return JSONResponse(
            {
                "status": "approval_required",
                "approval_id": approval_id,
                "message": "사용자 승인을 기다리는 중...",
            }
        )
    else:
        return JSONResponse(
            {"status": "error", "message": "승인 요청 전송 실패"}, status_code=500
        )


@app.post("/api/approval")
async def process_approval(
    response: ApprovalResponse, background_tasks: BackgroundTasks
):
    """
    사용자의 승인/거부 응답 처리
    """
    approval_id = response.approval_id

    if approval_id not in pending_approvals:
        raise HTTPException(
            status_code=404, detail="승인 요청을 찾을 수 없거나 만료되었습니다"
        )

    approval_data = pending_approvals[approval_id]

    if response.approved:
        # 승인됨 - 명령 실행
        approval_data["status"] = "approved"
        background_tasks.add_task(
            execute_command,
            approval_id,
            approval_data["command"],
            approval_data["chat_id"],
        )

        return JSONResponse(
            {"status": "approved", "message": "명령이 승인되었습니다. 실행 중..."}
        )
    else:
        # 거부됨
        approval_data["status"] = "rejected"
        reason = response.reason or "사용자가 거부했습니다"

        await bot.send_message(
            chat_id=approval_data["chat_id"],
            text=f"❌ **명령이 거부되었습니다**\n\n사유: {reason}",
        )

        del pending_approvals[approval_id]

        return JSONResponse(
            {"status": "rejected", "message": f"명령이 거부되었습니다: {reason}"}
        )


@app.get("/api/pending")
async def list_pending_approvals():
    """
    대기 중인 승인 목록 조회
    """
    return JSONResponse(
        {
            "pending_count": len(pending_approvals),
            "approvals": [
                {
                    "approval_id": k,
                    "command": v["command"][:100] + "..."
                    if len(v["command"]) > 100
                    else v["command"],
                    "timestamp": v["timestamp"].isoformat(),
                    "status": v["status"],
                }
                for k, v in pending_approvals.items()
            ],
        }
    )


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return JSONResponse(
        {
            "status": "healthy",
            "pending_approvals": len(pending_approvals),
            "timestamp": datetime.now().isoformat(),
        }
    )


# Telegram Bot 핸들러
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start 명령 처리"""
    await update.message.reply_text(
        "🦞 **OpenClaw REST API Bridge**\n\n"
        "텔레그램으로 명령을 보내면 승인 후 실행됩니다.\n\n"
        "**사용법:**\n"
        "1. 원하는 명령을 텍스트로 보내세요\n"
        "2. 승인/거부 버튼이 나타납니다\n"
        "3. '✅ 승인'을 누르면 실행됩니다\n\n"
        "**예시 명령:**\n"
        "- '파일 목록 보여줘'\n"
        "- 'test.py 파일 만들어줘'\n"
        "- '음악 생성해줘'",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """텍스트 메시지 처리"""
    if not update.message or not update.message.text:
        return

    user_id = str(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    message_id = str(update.message.message_id)
    command_text = update.message.text

    # 명령을 REST API로 전송
    try:
        response = requests.post(
            "http://localhost:8081/api/command",
            json={
                "command": command_text,
                "source": "telegram",
                "user_id": user_id,
                "chat_id": chat_id,
                "message_id": message_id,
            },
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "approval_required":
                await update.message.reply_text(
                    "⏳ 승인 요청이 전송되었습니다. 버튼을 눌러주세요."
                )
        else:
            await update.message.reply_text(f"❌ 명령 처리 실패: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"❌ 오류 발생: {str(e)}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """승인/거부 버튼 콜백 처리"""
    query = update.callback_query
    await query.answer()

    data = query.data
    action, approval_id = data.split(":")

    if action == "approve":
        # 승인 처리
        try:
            response = requests.post(
                "http://localhost:8081/api/approval",
                json={"approval_id": approval_id, "approved": True},
                timeout=10,
            )

            if response.status_code == 200:
                await query.edit_message_text(
                    query.message.text + "\n\n✅ **승인됨 - 실행 중...**",
                    parse_mode="Markdown",
                    reply_markup=None,
                )
            else:
                await query.edit_message_text(
                    query.message.text + f"\n\n❌ **승인 처리 실패**: {response.text}",
                    parse_mode="Markdown",
                    reply_markup=None,
                )
        except Exception as e:
            await query.edit_message_text(
                query.message.text + f"\n\n❌ **오류**: {str(e)}",
                parse_mode="Markdown",
                reply_markup=None,
            )

    elif action == "reject":
        # 거부 처리
        try:
            response = requests.post(
                "http://localhost:8081/api/approval",
                json={
                    "approval_id": approval_id,
                    "approved": False,
                    "reason": "사용자가 거부했습니다",
                },
                timeout=10,
            )

            await query.edit_message_text(
                query.message.text + "\n\n❌ **거부됨**",
                parse_mode="Markdown",
                reply_markup=None,
            )
        except Exception as e:
            await query.edit_message_text(
                query.message.text + f"\n\n❌ **오류**: {str(e)}",
                parse_mode="Markdown",
                reply_markup=None,
            )


def run_telegram_bot():
    """Telegram Bot 실행"""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 핸들러 등록
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 Telegram Bot 시작...")
    application.run_polling()


if __name__ == "__main__":
    # 참고: Telegram Bot은 OpenClaw Gateway에서 이미 실행 중!
    # API Bridge는 REST API 서버만 실행
    print("🚀 REST API 서버 시작 (포트 8081)...")
    print("📝 참고: Telegram Bot은 OpenClaw Gateway에서 실행 중입니다")
    uvicorn.run(app, host="0.0.0.0", port=8081)
