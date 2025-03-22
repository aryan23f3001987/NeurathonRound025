import os
import sys
import whisper

# Ensure FFmpeg is available
os.environ["PATH"] += os.pathsep + r"C:\Users\sanje\Downloads\ffmpeg\ffmpeg-2025-03-13-git-958c46800e-essentials_build\bin"

# Ensure audio file is provided
if len(sys.argv) < 2:
    print("❌ Error: No audio file provided.")
    sys.exit(1)

audio_path = sys.argv[1]

# Read the saved language from language.txt
language_mapping = {
    "english": "en",
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "german": "de",
}  # Add more if needed

language = None  # Default: Auto-detect

if os.path.exists("language.txt"):
    with open("language.txt", "r", encoding="utf-8") as f:
        saved_language = f.read().strip().lower()
        language = language_mapping.get(saved_language, None)  # Convert to ISO 639-1 code

# Load Whisper model
model = whisper.load_model("base")

try:
    print(f"🎯 Using Language: {language if language else 'Auto-Detect'}")

    # Force Whisper to use the specified language
    result = model.transcribe(
        audio_path,
        language=language, 
        task="transcribe",  # Ensures it's transcription, not translation
        fp16=False  # Prevents potential errors on some systems
    )

    text = result["text"]

    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Transcription Complete! Text saved to text.txt")
    print(text)

except Exception as e:
    print(f"❌ Error: {str(e)}")