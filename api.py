from flask import Flask, request, jsonify
from src.downloader.downloader import download_video
from src.transcriber.transcriber import transcribe_video
from src.clipper.clip_detector import detect_clips
from src.clipper.video_slicer import slice_clips
from src.captioner.captioner import add_captions

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        video_path = download_video(url)
        transcript = transcribe_video(video_path)
        clips = detect_clips(transcript)
        clip_paths = slice_clips(video_path, clips)
        captioned = [add_captions(p, transcript) for p in clip_paths]

        return jsonify({
            "status": "success",
            "clips": captioned
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)