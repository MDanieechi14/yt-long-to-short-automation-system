import yt_dlp
import os

def download_video(url: str, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "worstvideo[height<=360]+worstaudio/worst[height<=360]/worst",
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        "merge_output_format": "mp4",
        "postprocessor_args": [
            "-vf", "scale=640:-2"
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path