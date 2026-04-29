from flask import Flask, request, jsonify
from src.downloader.downloader import download_video
from src.transcriber.transcriber import transcribe_video
from src.clipper.clip_detector import detect_clips
from src.clipper.video_slicer import slice_clips
import traceback

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        print(f"Starting pipeline for: {url}")
        video_path = download_video(url)
        print(f"Downloaded: {video_path}")
        transcript = transcribe_video(video_path)
        print(f"Transcribed: {len(transcript.words)} words")
        clips = detect_clips(transcript)
        print(f"Detected: {len(clips)} clips")
        clip_paths = slice_clips(video_path, clips)
        print(f"Sliced: {clip_paths}")
        return jsonify({"status": "done", "clips": clip_paths})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/routes", methods=["GET"])
def routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)