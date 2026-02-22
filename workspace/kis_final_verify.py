import time
from pykis import PyKis
from pathlib import Path

def load_env():
    p = Path(r"D:\OpenClaw\.env")
    kv = {}
    if p.exists():
        for line in p.read_text(encoding='utf-8', errors='ignore').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                kv[k.strip()] = v.strip().strip('"').strip("'")
    return kv

def main():
    env = load_env()
    # Based on user's manual correction and screenshot:
    user_id = env.get("KIS_USER_ID", "2873465")
    # User said 290300 is password. nigora~~1 was also mentioned earlier as password.
    # Typically KIS needs AppKey, AppSecret, and potentially an HTS ID.
    # Some versions of pykis use 'secret' or 'secretkey'.
    
    app_key = env.get("KIS_APP_KEY")
    app_secret = env.get("KIS_APP_SECRET")
    account = "5016942501" 

    print(f"Final Verification: ID={user_id}, Account={account}")
    try:
        kis = PyKis(
            id=user_id,
            account=account,
            appkey=app_key,
            secretkey=app_secret,
            virtual_id=user_id,
            virtual_appkey=app_key,
            virtual_secretkey=app_secret
        )
        # Try fetching Samsung Price (005930)
        stock = kis.stock("005930")
        quote = stock.quote()
        print(f"VERIFY_SUCCESS|{quote.name}|{quote.price}")
    except Exception as e:
        print(f"VERIFY_FAILED|{e}")

if __name__ == "__main__":
    main()
