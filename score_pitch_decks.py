import os
import pandas as pd
import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

input_folder = "outputs"
output_file = "outputs/score_table_nlp.csv"

# Scoring functions
def score_problem_clarity(text):
    return min(max((len(text.split()) / 100), 0), 10)

def score_market_potential(text):
    keywords = ["TAM", "market size", "billion", "million", "opportunity"]
    count = sum(text.lower().count(k.lower()) for k in keywords)
    return min(count, 10)

def score_traction(text):
    count = sum(1 for word in text.split() if "%" in word or "users" in word.lower() or "growth" in word.lower())
    return min(count, 10)

def score_team_strength(text):
    doc = nlp(text)
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return min(len(people), 10)

def score_business_model(text):
    keywords = ["SaaS", "subscription", "transaction", "licensing", "ads", "freemium"]
    return min(sum(text.lower().count(k.lower()) for k in keywords), 10)

def score_confidence_tone(text):
    sentiment = TextBlob(text).sentiment
    confidence = ((sentiment.polarity + (1 - sentiment.subjectivity)) / 2) * 10
    return round(confidence, 2)

# Process each deck
results = []
for file in os.listdir(input_folder):
    if file.endswith(".txt"):
        with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
            text = f.read()
        
        row = {
            "Startup": file.replace(".txt", ""),
            "Problem Clarity": score_problem_clarity(text),
            "Market Potential": score_market_potential(text),
            "Traction": score_traction(text),
            "Team Strength": score_team_strength(text),
            "Business Model": score_business_model(text),
            "Confidence / Tone": score_confidence_tone(text)
        }
        row["Total Score"] = round(sum(row[k] for k in row if k != "Startup"), 2)
        results.append(row)

# Save to CSV
df = pd.DataFrame(results).sort_values("Total Score", ascending=False)
df.to_csv(output_file, index=False)
print("✅ NLP-based scoring complete. Results saved to:", output_file)
