# analysis/llm_client.py
import os
import json
import openai                             # for Whisper
from google import genai                 # *not* "import google_genai"
from google.genai import TextPrompt, ImagePrompt
from .prompts import FRAME_PROMPT, AUDIO_PROMPT

class LLMClient:
    def __init__(self, gemini_key: str, openai_key: str):
        # 1) configure the Google GenAI client for Gemini Vision
        genai.configure(api_key=gemini_key)
        # 2) configure the OpenAI client for Whisper audio
        openai.api_key = openai_key

    def analyze_frame(self, image_path: str) -> dict:
        # load the image bytes
        with open(image_path, "rb") as f:
            img = f.read()

        # build a multimodal prompt
        prompt = TextPrompt(
            text=FRAME_PROMPT,
            image=ImagePrompt(data=img, mime_type="image/jpeg")
        )

        # call the vision model
        resp = genai.generate_content(
            model="models/gemini-1.5-flash",
            prompt=prompt
        )

        # extract and clean the JSON from the markdown fence
        raw = resp.choices[0].content
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("\n```", 1)[0].strip()

        return json.loads(raw)

    def analyze_transcript(self, transcript: str) -> dict:
        # transcribe with Whisper (OpenAI v0.28 API)
        wh = openai.Audio.transcribe("whisper-1", transcript)
        return {"transcript": wh["text"]}
