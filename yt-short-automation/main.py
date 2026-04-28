from src.downloader.downloader import download_video
from src.transcriber.transcriber import transcribe_video
from src.clipper.clip_detector import detect_clips
from src.clipper.video_slicer import slice_clips
from src.captioner.captioner import add_captions

def run_pipeline(youtube_url: str):
    print("\n🚀 Starting YouTube Long-to-Short Pipeline...")

    # Step 1: Download
    print("\n📥 Downloading video...")
    video_path = download_video(youtube_url)
    print(f"Video saved: {video_path}")

    # Step 2: Transcribe
    print("\n🎙️ Transcribing video...")
    transcript = transcribe_video(video_path)

    # Step 3: Detect clips
    print("\n🔍 Detecting highlight clips...")
    clips = detect_clips(transcript)

    if not clips:
        print("❌ No clips detected. Exiting.")
        return

    # Step 4: Slice clips
    print("\n✂️ Slicing clips...")
    clip_paths = slice_clips(video_path, clips)

    # Step 5: Add captions
    print("\n💬 Adding captions...")
    for clip_path in clip_paths:
        add_captions(clip_path, transcript)

    print("\n✅ Pipeline complete! Check output/captioned/ for your Shorts.")

if __name__ == "__main__":
    run_pipeline("https://www.youtube.com/watch?v=dQw4w9WgXcQ")