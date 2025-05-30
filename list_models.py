# list_models.py
import os
from google import genai

# make sure GEMINI_KEY is set in your environment
client = genai.Client(api_key=os.environ["GEMINI_KEY"])

# list() lives on client.models
for m in client.models.list():
    print(m.name, "→ supports:", m.supported_actions)
