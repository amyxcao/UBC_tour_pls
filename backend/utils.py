# from classes.survey import Preferences
# from typing import Dict

# def get_number_tag_matches(tags: Preferences, hit: Dict) -> float:
#         """
#         Get the number of tag matches based on how many of the user's tags match the hit's metadata.
        
#         Args:
#             tags: A Preferences object with attributes:
#                 - time_period: List[str]
#                 - themes: List[str]
#                 - exhibits: List[str]
#                 - art_medium: List[str]
#                 - additional_interests: List[str]
#             hit: A dictionary representing a search result hit.
            
#         Returns:
#             A float score representing the number of matching tags.
#         """
#         score = 0
#         for key in tags.__dict__.keys():
#             if key in hit['metadata']:
#                 matches = set(hit['metadata'][key]) & set(getattr(tags, key))
#                 score += len(matches)
#         return score

import json
from backend.survey import Preferences
from typing import Dict

def load_json_file(filepath):
    """Load and return JSON data from a given file path."""
    with open(filepath, 'r') as f:
        return json.load(f)

def get_number_tag_matches(tags: Preferences, hit: Dict) -> float:
    """
    Get the number of tag matches between the user's preferences and a search result hit's metadata.

    Args:
        tags: A Preferences object with attributes like time_period, themes, exhibits, etc.
        hit: A dictionary representing a search result hit with metadata.

    Returns:
        A float score representing the number of matching tags.
    """
    score = 0
    for key in tags.__dict__.keys():
        if key in hit['metadata']:
            matches = set(hit['metadata'][key]) & set(getattr(tags, key))
            score += len(matches)
    return score
