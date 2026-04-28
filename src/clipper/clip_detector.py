def detect_clips(transcript, clip_duration: int = 45, max_clips: int = 3) -> list:
    """
    Splits transcript into equal time-based chunks as clips.
    """
    if not transcript.words:
        print("⚠️ No words found in transcript.")
        return []

    total_duration = transcript.words[-1].end / 1000
    print(f"📹 Total duration: {total_duration:.2f}s")

    clips = []
    start = 0

    while start + clip_duration <= total_duration and len(clips) < max_clips:
        end = start + clip_duration
        clips.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "text": f"clip_{len(clips)+1}",
            "rank": 1
        })
        start += clip_duration

    print(f"✅ Found {len(clips)} clips!")
    return clips