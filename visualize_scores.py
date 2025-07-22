import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the scores
df = pd.read_csv("outputs/scores.csv")

# Sort by score
df = df.sort_values("Total Score", ascending=False)

# Set the plot style
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Plot
barplot = sns.barplot(
    x="Total Score",
    y="Startup",
    data=df,
    palette="viridis"
)

# Add labels
for i, v in enumerate(df["Total Score"]):
    barplot.text(v + 0.5, i, str(v), color='black', va="center")

plt.title("Startup Pitch Deck Scores")
plt.xlabel("Total Score (out of 60)")
plt.ylabel("Startup")
plt.tight_layout()

# Save plot
os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/bar_chart_scores.png")
plt.show()

print("✅ Chart saved as outputs/bar_chart_scores.png")
