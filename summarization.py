from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load T5 model and tokenizer
model_name = "t5-small"  # You can use your fine-tuned model here
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_text(file_path, output_file="summarized_text.txt", max_length=300, min_length=150):
    """Reads text from a file, summarizes it using T5, and saves the summary to another file."""
    
    # Read input text
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()
    
    if not text:
        print("❌ No text found for summarization.")
        return
    
    # Prepare input for T5
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate summary
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Save summarized text
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write(summary)
    
    print(f"✅ Summarization complete! Saved to {output_file}")

if __name__ == "__main__":
    summarize_text("text.txt")