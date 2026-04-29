import yt_dlp
import os

def download_video(url: str, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "worst[ext=mp4]/worst",  # lowest quality to save memory
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",  # shorter filename
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path