# YT Long-to-Short Automation System

## What it does
Automatically converts YouTube long-form videos into short clips using AI transcription and video processing.

## Tech Stack
- Python + Flask (API)
- yt-dlp (video download)
- AssemblyAI (transcription)
- ffmpeg (video slicing)
- n8n (workflow automation)
- Render (cloud deployment)

## Architecture
Google Sheets → n8n → Flask API → Pipeline → Clips

## Known Limitations & Solutions
| Limitation | Cause | Solution |
|------------|-------|----------|
| 512MB RAM on Render free tier | Video processing is memory intensive | Upgrade to Render $7/month (2GB RAM) |
| Low resolution output (320p) | Memory constraint workaround | Full quality available on paid tier |
| No captions on cloud | Memory constraint | Runs locally with full captions |
| Single clip output | Memory constraint | Multiple clips on paid tier |

## Local Setup
```bash
git clone <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Production Notes
For full quality output including captions and multiple clips,
a minimum of 2GB RAM is recommended.