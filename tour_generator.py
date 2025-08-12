from dotenv import load_dotenv
import os
import re
import json
from datetime import datetime
from pathlib import Path
from openai import AzureOpenAI
from typing import List

load_dotenv()

class TourGuideGenerator:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY_2"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_2"),
            api_version=os.getenv("AZURE_OPENAI_VERSION_2")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_2")
        self.output_dir = "./outputs"

    def generate(
        self,
        prompt_type: str,
        context: str,
        exhibit_chunks: List[str],
        survey_id: str = "unknown",
        tour_length_minutes: int = None,
        major: str = "",
        age_group: str = "",
        class_subject: str = "",
        topics_of_interest: List[str] = [],
        exhibit_name: str = "",
        additional_notes: str = ""
    ) -> dict:
        if not isinstance(exhibit_chunks, list):
            raise TypeError("exhibit_chunks must be a list of strings")

        formatted_chunk = "\n\n".join(
            f"# Chunk {i+1}\n{chunk.strip()}" for i, chunk in enumerate(exhibit_chunks) if chunk.strip()
        )

        prompt = self.build_prompt(
            prompt_type,
            context,
            formatted_chunk,
            tour_length_minutes,
            major,
            age_group,
            class_subject,
            topics_of_interest,
            exhibit_name,
            additional_notes
        )

        temperature = {
            "talking_points": 0.3,
            "itinerary": 0.3,
            "engagement_tips": 0.7
        }.get(prompt_type, 0.3)

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )

        raw_response = response.choices[0].message.content.strip()
        raw_response = self._clean_json(raw_response)

        try:
            output_json = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON response. Saving raw output instead.")
            print("Error:", e)
            output_json = {"error": raw_response}

        # Save generated output
        filename = f"{survey_id}_{prompt_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(self.output_dir, exist_ok=True)
        save_path = os.path.join(self.output_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)

        print(f"✅ Output saved to: {save_path}")

        # ✅ Only save survey JSON once (during "talking_points" step)
        if prompt_type == "talking_points":
            survey_data = {
                "survey_id": survey_id,
                "tour_length_minutes": tour_length_minutes,
                "major": major,
                "age_group": age_group,
                "class_subject": class_subject,
                "topics_of_interest": topics_of_interest,
                "exhibit_name": exhibit_name,
                "additional_notes": additional_notes
            }

            survey_filename = f"{survey_id}_survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            survey_save_path = os.path.join(self.output_dir, survey_filename)
            with open(survey_save_path, "w", encoding="utf-8") as f:
                json.dump(survey_data, f, indent=2, ensure_ascii=False)

            print(f"📝 Survey saved to: {survey_save_path}")

        return output_json

    def _clean_json(self, raw: str) -> str:
        if raw.startswith("```json"):
            raw = raw[len("```json"):].strip()
        if raw.endswith("```"):
            raw = raw[:-len("```")].strip()
        raw = raw.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
        raw = re.sub(r",(\s*[}\]])", r"\1", raw)
        return raw

    def build_prompt(
        self,
        prompt_type: str,
        context: str,
        exhibit_chunk: str,
        tour_length_minutes: int = None,
        major: str = "",
        age_group: str = "",
        class_subject: str = "",
        topics_of_interest: List[str] = [],
        exhibit_name: str = "",
        additional_notes: str = ""
    ) -> str:
        base_prompt = f"""
# Role and Objective
You are a helpful assistant for museum tour planning. Your job is to generate content that helps a volunteer guide lead an educational and engaging tour based on exhibit materials and survey context.

# Instructions
- Read the tour context carefully
- Use details from the survey (such as tour guide's major, student age group, class subject, and interests)
- Tailor language and content based on the intended audience
- Prioritize clarity, cultural relevance, and hands-on engagement
""".strip()

        survey_info = f"""
# Survey Information
- Tour Guide Major: {major}
- Age Group: {age_group}
- Class Subject: {class_subject}
- Topics of Interest: {", ".join(topics_of_interest)}
- Exhibit Name: {exhibit_name}
- Tour Length: {tour_length_minutes} minutes
- Additional Notes: {additional_notes}
""".strip()

        if prompt_type == "talking_points":
            return base_prompt + "\n\n" + survey_info + f"""

# Talking Points Instructions
- Identify recurring themes across the exhibit
- Include technical details (symbolism, techniques, materials)
- Incorporate the tour guide’s academic background (major)
- Relate to the class subject and topics of interest
- Use bullet points with short headers
- Refer to specific artworks titles 

# Output Format
{{
  "themes": [
    {{
      "title": "Theme Title",
      "points": [
        "First bullet under this theme",
        "Second bullet under this theme"
      ]
    }}
  ]
}}

# Context
{context}

# Exhibit Chunk
{exhibit_chunk}
""".strip()

        elif prompt_type == "itinerary":
            return base_prompt + "\n\n" + survey_info + f"""

# Itinerary Instructions
Utilize the total tour duration of: {tour_length_minutes} minutes. Break the tour into sequential time blocks that are between 7 to 10 minutes long. Keep it brief with time for personal reflection of the tour guide. Minimal text.
Include:
1. Introduction
2. Context of the exhibit
3. Tour Guide’s personal reflection
4. Engagement activities
5. Wrap-up/conclusion

# Output Format
{{
  "itinerary": [
    {{ "time": "0:00–10:00", "activity": "Welcome and introduce the exhibit" }},
    {{ "time": "10:00–20:00", "activity": "Overview of the Qing Dynasty and symbolism" }}
  ]
}}

# Context
{context}

# Exhibit Chunk
{exhibit_chunk}
""".strip()

        elif prompt_type == "engagement_tips":
            return base_prompt + "\n\n" + survey_info + f"""

# Engagement Tips Instructions
- Make the tips age appropriate according to the age group
- Use the tour guide’s major, the age group, and any additional notes to guide tone and creativity
- Include at least one interactive activity 
- Focus on making the content fun, relevant, and educational

# Output Format
{{
  "tone_framing": ["Frame the tour as a treasure hunt"],
  "key_takeaways": ["Silk symbolized power in Qing dynasty"],
  "creative_activities": ["Design your own robe using meaningful colors"]
}}

# Context
{context}

# Exhibit Chunk
{exhibit_chunk}
""".strip()

        else:
            raise ValueError("❌ Invalid prompt type")
