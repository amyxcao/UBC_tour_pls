import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_2"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_2"),
    api_version=os.getenv("AZURE_OPENAI_VERSION_2")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_2")

def evaluate_engagement(output: dict, survey: dict, survey_id: str) -> dict:
    prompt = f"""
You are evaluating engagement tips for a museum tour for {survey['age_group']} year olds interested in {', '.join(survey['topics_of_interest'])}.

--- Tone & Framing ---
{'; '.join(output.get('tone_framing', []))}

--- Key Takeaways ---
{'; '.join(output.get('key_takeaways', []))}

--- Creative Activities ---
{'; '.join(output.get('creative_activities', []))}

Score from 1 to 5 and provide a brief justification for each of the following criteria:
1. Creativity
2. Relevance to the exhibit
3. Appropriateness for age group

Respond in JSON:
{{"creativity": ..., "relevance": ..., "age_fit": ...}}
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()
    result = {
        "survey_id": survey_id,
        "type": "engagement",
        "scores": content,
        "timestamp": datetime.now().isoformat()
    }
    return result