import json
from tour_generator import TourGuideGenerator
from survey import format_survey_context, Preferences
from query_rewritter import generate_human_query
from retriever import DefaultRetriever

def collect_survey() -> dict:
    print("📝 Museum Tour Survey\n")

    major = input("1. What is your major (as the tour guide)? ")
    age_group = input("2. What is the age group of the tour participants? ")
    class_subject = input("3. What is the class subject of the tour group? ")

    print("\n4. What are the group's topics of interest? (comma-separated)")
    print("   You can include themes, materials, regions, time periods, colors, and purposes")
    print("   Examples: symbolism, porcelain, blue, Qing, export\n")
    topics_of_interest = input("Topics of interest: ").split(",")

    exhibit_name = input("\n5. Which exhibit do you want to focus on? ")
    tour_length = int(input("6. How long is the tour (in minutes)? "))
    additional_notes = input("7. Any additional notes? (optional): ")

    return {
        "major": major.strip(),
        "age_group": age_group.strip(),
        "class_subject": class_subject.strip(),
        "topics_of_interest": [t.strip() for t in topics_of_interest],
        "exhibit_name": exhibit_name.strip(),
        "tour_length_minutes": tour_length,
        "additional_notes": additional_notes.strip()
    }

def parse_topics_to_preferences(topics: list[str]) -> Preferences:
    categories = {
        "materiality": ["porcelain", "stoneware", "silk", "bronze", "ceramics"],
        "region": ["china", "europe", "east asia", "jingdezhen"],
        "colour": ["blue", "cobalt", "white", "gold", "red"],
        "purpose": ["export", "ritual", "decoration", "daily use"],
        "themes": ["symbolism", "technique", "mythology", "nature"],
        "time_period": ["ming", "qing", "song", "yuan"]
    }

    fields = {key: [] for key in categories}
    additional_interests = []

    for topic in topics:
        topic_lower = topic.strip().lower()
        matched = False
        for key, values in categories.items():
            if topic_lower in values:
                fields[key].append(topic_lower)
                matched = True
                break
        if not matched:
            additional_interests.append(topic.strip())

    return Preferences(
        exhibits=[],  # Set later
        time_period=fields["time_period"],
        materiality=fields["materiality"],
        region=fields["region"],
        colour=fields["colour"],
        purpose=fields["purpose"],
        themes=fields["themes"],
        additional_interests=additional_interests
    )

def main():
    print("🎧 Welcome to the Museum Tour Generator")

    survey = collect_survey()

    survey_context = format_survey_context(survey)
    preferences = parse_topics_to_preferences(survey["topics_of_interest"])
    preferences.exhibits = [survey["exhibit_name"]]

    rewritten_query = generate_human_query(preferences)
    retriever = DefaultRetriever()
    relevant_chunks = retriever._retrieve_with_text(rewritten_query, preferences, k=5)  # returns {header: text}

    generator = TourGuideGenerator()

    print("\n🎟️ Generating Itinerary...")
    itinerary = generator.generate("itinerary", survey_context, relevant_chunks, survey_id="cli")
    print(json.dumps(itinerary, indent=2, ensure_ascii=False))

    print("\n🗣️ Generating Talking Points...")
    talking_points = generator.generate("talking_points", survey_context, relevant_chunks, survey_id="cli")
    print(json.dumps(talking_points, indent=2, ensure_ascii=False))

    print("\n🎨 Generating Engagement Tips...")
    engagement = generator.generate("engagement_tips", survey_context, relevant_chunks, survey_id="cli")
    print(json.dumps(engagement, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
