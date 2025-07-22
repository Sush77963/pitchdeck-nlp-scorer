import os
import pdfplumber

# Folder where your pitch decks are stored
data_folder = "data"
output_folder = "outputs"

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDF files
for filename in os.listdir(data_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(data_folder, filename)
        print(f"🔍 Reading {filename}...")

        # Extract text from PDF
        with pdfplumber.open(filepath) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""
                full_text += "\n--- Page Break ---\n"

        # Save extracted text to .txt file
        text_filename = filename.replace(".pdf", ".txt")
        with open(os.path.join(output_folder, text_filename), "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"✅ Saved text to {text_filename}")
