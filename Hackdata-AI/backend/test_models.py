from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models_to_test = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest"
]

for model in models_to_test:
    print("\nTesting:", model)

    try:
        response = client.models.generate_content(
            model=model,
            contents="Say only: OK"
        )
        print("SUCCESS:", response.text)

    except Exception as e:
        print("FAILED:", type(e).__name__)
        print(str(e)[:300])