import os
import json
import csv
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_2"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_2"),
    api_version=os.getenv("AZURE_OPENAI_VERSION_2")
)
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_2")

# Paths
FOLDER = "./outputs"
CSV_FILE = "evaluation_results.csv"

FIELDS = [
    "ID",
    "TopicalAlignment",
    "AgeAppropriateness",
    "SubjectFit",
    "ToneMatch",
    "LengthAppropriateness",
    "Personalization",
    "Notes"
]

# Load the JSON file in the folder that starts with a certain prefix
def load_file_with_prefix(folder, prefix):
    for file in os.listdir(folder):
        if file.startswith(prefix) and file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"No file starting with {prefix} in {folder}")

# Evaluate the tour and extract ratings + comments
def evaluate_tour(folder_path: str, survey_id: str) -> list:
    survey = load_file_with_prefix(folder_path, "api_survey")
    talking_points = load_file_with_prefix(folder_path, "api_talking_points")
    itinerary = load_file_with_prefix(folder_path, "api_itinerary")
    engagement_tips = load_file_with_prefix(folder_path, "api_engagement_tips")

    prompt = f"""
You are evaluating a GPT-4-generated museum tour plan.

The output should reflect the user's preferences from the survey. In some cases, the surveys intentionally include unrealistic or extreme inputs — such as unusual tour guide majors (e.g., "cooking") or age groups (e.g., very young or very old). You should consider how well the response still tailors itself to these inputs, even if they are unusual.

Please rate the following on a scale of 1–5, and give a short explanation for each:

1. Topical Alignment — Does the content reflect the selected topics of interest?
2. Age Appropriateness — Is the language and activity design suitable for the specified age group?
3. Subject Fit — Is the output relevant to the chosen class subject (e.g., World History, Art)?
4. Tone Match — Does the tone align with the tour guide's intended style?
5. Length Appropriateness — Is the tour scaled to the length indicated in the survey?
6. Personalization — Does the output integrate other survey details like the guide's major or additional notes?

Even with unrealistic inputs, the system should still acknowledge them and adapt accordingly.

Respond in this format:

TopicalAlignment: <score> - <brief explanation>  
AgeAppropriateness: <score> - <brief explanation>  
SubjectFit: <score> - <brief explanation>  
ToneMatch: <score> - <brief explanation>  
LengthAppropriateness: <score> - <brief explanation>  
Personalization: <score> - <brief explanation>

---

User Survey:
{json.dumps(survey, indent=2)}

---

Generated Talking Points:
{json.dumps(talking_points, indent=2)}

---

Generated Itinerary:
{json.dumps(itinerary, indent=2)}

---

Generated Engagement Tips:
{json.dumps(engagement_tips, indent=2)}
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    print("\n--- GPT Response ---\n", text, "\n--- End ---\n")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    scores = [survey_id]
    comments = []

    for field in FIELDS[1:-1]:  # Skip ID and Notes
        field_clean = field.lower().replace("_", "").replace(" ", "")
        found = False

        for i, line in enumerate(lines):
            clean_line = re.sub(r"[^\w]", "", line.lower())
            if field_clean in clean_line and re.search(r"\d", clean_line):
                match = re.match(r".*?(\d)\s*[-–:]?\s*(.*)", line)
                if match:
                    score = int(match.group(1))
                    explanation = match.group(2).strip()

                    if not explanation and i + 1 < len(lines):
                        explanation = lines[i + 1].strip()
                    scores.append(score)
                    comments.append(explanation)
                    found = True
                    break

        if not found:
            print(f"⚠️ Field not matched: {field}")
            scores.append(None)
            comments.append("Missing")

    scores.append(" | ".join(comments))
    return scores

def main():
    with open(CSV_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(FIELDS)

        for folder_name in sorted(os.listdir(FOLDER), key=lambda x: int(x) if x.isdigit() else x):
            folder_path = os.path.join(FOLDER, folder_name)
            if not os.path.isdir(folder_path):
                continue

            try:
                print(f"Evaluating folder {folder_name}...")
                row = evaluate_tour(folder_path, folder_name)
                writer.writerow(row)
                print(f"✅ Saved results for folder {folder_name}")
            except Exception as e:
                print(f"❌ Failed on {folder_name}: {e}")

if __name__ == "__main__":
    main()
