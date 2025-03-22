import cv2
import pytesseract
import os
import platform
import sys

# Set Tesseract data path (Linux default)
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"

# Auto-detect Tesseract path (for Windows users)
if platform.system() == "Windows":
    tess_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tess_path):
        pytesseract.pytesseract.tesseract_cmd = tess_path
    else:
        print("⚠️ Warning: Tesseract not found! Ensure it's installed and in PATH.")

def extract_text(image_path, lang="eng"):
    """Extracts text from an image using OCR with specified language."""
    if not os.path.exists(image_path):
        raise FileNotFoundError("❌ Image file not found!")

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("❌ Error loading image. Ensure it's a valid image file.")

    # Convert to grayscale for better OCR accuracy
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding (improves OCR on noisy backgrounds)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)

    # Perform OCR with the given language
    text = pytesseract.image_to_string(processed, lang=lang)

    return text.strip()

def main():
    """Main function to process the image and save extracted text."""
    image_path = "uploaded_image.jpg"  # Image saved by Streamlit
    lang = sys.argv[1] if len(sys.argv) > 1 else "eng+hin"  # Default: Auto-detect both Hindi & English

    try:
        extracted_text = extract_text(image_path, lang)
        
        # Save extracted text to text.txt
        with open("text.txt", "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)
        
        print("✅ Text extraction completed. Check text.txt.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()