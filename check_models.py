import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API Key found in .env")
    exit()

print(f"Checking models for key: {api_key[:5]}...")

# We use the direct web link to ask Google (bypassing the library issues)
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("\n--- YOUR AVAILABLE MODELS ---")
    valid_models = []
    for model in data.get('models', []):
        # We only care about models that can chat (generateContent)
        if "generateContent" in model.get('supportedGenerationMethods', []):
            # Google gives names like "models/gemini-pro". We just want "gemini-pro"
            clean_name = model['name'].replace("models/", "")
            print(f"✅ {clean_name}")
            valid_models.append(clean_name)
    
    if not valid_models:
        print("\nWARNING: No chat models found. You might need to enable the 'Generative Language API' in Google Cloud Console.")
else:
    print(f"\nERROR: Could not connect to Google. Status: {response.status_code}")
    print(response.text)