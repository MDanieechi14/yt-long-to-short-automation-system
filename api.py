from flask import Flask, request, jsonify
from src.downloader.downloader import download_video
from src.transcriber.transcriber import transcribe_video
from src.clipper.clip_detector import detect_clips
from src.clipper.video_slicer import slice_clips
from src.captioner.captioner import add_captions
import threading
import uuid
import json
import os

app = Flask(__name__)
JOBS_FILE = "jobs.json"

def read_jobs():
    if not os.path.exists(JOBS_FILE):
        return {}
    with open(JOBS_FILE, "r") as f:
        return json.load(f)

def write_job(job_id: str, data: dict):
    jobs = read_jobs()
    jobs[job_id] = data
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f)

def run_pipeline(job_id: str, url: str):
    try:
        write_job(job_id, {"status": "processing"})
        video_path = download_video(url)
        transcript = transcribe_video(video_path)
        clips = detect_clips(transcript)
        clip_paths = slice_clips(video_path, clips)
        captioned = [add_captions(p, transcript) for p in clip_paths]
        write_job(job_id, {"status": "done", "clips": captioned})
        print(f"Job {job_id} completed!")
    except Exception as e:
        write_job(job_id, {"status": "error", "error": str(e)})
        print(f"Job {job_id} failed: {str(e)}")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    job_id = str(uuid.uuid4())
    thread = threading.Thread(target=run_pipeline, args=(job_id, url))
    thread.start()
    return jsonify({"job_id": job_id, "status": "started"})

@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    jobs = read_jobs()
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@app.route("/routes", methods=["GET"])
def routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)