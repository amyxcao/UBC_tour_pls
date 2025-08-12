from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SurveyResponse:
    def __init__(self, 
                 major: str, 
                 age_group: str, 
                 class_subject: str, 
                 exhibits: List[str], 
                 tour_length_minutes: int, 
                 time_period: List[str], 
                 materiality: List[str], 
                 region: List[str], 
                 colour: List[str],
                 purpose: List[str],
                 themes: List[str],
                 additional_interests: str,
                 additional_notes: str) -> None:
        self.major = major
        self.age_group = age_group
        self.class_subject = class_subject
        self.exhibits = exhibits
        self.tour_length_minutes = tour_length_minutes
        self.time_period = time_period
        self.materiality = materiality
        self.region = region
        self.colour = colour
        self.purpose = purpose
        self.themes = themes
        self.additional_interests = additional_interests
        self.additional_notes = additional_notes

@dataclass
class Preferences:
    exhibits: List[str]
    time_period: List[str]
    materiality: List[str]
    region: List[str]
    colour: List[str]
    purpose: List[str]
    themes: List[str]
    additional_interests: List[str]
        
    def count_preferences(self) -> int:
        total = 0
        for field, value in self.__dict__.items():
            if field == "additional_interests":
                continue  # skip this field
            if isinstance(value, list) and value:
                total += len(value)
        return total
    
def format_survey_context(survey: Dict[str, Any]) -> str:
    return f"""
This museum tour is for a volunteer guide majoring in {survey['major']}.
The audience is students aged {survey['age_group']} in a {survey['class_subject']} class.
The class is interested in: {", ".join(survey['topics_of_interest'])}.
Please focus on the following exhibit: {", ".join(survey['exhibit_name'])}.
The tour will be approximately {survey['tour_length_minutes']} minutes long.

Additional guide notes: {survey['additional_notes']}
""".strip()
