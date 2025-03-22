import streamlit as st
import os
import tempfile
import subprocess
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

def save_language(language):
    with open("language.txt", "w", encoding="utf-8") as lang_file:
        lang_file.write(language.lower())

def read_text():
    if os.path.exists("text.txt"):
        with open("text.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""

def read_summarized_text():
    if os.path.exists("summarized_text.txt"):
        with open("summarized_text.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""

def read_flashcards():
    if os.path.exists("flashcards.txt"):
        with open("flashcards.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []

st.title("Audio, Text, or Image to Text Converter & AI Processing")
option = st.radio("Choose an input method:", ["Audio (File/YouTube)", "Text", "Upload Image"])

if option in ["Text", "Upload Image"]:
    language = st.selectbox("Select language:", ["English", "Hindi"])
else:
    language = "English"
save_language(language)

if option == "Audio (File/YouTube)":
    audio_option = st.radio("Choose audio source:", ["Upload File", "YouTube Link"])
    if audio_option == "Upload File":
        uploaded_audio = st.file_uploader("Upload an audio file", type=['mp3', 'wav'])
        if uploaded_audio and st.button("Convert Audio to Text"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(uploaded_audio.read())
                temp_audio_path = temp_audio.name
            subprocess.run(["python", "Audio_To_Text_Actual.py", temp_audio_path])
            os.remove(temp_audio_path)
    elif audio_option == "YouTube Link":
        yt_link = st.text_input("Enter YouTube Video Link:")
        if st.button("Extract & Convert Audio") and yt_link:
            subprocess.run(["python", "Youtube_Audio_To_Text.py", yt_link])

elif option == "Text":
    user_text = st.text_area("Enter text below:")
    if st.button("Save Text"):
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(user_text)
        
        if language.lower() == "hindi":
            subprocess.run(["python", "translate_to_english.py"])

elif option == "Upload Image":
    uploaded_file = st.file_uploader("📷 Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        with open("uploaded_image.jpg", "wb") as f:
            f.write(uploaded_file.read())
        st.image("uploaded_image.jpg", caption="Uploaded Image", use_column_width=True)
        subprocess.run(["python", "Image_To_Text.py"])
        
        if language.lower() == "hindi":
            subprocess.run(["python", "translate_to_english.py"])

text_content = read_text()
translated_text = text_content
if text_content and language.lower() == "hindi":
    if os.path.exists("translated.txt"):
        with open("translated.txt", "r", encoding="utf-8") as trans_file:
            translated_text = trans_file.read().strip()

if text_content:
    st.subheader("Extracted/Saved Text")
    with st.expander("📄 View Original Text"):
        st.write(text_content)

if st.button("Summarize Text"):
    subprocess.run(["python", "summarization.py"])
    st.rerun()

summarized_text = read_summarized_text()
if summarized_text:
    st.subheader("Summarized Text")
    with st.expander("📖 View Summarized Text"):
        st.write(summarized_text)

if st.button("Generate Flashcards"):
    subprocess.run(["python", "Flashcard_section.py"])
    st.rerun()

flashcards = read_flashcards()
if flashcards:
    st.subheader("Flashcards")
    with st.expander("🃏 View Generated Flashcards"):
        for i, flashcard in enumerate(flashcards, 1):
            with st.container():
                question, answer = flashcard.split("?") if "?" in flashcard else (flashcard, "")
                st.markdown(f"**Flashcard {i}:**")
                st.info(f"📌 {question.strip()}?")
                if answer.strip():
                    with st.expander("💡 Reveal Answer"):
                        st.success(answer.strip())
                st.markdown("---")

if st.button("Refresh App"):
    for file in ["text.txt", "language.txt", "uploaded_image.jpg", "translated.txt", "summarized_text.txt", "flashcards.txt"]:
        if os.path.exists(file):
            os.remove(file)
    st.rerun()