import os
import subprocess

def slice_clips(video_path: str, clips: list, output_dir: str = "output/clips") -> list:
    os.makedirs(output_dir, exist_ok=True)
    output_paths = []

    for i, clip in enumerate(clips):
        start = clip["start"]
        end = clip["end"]
        duration = end - start
        output_path = f"{output_dir}/clip_{i+1}.mp4"

        print(f"✂️  Slicing clip {i+1}: {start}s → {end}s")

        command = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(duration),
            "-vf", "scale=320:-2",      # tiny resolution
            "-r", "15",                  # low framerate
            "-c:v", "libx264",
            "-preset", "ultrafast",      # lowest CPU/memory usage
            "-crf", "35",               # lower quality = less memory
            "-c:a", "aac",
            "-b:a", "64k",              # low audio bitrate
            "-threads", "1",            # single thread to save memory
            "-loglevel", "error",
            output_path
        ]

        subprocess.run(command, check=True)
        output_paths.append(output_path)
        print(f"✅ Saved: {output_path}")

    return output_paths