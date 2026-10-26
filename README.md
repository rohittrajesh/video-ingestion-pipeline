# Video Ingestion Pipeline

A prototype for reviewing the production quality of TikTok and other short-form promotional videos before publication. It brings video ingestion, visual measurements, audio processing and structured feedback into a single review workflow.

## Video ingestion

- Accept reference and target video uploads through an analysis endpoint.
- Work with local video files.
- Download clips from supported video URLs through the ingestion helper.
- Prepare media for frame extraction and audio analysis.

## Visual analysis

- Sample video frames and measure average brightness and contrast.
- Estimate scene-change frequency as a signal of editing pace.
- Extract a representative frame for AI-assisted review.
- Define visual review criteria for lighting, contrast and close-up framing.

## Audio analysis

- Extract the video's audio track.
- Calculate average audio energy.
- Provide a speech-transcription helper.
- Define voiceover review criteria for vocal energy, clarity and brand emphasis.

## Quality scoring and feedback

- Combine visual and audio criteria through a weighted scoring rubric.
- Identify criteria that fall below the rubric's review threshold.
- Return structured feedback and a recommendation: **pass**, **manual review** or **re-shoot**.
- Support an intended 0–100 quality-score format once the input metrics are consistently normalized.

## Development scope

The repository contains the ingestion, feature-extraction and scoring components. End-to-end AI integration and score normalization still require completion. Reference videos are accepted by the API, but reference-based benchmarking is a planned extension.

The assessment is intended to help creators prioritize production-quality improvements. It is not a validated predictor of TikTok views, engagement or sales.
