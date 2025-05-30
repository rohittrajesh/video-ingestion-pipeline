# Weights for each criterion 
CRITERIA_WEIGHTS = {
    "brightness":      0.15,
    "contrast":        0.10,
    "closeup_score":   0.10,
    "scene_cuts_per_sec": 0.05,
    "average_energy":  0.10,
    "vocal_energy":    0.15,
    "clarity":         0.15,
    "brand_emphasis":  0.20,
}


def score_and_feedback(video_features: dict,
                       audio_features: dict,
                       vision_scores: dict,
                       audio_scores: dict) -> dict:
    """
    Combine all metrics into a 0–100 quality score,
    generate feedback bullet points, and recommendation.
    """
    metrics = {**video_features, **audio_features, **vision_scores, **audio_scores}
    total = 0.0
    for k, w in CRITERIA_WEIGHTS.items():
        val = metrics.get(k, 0.0)
        total += val * w
    # scale 0–10 → 0–100
    quality = round(total * 10, 2)

    feedback = []
    for k, val in metrics.items():
        if k in CRITERIA_WEIGHTS and val < 5:
            feedback.append(f"{k} is low ({val:.1f})")

    if quality >= 70:
        rec = "pass"
    elif quality >= 40:
        rec = "manual_review"
    else:
        rec = "re-shoot"

    return {"score": quality, "feedback": feedback, "recommendation": rec}