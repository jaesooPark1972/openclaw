import os
from upstash_vector import Index
from dotenv import load_dotenv

# Load env from D:\OpenClaw\.env
load_dotenv(r"D:\OpenClaw\.env")

def test_connection():
    url = os.getenv("UPSTASH_VECTOR_REST_URL")
    token = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    
    print(f"URL: {url}")
    print(f"Token: {token[:10]}..." if token else "Token: None")
    
    if not url or not token:
        print("❌ Error: Missing credentials.")
        return

    try:
        index = Index(url=url, token=token)
        # Try a lightweight operation, e.g. info or fetch generic
        info = index.info()
        print("✅ Connection Successful!")
        print(f"Vector Count: {info.vector_count}")
        print(f"Index Dimension: {info.dimension}")
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")

if __name__ == "__main__":
    test_connection()
