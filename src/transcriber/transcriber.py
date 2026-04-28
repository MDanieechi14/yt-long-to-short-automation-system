import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

def transcribe_video(file_path: str) -> aai.Transcript:
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    config = aai.TranscriptionConfig(
        speech_models=[aai.SpeechModel.universal]
    )

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    print(f"✅ Transcription complete! Words: {len(transcript.words)}")
    return transcript