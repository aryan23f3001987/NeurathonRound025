from deep_translator import GoogleTranslator
import os

def read_files():
    """Reads language and text content from files."""
    lang_file_path = r"language.txt"
    text_file_path = r"text.txt"

    language = open(lang_file_path, "r", encoding="utf-8").read().strip().lower() if os.path.exists(lang_file_path) else "english"
    text_content = open(text_file_path, "r", encoding="utf-8").read().strip() if os.path.exists(text_file_path) else ""

    return language, text_content

def translate_text(text, language):
    """Translates text to English using deep-translator."""
    if not text:
        return "❌ No text provided for translation."

    lang_map = {
        "hindi": "hi",
        "english": "en",
    }

    lang_code = lang_map.get(language, "en")  # Default to English

    try:
        translated = GoogleTranslator(source=lang_code, target="en").translate(text)
        return translated if translated else "❌ Empty response from translation API."
    except Exception as e:
        return f"❌ Translation failed: {e}"

def save_translated_text(translated_text):
    """Overwrites text.txt with the translated text."""
    text_file_path = r"text.txt"
    with open(text_file_path, "w", encoding="utf-8") as trans_file:
        trans_file.write(translated_text)
    
    print(f"✅ Translated text saved in: {text_file_path}")

if __name__ == "__main__":
    language, text_content = read_files()
    print(f"📌 Detected Language: {language}")
    print(f"📌 Original Text: {text_content}")

    if text_content:
        translated_text = translate_text(text_content, language)
        print(f"🌍 Translated Text: {translated_text}")
        save_translated_text(translated_text)
    else:
        print("❌ No text found in `text.txt`.")