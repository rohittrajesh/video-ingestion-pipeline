import os
from pathlib import Path
from yt_dlp import YoutubeDL
import ffmpeg


def fetch_video(source: str, output_dir: Path = Path("temp")) -> Path:
    """
    Accepts a local path or URL.
    If URL, downloads to output_dir.
    Returns a Path to a local .mp4 file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    if source.startswith("http://") or source.startswith("https://"):
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': str(output_dir / '%(id)s.%(ext)s'),
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(source, download=True)
            filename = ydl.prepare_filename(info)
            # ensure .mp4 extension
            if not filename.endswith(".mp4"):
                mp4_path = Path(filename).with_suffix(".mp4")
                ffmpeg.input(filename).output(str(mp4_path)).run(overwrite_output=True)
                Path(filename).unlink()
                return mp4_path
            return Path(filename)
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")
        return path