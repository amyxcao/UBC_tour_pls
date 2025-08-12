# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List

# from run_pipeline import format_survey_context, parse_topics_to_preferences
# from retriever import DefaultRetriever
# from tour_generator import TourGuideGenerator
# from query_rewritter import generate_human_query

# #uvicorn tour_api:app --reload


# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "src_ubc"))



# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:3000"] for stricter config
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class SurveyInput(BaseModel):
#     major: str
#     age_group: str
#     class_subject: str
#     topics_of_interest: List[str]
#     exhibit_name: str
#     tour_length_minutes: int
#     additional_notes: str = ""

# @app.post("/generate")
# def generate_outputs(survey: SurveyInput):
#     survey_dict = survey.dict()
#     print("🧪 Survey Dict:", survey_dict)

#     context = format_survey_context(survey_dict)
#     print("📄 Context:", context)

#     preferences = parse_topics_to_preferences(survey_dict["topics_of_interest"])
#     print("🎯 Preferences:", preferences)

#     preferences.exhibits = [survey_dict["exhibit_name"]]
    
#     rewritten_query = generate_human_query(preferences)
#     print("✏️ Rewritten Query:", rewritten_query)

#     retriever = DefaultRetriever()
#     relevant_chunks = retriever._retrieve_with_text(rewritten_query, preferences, k=5)
#     print("📚 Retrieved Chunks:", relevant_chunks)

#     generator = TourGuideGenerator()

#     return {
#         "itinerary": generator.generate(
#             "itinerary",
#             context,
#             relevant_chunks,
#             survey_id="api",
#             tour_length_minutes=survey_dict["tour_length_minutes"] 
#         ),
#         "talking_points": generator.generate(
#             prompt_type="talking_points",
#             context=context,
#             exhibit_chunks=relevant_chunks,
#             survey_id="api"
#         ),
#         "engagement_tips": generator.generate(
#             prompt_type="engagement_tips",
#             context=context,
#             exhibit_chunks=relevant_chunks,
#             survey_id="api"
#         )
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.run_pipeline import format_survey_context, parse_topics_to_preferences
from backend.retriever import DefaultRetriever
from backend.tour_generator import TourGuideGenerator
from backend.query_rewritter import generate_human_query

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src_ubc"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SurveyInput(BaseModel):
    major: str
    age_group: str
    class_subject: str
    topics_of_interest: List[str]
    exhibit_name: str
    tour_length_minutes: int
    additional_notes: str = ""

@app.post("/generate")
def generate_outputs(survey: SurveyInput):
    survey_dict = survey.dict()
    print("🧪 Survey Dict:", survey_dict)

    context = format_survey_context(survey_dict)
    print("📄 Context:", context)

    preferences = parse_topics_to_preferences(survey_dict["topics_of_interest"])
    print("🎯 Preferences:", preferences)

    preferences.exhibits = [survey_dict["exhibit_name"]]
    
    rewritten_query = generate_human_query(preferences)
    print("✏️ Rewritten Query:", rewritten_query)

    retriever = DefaultRetriever()
    relevant_chunks = retriever._retrieve_with_text(rewritten_query, preferences, k=5)
    print("📚 Retrieved Chunks:", relevant_chunks)

    generator = TourGuideGenerator()

    return {
        "itinerary": generator.generate(
            prompt_type="itinerary",
            context=context,
            exhibit_chunks=relevant_chunks,
            survey_id="api",
            major=survey_dict["major"],
            age_group=survey_dict["age_group"],
            class_subject=survey_dict["class_subject"],
            topics_of_interest=survey_dict["topics_of_interest"],
            exhibit_name=survey_dict["exhibit_name"],
            tour_length_minutes=survey_dict["tour_length_minutes"],
            additional_notes=survey_dict["additional_notes"]
        ),
        "talking_points": generator.generate(
            prompt_type="talking_points",
            context=context,
            exhibit_chunks=relevant_chunks,
            survey_id="api",
            major=survey_dict["major"],
            age_group=survey_dict["age_group"],
            class_subject=survey_dict["class_subject"],
            topics_of_interest=survey_dict["topics_of_interest"],
            exhibit_name=survey_dict["exhibit_name"],
            tour_length_minutes=survey_dict["tour_length_minutes"],
            additional_notes=survey_dict["additional_notes"]
        ),
        "engagement_tips": generator.generate(
            prompt_type="engagement_tips",
            context=context,
            exhibit_chunks=relevant_chunks,
            survey_id="api",
            major=survey_dict["major"],
            age_group=survey_dict["age_group"],
            class_subject=survey_dict["class_subject"],
            topics_of_interest=survey_dict["topics_of_interest"],
            exhibit_name=survey_dict["exhibit_name"],
            tour_length_minutes=survey_dict["tour_length_minutes"],
            additional_notes=survey_dict["additional_notes"]
        )
    }
