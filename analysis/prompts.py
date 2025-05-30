# Visual analysis prompt for a single frame
FRAME_PROMPT = """
Assume that we need an expert video-analysis on the provided video to correctly determine if it is an appropriate 
advertisement that excells in selling the product. To do this, we will: 
Rate the following characteristics of this single video frame on a scale from 0 to 10:
- Brightness
- Contrast
- Presence of close-ups (0=no close-ups, 10=all close-ups) with close-ups meaning how close the person 
or product is to the camera. 

Respond in JSON:
{"brightness": <int>, "contrast": <int>, "closeup_score": <int>}
"""

# Audio analysis prompt for the transcript\
AUDIO_PROMPT = """
Assume that we need an expert audio-analysis on the provided video to correctly determine if it is an appropriate 
advertisement that excells in selling the product. To do this, we will: 
rate the transcript of a user's voiceover, on a scale 0 to 10:
- Vocal energy
- Clarity

Provide JSON:
{"vocal_energy": <int>, "clarity": <int>, "brand_emphasis": <int>}
"""