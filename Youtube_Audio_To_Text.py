import os
import sys
import whisper
import yt_dlp

# Check if a YouTube link is provided
if len(sys.argv) < 2:
    print("❌ Error: No YouTube link provided.")
    sys.exit(1)

youtube_url = sys.argv[1]
output_audio = "downloaded_audio.wav"  # Final expected output file

# Download audio using yt-dlp
print("📥 Downloading audio from YouTube...")
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded_audio',  # Base name without extension
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
except Exception as e:
    print(f"❌ Error downloading audio: {str(e)}")
    sys.exit(1)

# Ensure the audio file exists (check the correct filename)
final_audio_path = "downloaded_audio.wav"  # Matches FFmpegExtractAudio output
if not os.path.exists(final_audio_path):
    print("❌ Error: Audio file was not downloaded or converted!")
    sys.exit(1)

# Load Whisper model
print("🧠 Loading Whisper model...")
model = whisper.load_model("base")

# Transcribe audio (forcing English)
print("📝 Transcribing audio...")
try:
    result = model.transcribe(final_audio_path, language="english")
    text = result["text"]

    if text.strip():
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ Transcription complete! Text saved to text.txt")
        print("\n📝 Transcribed Text (First 500 characters):\n", text[:500])
    else:
        print("❌ Transcription failed: No text detected.")

except Exception as e:
    print(f"❌ Error during transcription: {str(e)}")
    sys.exit(1)

# Clean up downloaded file
os.remove(final_audio_path)