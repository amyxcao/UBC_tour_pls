from classes import *
from query_rewritter import *
from retriever import DefaultRetriever
from survey import Preferences, SurveyResponse


def main():
    # Example usage of the SurveyResponse class
    response = SurveyResponse(
        major="Computer Science",
        age_group="18-24",
        class_subject="Introduction to AI",
        exhibits=["Exhibit A", "Exhibit B"],
        tour_length_minutes=60,
        time_period=["qing"],
        materiality=["cermanics"],
        themes=[],
        additional_interests=["auspicious symbolism"],
        region=["east asia"],
        colour=["iron"],
        purpose=[""],
        additional_notes=["rare artifacts"],
    )

    preferences = Preferences(
        exhibits=response.exhibits,
        time_period=response.time_period,
        materiality=response.materiality,
        region=response.region,
        colour=response.colour,
        purpose=response.purpose,
        themes=response.themes,
        additional_interests=response.additional_interests,
    )

    query = generate_human_query(preferences)
    retriever = DefaultRetriever()
    results = retriever._retrieve_with_text(query, preferences, k=5)
    print(results)


if __name__ == "__main__":
    main()
