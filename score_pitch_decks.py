import os
import pandas as pd

# Folder with extracted text files
input_folder = "outputs"

# Keywords for each metric
score_keywords = {
    "Problem Clarity": ["problem", "pain", "struggle", "issue", "gap"],
    "Market Potential": ["market", "TAM", "SAM", "SOM", "opportunity", "billion"],
    "Traction": ["users", "customers", "revenue", "growth", "downloads", "sales"],
    "Team Strength": ["team", "founder", "co-founder", "experience", "background"],
    "Business Model": ["model", "revenue", "pricing", "plan", "monetize", "subscription"],
    "Confidence/Tone": ["scale", "vision", "global", "disrupt", "leader", "billion"]
}

# Score weight per category
max_score = 10

# Function to score based on keyword frequency
def score_text(text, keywords):
    score = 0
    for word in keywords:
        if word.lower() in text.lower():
            score += 1
    return min(score, max_score)

# Score all files
results = []
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        deck_name = filename.replace(".txt", "")
        scores = {"Startup": deck_name}

        # Score each metric
        for metric, keywords in score_keywords.items():
            scores[metric] = score_text(text, keywords)

        # Total score (out of 60)
        scores["Total Score"] = sum(scores[metric] for metric in score_keywords)
        results.append(scores)

# Save to CSV
df = pd.DataFrame(results)
df = df.sort_values(by="Total Score", ascending=False)
df.to_csv("outputs/scores.csv", index=False)
print("✅ Scores saved to outputs/scores.csv")
