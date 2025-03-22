from pytube import YouTube
from moviepy.editor import AudioFileClip

def convert_youtube_to_audio(youtube_url, output_audio_path="output_audio.wav"):
    # Download the highest-quality audio from YouTube
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_audio_path = audio_stream.download(filename="temp_audio.mp4")

    # Convert the downloaded audio to WAV format
    audio = AudioFileClip(temp_audio_path)
    audio.write_audiofile(output_audio_path)
    
    return output_audio_path