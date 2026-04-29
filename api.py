from flask import Flask, request, jsonify
from src.downloader.downloader import download_video
from src.transcriber.transcriber import transcribe_video
from src.clipper.clip_detector import detect_clips
from src.clipper.video_slicer import slice_clips
from src.captioner.captioner import add_captions

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        print(f"Starting processing for: {url}")
        video_path = download_video(url)
        transcript = transcribe_video(video_path)
        clips = detect_clips(transcript)
        clip_paths = slice_clips(video_path, clips)
        captioned = [add_captions(p, transcript) for p in clip_paths]

        return jsonify({
            "status": "success",
            "clips": captioned,
            "message": "Processing completed successfully"
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)