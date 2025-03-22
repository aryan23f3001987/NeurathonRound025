from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load the locally saved FLAN-T5 model
model_name = "flan_t5_model"
tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_flashcards(file_path="text.txt", output_file="flashcards.txt", num_flashcards=5):
    """Generates simple, clear, and structured flashcards from a summarized text file and saves them."""
    
    # Read summarized text
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()
    
    if not text:
        print("❌ No text found for flashcard generation.")
        return
    
    # Prepare input for T5
    input_text = f"Generate {num_flashcards} key facts: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
    
    # Generate flashcards
    flashcard_ids = model.generate(
        inputs,
        max_length=80,  # Shorter facts
        min_length=20,  # Meaningful information
        length_penalty=1.2,
        num_beams=5,
        early_stopping=True
    )

    # Decoding and formatting flashcards
    flashcards = tokenizer.decode(flashcard_ids[0], skip_special_tokens=True)
    flashcards_list = flashcards.split("\n")  # Ensures each fact is a separate line

    # Save flashcards (each in a new line)
    with open(output_file, "w", encoding="utf-8") as out_file:
        for flashcard in flashcards_list:
            fact = flashcard.strip().replace("*", "").replace("- ", "")  # Remove symbols if any
            if fact:  # Avoid empty lines
                out_file.write(fact + "\n")

    print(f"✅ Flashcards generated! Saved to {output_file}")

if __name__ == "__main__":
    generate_flashcards()