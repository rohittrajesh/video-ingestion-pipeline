from pydub import AudioSegment
import numpy as np
import tempfile
import os
import openai


def extract_audio(video_path, format="wav"):
    """
    Extracts the audio track from a video file.
    Returns a pydub.AudioSegment.
    """
    audio = AudioSegment.from_file(str(video_path))
    return audio


def compute_audio_energy(audio_segment):
    """
    Compute average RMS energy of the audio segment.
    """
    samples = np.array(audio_segment.get_array_of_samples())
    energy = np.mean(samples.astype(float)**2)
    return {"average_energy": float(energy)}


def transcribe_audio(audio_segment, model="whisper-1"):
    """
    Transcribes audio using OpenAI Whisper API.
    Returns a dict with `transcript` and raw `whisper_response`.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_segment.export(tmp.name, format="wav")
        tmp.flush()
        with open(tmp.name, "rb") as f:
            resp = openai.Audio.transcribe(model, f)
        os.unlink(tmp.name)
    return {"transcript": resp.get("text", ""), "whisper_response": resp}