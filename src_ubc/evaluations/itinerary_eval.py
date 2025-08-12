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

def evaluate_itinerary(output: dict, survey: dict, survey_id: str) -> dict:
    formatted = "\n".join([f"{block['time']}: {block['activity']}" for block in output.get("itinerary", [])])
    
    prompt = f"""
You are a museum tour evaluator.

Tour context:
- Audience: {survey['age_group']} year olds
- Class: {survey['class_subject']}
- Interests: {', '.join(survey['topics_of_interest'])}
- Tour length: {survey['tour_length_minutes']} minutes

Evaluate the following itinerary: 
{formatted}

Score from 1 to 5:
1. Structure and logical flow
2. Fit for pacing
3. Relevance to age and topic
4. Clarity for kids

Respond in JSON:
{{"structure": ..., "timing": ..., "relevance": ..., "clarity": ...}}
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()
    result = {
        "survey_id": survey_id,
        "type": "itinerary",
        "scores": content,
        "timestamp": datetime.now().isoformat()
    }
    return result
