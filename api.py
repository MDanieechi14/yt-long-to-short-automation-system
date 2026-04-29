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
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500