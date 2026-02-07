import os

keys = [
    "DEEPSEEK_API_KEY",
    "CEREBRAS_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "GROQ_API_KEY",
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "SAMBANOVA_API_KEY"
]

for key in keys:
    val = os.environ.get(key)
    if val:
        print(f"{key}: {val[:5]}...{val[-4:] if len(val) > 4 else ''} (Length: {len(val)})")
    else:
        # Check User environment specifically if not in process env
        import subprocess
        try:
            cmd = f'[System.Environment]::GetEnvironmentVariable("{key}", "User")'
            result = subprocess.check_output(['powershell', '-Command', cmd], text=True).strip()
            if result:
                print(f"{key} (User): {result[:5]}...{result[-4:] if len(result) > 4 else ''} (Length: {len(result)})")
            else:
                print(f"{key}: NOT FOUND")
        except:
            print(f"{key}: ERROR CHECKING")
