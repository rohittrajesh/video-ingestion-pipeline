import os
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import ffmpeg
import uvicorn

from ingest.downloader import fetch_video
from features.video_features import compute_brightness_contrast, compute_scene_rate
from features.audio_features import extract_audio, compute_audio_energy, transcribe_audio
from analysis.llm_client import LLMClient
from scoring.rubric import score_and_feedback

# ─── Load .env ────────────────────────────────────────────────────────────────
env_path = find_dotenv()
if not env_path:
    raise RuntimeError("No .env file found!")
load_dotenv(env_path, override=True)

GEMINI_KEY   = os.getenv("GEMINI_KEY")
OPENAI_KEY   = os.getenv("OPENAI_API_KEY")
if not GEMINI_KEY or not OPENAI_KEY:
    raise RuntimeError("GEMINI_KEY and OPENAI_API_KEY must both be set in your .env")

llm = LLMClient(GEMINI_KEY, OPENAI_KEY)

# ─── FastAPI setup ────────────────────────────────────────────────────────────
app = FastAPI()
temp_dir = Path("temp")
temp_dir.mkdir(exist_ok=True)

@app.post("/analyze")
async def analyze(
    reference: UploadFile = File(...),
    target:    UploadFile = File(...),
):
    # save uploads
    ref_path = temp_dir / reference.filename
    tgt_path = temp_dir / target.filename
    open(ref_path, "wb").write(await reference.read())
    open(tgt_path, "wb").write(await target.read())

    # ingest/download
    ref_vid = fetch_video(str(ref_path))
    tgt_vid = fetch_video(str(tgt_path))

    # video features
    vid_feats = compute_brightness_contrast(tgt_vid)
    vid_feats.update(compute_scene_rate(tgt_vid))

    # audio features & transcript
    audio_seg   = extract_audio(tgt_vid)
    aud_feats   = compute_audio_energy(audio_seg)
    transcript  = transcribe_audio(audio_seg)["transcript"]

    # grab a single key-frame at 1s
    sample_frame = temp_dir / "frame1.jpg"
    (
        ffmpeg
        .input(str(tgt_vid), ss=1)
        .filter("scale", 640, -1)
        .output(str(sample_frame), vframes=1)
        .run(quiet=True, overwrite_output=True)
    )

    # LLM analysis
    vision_scores = llm.analyze_frame(str(sample_frame))
    audio_scores  = llm.analyze_transcript(transcript)

    # scoring & return
    return score_and_feedback(vid_feats, aud_feats, vision_scores, audio_scores)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
