def generate_human_query(user_interests: dict) -> str:
    query_parts = []
    base_phrase = "I am interested in museum artifacts"
    
    # 1. Handle time periods.
    if user_interests.get("time_periods"):
        periods_list = " and ".join(user_interests["time_periods"])
        query_parts.append(f"from the {periods_list} Dynasty periods")
    
    # 2. Handle art mediums and themes.
    art_details = []
    if user_interests.get("art_medium"):
        mediums_list = " and ".join(user_interests["art_medium"])
        art_details.append(mediums_list)
    if user_interests.get("themes"):
        themes_list = " and ".join(user_interests["themes"])
        art_details.append(themes_list)
    
    if art_details:
        query_parts.append("focusing on " + " and ".join(art_details))
        
    # 3. Handle keywords.
    if user_interests.get("keywords"):
        keywords_str = ", ".join(user_interests["keywords"])
        # Add connecting phrase based on previous parts.
        if query_parts:
            query_parts.append(f"and with interests in {keywords_str}")
        else:
            query_parts.append(f"with interests in {keywords_str}")
    
    # Combine all parts.
    if query_parts:
        final_query = f"{base_phrase} " + ", ".join(query_parts) + "."
    else:
        final_query = "I am looking for general museum artifacts."
    
    # Capitalize the first letter.
    return final_query[0].upper() + final_query[1:] if final_query else ""