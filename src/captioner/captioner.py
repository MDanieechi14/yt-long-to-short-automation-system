import os
import subprocess

def ms_to_srt_time(ms: int) -> str:
    """Convert milliseconds to SRT timestamp format."""
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def generate_srt(transcript, video_start_s: float, video_end_s: float, srt_path: str):
    """Generate an SRT subtitle file from transcript words."""
    video_start_ms = video_start_s * 1000
    video_end_ms = video_end_s * 1000

    words = [
        w for w in transcript.words
        if video_start_ms <= w.start <= video_end_ms
    ]

    with open(srt_path, "w") as f:
        for i, word in enumerate(words):
            start = ms_to_srt_time(int(word.start - video_start_ms))
            end = ms_to_srt_time(int(word.end - video_start_ms))
            f.write(f"{i+1}\n{start} --> {end}\n{word.text}\n\n")

    print(f"📝 SRT generated: {srt_path}")

def add_captions(video_path: str, transcript, output_dir: str = "output/captioned") -> str:
    """
    Burns captions onto video using ffmpeg subtitle filter.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("output/srt", exist_ok=True)

    filename = os.path.basename(video_path)
    srt_path = f"output/srt/{filename}.srt"
    output_path = f"{output_dir}/captioned_{filename}"

    # Get clip duration using ffprobe
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ], capture_output=True, text=True)
    duration = float(result.stdout.strip())

    # Generate SRT — assume clip starts at 0 for simplicity
    generate_srt(transcript, 0, duration, srt_path)

    # Burn subtitles with ffmpeg
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=2'",
        "-c:a", "copy",
        "-loglevel", "error",
        output_path
    ]

    subprocess.run(command, check=True)
    print(f"✅ Captioned video saved: {output_path}")
    return output_path