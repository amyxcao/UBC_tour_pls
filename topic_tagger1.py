import json
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import re

TIME_PERIOD_TAGS = [
    "tang", "song", "yuan", "ming", "qing"
]

MATERIALITY_TAGS = [
    "earthenware", "porcelain", "stoneware"
]

REGION_TAGS = [
    "longquan_kilns", "jingdezhen_kilns", "jizhou_kilns", "dehua",
    "southeast_asia", "east_asia", "europe"
]

COLOUR_TAGS = [
    "celadon", "green", "sancai/three_colour", "wucai/five_colour", "iron", "blue/cobalt", "yellow", "white_porcelain/blanc_de_chine"
]

PURPOSE_TAGS = [
    "court", "imperial", "ritual", "decoration", 
    "functional", "curiosities", "commission", "export", "import"
]

THEME_TAGS = [
    "symbolism", "technique", "mythical", "landscapes", 
    "nature", "religious"
]

INSTRUCTIONS = "Select one or more relevant tags, or leave it blank"

def create_prompt(text, header):
    return f"""
    You are a museum content classifier. Based on the exhibit description below, assign the most appropriate value(s) for each of the following categories. 

    Choose one or more tags from the **provided tag lists only**. If no relevant tag applies, leave the field blank. Do not invent or modify tags under any circumstances.

    For each selected tag, include a concise explanation referencing specific details from the exhibit description that justify your choice. If no tags are selected, leave the explanation field blank.

    Some very short (<50 words) entries may be incomplete or administrative, such as a title page or staff listing (e.g., “Florian Knothe Research Assistant and Translator Kikki Lam”). In such cases, **leave all tag fields and the explanation blank**.

    Use the following definitions when determining ceramic materiality:

    - **Ci (瓷):** A Chinese term for all high-fired ceramics, including both porcelain and stoneware.
    - **Porcelain (Western definition):** White, translucent ceramics made from kaolin clay, fired at ~1300°C, producing a glassy, ringing material.
    - **Stoneware:** Dense, hard ceramics made from gray or brown clay, fired at 1000–1250°C. Typically opaque and not white-bodied.
    - **Earthenware:** Low-fired ceramics (below 1000°C); porous and less durable.

    ---

    **Header**: {header}  
    **Text**: {text}

    ---

    **Time Period** (choose from):  
    {json.dumps(TIME_PERIOD_TAGS)}

    **Materiality** (choose from):  
    {json.dumps(MATERIALITY_TAGS)}

    **Region of Origin** (choose from):  
    {json.dumps(REGION_TAGS)}

    **Colour** (choose from):  
    {json.dumps(COLOUR_TAGS)}

    **Purpose** (choose from):  
    {json.dumps(PURPOSE_TAGS)}

    **Themes** (choose from):  
    {json.dumps(THEME_TAGS)}

    ---

    Respond with JSON in this format:
    {{
    "time_period": ["TimePeriodTagHere"],
    "materiality": ["MaterialityTagHere"],
    "region": ["RegionTagHere"],
    "colour": ["ColourTagHere"],
    "purpose": ["PurposeTagHere"],
    "themes": ["ThemeTagHere"],
    "type": ["TypeTagHere"],
    "explanation": "Provide a brief explanation for the selected tags, referencing specific text details. Leave this field blank if no tags are selected."
    }}
    """


def clean_json_string(s: str) -> str:
    # Remove markdown code fences and language specifiers
    s = s.strip()
    if s.startswith("```"):
        # Remove starting and ending fence.
        s = s.lstrip("`").rstrip("`").strip()
        # Remove language specifier if it exists (e.g. "json")
        s = re.sub(r"^json\s*", "", s, flags=re.IGNORECASE)
    return s

def tag_chunk(text, header):
    prompt = create_prompt(text, header)
    client = AzureOpenAI(
        api_version=os.environ.get("API_VERSION", "2024-12-01-preview"),
        azure_endpoint=os.environ.get(
            "AZURE_OPENAI_ENDPOINT", "https://openai-ai-museum.openai.azure.com/"
        ),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=16384,
        temperature=0,
        model=os.environ.get("AZURE_OPENAI_DEPLOYEMENT", "gpt-4o"),
        stream=True,
        seed=125
    )

    # Collect streamed content
    collected_response = ""
    for chunk in response:
        if chunk.choices:
            delta = chunk.choices[0].delta
            collected_response += delta.content if hasattr(delta, "content") and delta.content is not None else ""
    
    # Clean the response from markdown formatting
    clean_response = clean_json_string(collected_response)
    
    try:
        return json.loads(clean_response)
    except json.JSONDecodeError:
        print("Could not decode JSON:", clean_response)
        return {}

def topic_tagger(input_file, output_dir=None):
    """_summary_

    Args:
        input_file (_type_): _description_
        output_dir (_type_, optional): _description_. Defaults to None.
    """
    # Load chunked JSON
    with open(input_file, "r") as f:
        data = json.load(f)
    
    if output_dir is None:
        output_file = input_file  # Overwrite input file if no output directory specified.
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, os.path.basename(input_file))

        
    for item in data.values(): 
        chunk_text_list = item.get('text', '')
        chunk_text = " ".join(chunk_text_list)
        header = item.get('header', '')
        llm_tags = tag_chunk(chunk_text, header)
        
        # update tags in JSON
        item['time_period'] = llm_tags.get('time_period', [])
        item['materiality'] = llm_tags.get('materiality', [])
        item['region'] = llm_tags.get('region', [])
        item['colour'] = llm_tags.get('colour', [])
        item['purpose'] = llm_tags.get('purpose', [])
        item['themes'] = llm_tags.get('themes', [])
        item['explanation'] = llm_tags.get('explanation', '')
        
    print("completed tagging for", input_file)
    # Save updated JSON
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)