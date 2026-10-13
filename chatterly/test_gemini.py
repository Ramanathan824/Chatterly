import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
if not ENV_FILE.is_file():
    ENV_FILE = Path(__file__).resolve().parent / ".env"

load_dotenv(ENV_FILE)
print(f"Using .env file: {ENV_FILE}")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                'Reply with exactly this sentence and no other text: '
                '"Hi! I\'m Chatterly, your friendly AI assistant."'
            )
        )

        print("Gemini response:")
        print(response.text)

    except Exception as error:
        print("AI request failed:", error)