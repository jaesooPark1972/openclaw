import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from pykis import PyKis, KisQuote, KisAccountNumber
from datetime import datetime

# Load Environment from Master .env
def load_env():
    env_path = Path(r"D:\OpenClaw\.env")
    kv = {}
    if env_path.exists():
        content = env_path.read_text(encoding='utf-8', errors='ignore')
        for line in content.splitlines():
            line = line.strip()
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                k_clean = k.strip()
                v_clean = v.strip().strip("'").strip('"')
                kv[k_clean] = v_clean
    return kv

ENV = load_env()

class StockTradingAgent:
    def __init__(self):
        self.kis = None
        self._init_client()

    def _init_client(self):
        app_key = ENV.get("KIS_APP_KEY")
        app_secret = ENV.get("KIS_APP_SECRET")
        account_str = ENV.get("KIS_ACCOUNT")
        virtual = ENV.get("KIS_VIRTUAL_MODE", "true").lower() == "true"
        
        # In python-kis 2.1.6, ID is HTS ID. If not found, use a placeholder or ask user.
        user_id = ENV.get("KIS_USER_ID") or "wowpark" # Try common ID or placeholder

        if not all([app_key, app_secret, account_str]):
            print("ERROR: KIS credentials (KEY, SECRET, ACCOUNT) are missing in .env")
            return

        try:
            # Handle account string (e.g., 50169425-01 or 5016942501)
            # KIS requires 8 digit + 2 digit
            clean_acc = account_str.replace("-", "")
            if len(clean_acc) == 8:
                # Default to 01 if suffix is missing
                clean_acc += "01"
            
            if virtual:
                self.kis = PyKis(
                    id=user_id,
                    account=clean_acc,
                    appkey=app_key,
                    secretkey=app_secret,
                    virtual_id=user_id,
                    virtual_appkey=app_key,
                    virtual_secretkey=app_secret
                )
            else:
                self.kis = PyKis(
                    id=user_id,
                    account=clean_acc,
                    appkey=app_key,
                    secretkey=app_secret
                )
            # print(f"KIS Client Initialized (Virtual: {virtual}, Account: {clean_acc})")
        except Exception as e:
            print(f"ERROR: Failed to init KIS client - {e}")

    def get_balance(self) -> str:
        if not self.kis: return "KIS client not initialized."
        try:
            # In 2.1.6, account().balance() returns KisBalance
            balance = self.kis.account().balance()
            res = {
                "deposit": int(balance.deposit or 0),
                "withdrawable": int(balance.withdrawable_amount or 0),
                "purchase_amount": int(balance.purchase_amount or 0),
                "total_evaluation": int(balance.total or 0),
                "profit": int(balance.profit or 0),
                "profit_rate": float(balance.profit_rate or 0.0)
            }
            return json.dumps(res, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Error fetching balance: {e}"

    def get_price(self, code: str) -> str:
        if not self.kis: return "KIS client not initialized."
        try:
            stock = self.kis.stock(code)
            quote = stock.quote()
            res = {
                "code": code,
                "name": quote.name or code,
                "price": int(quote.price),
                "change": int(quote.change),
                "rate": float(quote.change_rate) if hasattr(quote, 'change_rate') else 0.0,
                "volume": int(quote.volume)
            }
            return json.dumps(res, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Error fetching price for {code}: {e}"

    def place_order(self, action: str, code: str, qty: int, price: Optional[int] = None, confirm: str = "") -> str:
        if confirm != "YES":
            return f"ORDER_STOPPED: Please call again with confirm='YES' to actually execute the {action} order."
        if not self.kis: return "KIS client not initialized."
        try:
            stock = self.kis.stock(code)
            # Market order if price is 0 or None
            if action.lower() == "buy":
                order = stock.buy(qty=qty, price=price or 0)
            elif action.lower() == "sell":
                order = stock.sell(qty=qty, price=price or 0)
            else:
                return "Invalid action. Use 'buy' or 'sell'."
            return f"SUCCESS: {action.upper()} {code} x {qty} @ {price or 'MARKET'} (Order ID: {order.id})"
        except Exception as e:
            return f"Order failed: {e}"

if __name__ == "__main__":
    import sys
    agent = StockTradingAgent()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "balance":
            print(agent.get_balance())
        elif cmd == "price" and len(sys.argv) > 2:
            print(agent.get_price(sys.argv[2]))
        elif cmd in ["buy", "sell"] and len(sys.argv) > 4:
            p = int(sys.argv[4]) if sys.argv[4].isdigit() else None
            conf = sys.argv[5] if len(sys.argv) > 5 else ""
            print(agent.place_order(cmd, sys.argv[2], int(sys.argv[3]), p, conf))
    else:
        print("Usage: python stock_trading_mcp.py [balance|price|buy|sell] ...")
