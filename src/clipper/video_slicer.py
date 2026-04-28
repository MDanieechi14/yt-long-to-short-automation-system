import os
import subprocess

def slice_clips(video_path: str, clips: list, output_dir: str = "output/clips") -> list:
    """
    Slices a video into clips using ffmpeg directly (memory efficient).
    Returns list of output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    output_paths = []

    for i, clip in enumerate(clips):
        start = clip["start"]
        end = clip["end"]
        duration = end - start
        label = clip["text"].replace(" ", "_")[:20]
        output_path = f"{output_dir}/clip_{i+1}_{label}.mp4"

        print(f"✂️  Slicing clip {i+1}: {start}s → {end}s ({clip['text']})")

        command = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-loglevel", "error",
            output_path
        ]

        subprocess.run(command, check=True)
        output_paths.append(output_path)
        print(f"✅ Saved: {output_path}")

    return output_paths