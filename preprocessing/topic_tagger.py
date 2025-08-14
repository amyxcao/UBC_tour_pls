import json
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import re

TIME_PERIOD_TAGS = [
    "tang", "song", "yuan", "ming", "qing"
]

MATERIALITY_TAGS = [
    "earthenware", "porcelain", "stoneware", "ceramics", "clay", "firing", "temperature", "kilns"
]

REGION_TAGS = [
    "longquan_kilns", "jingdezhen_kilns", "jizhou_kilns", "dehua",
    "southeast_asia", "east_asia", "europe"
]

COLOUR_TAGS = [
    "celadon", "green", "sancai", "three_colour", "wucai", "five_colour", "iron", "blue", "cobalt", "yellow", "white_porcelain", "blanc_de_chine"
]

PURPOSE_TAGS = [
    "court", "imperial", "ritual", "decoration", 
    "functional", "curiosities", "commission", "export", "import"
]

THEME_TAGS = [
    "symbolism", "technique", "mythical", "landscapes", 
    "nature", "religious"
]

INSTRUCTIONS = "(Select all relevant tags or leave bank)"

def create_prompt(text, header):
    return f"""
    You are a museum content classifier. Based on the exhibit description below, assign the most appropriate value(s) for each of the following categories.

    Choose one or more tags from the **provided tag lists only**. If no relevant tag applies, leave the field blank. Do not invent or modify tags under any circumstances.

    Some very short (<50 words) entries may be incomplete or administrative. In such cases, **leave all tag fields**.

    Use the following definitions when determining ceramic materiality:
    - **Ci (瓷):** Chinese term for high-fired ceramics including both porcelain and stoneware.
    - **Porcelain:** White, translucent ceramics from kaolin clay, fired at ~1300°C.
    - **Stoneware:** Dense ceramics from gray/brown clay, 1000–1250°C, opaque.
    - **Earthenware:** Low-fired ceramics (<1000°C); porous and less durable.

    ---
    **Header**: {header}
    **Text**: {text}

    ---

    **Time Period** {INSTRUCTIONS}:  
    {json.dumps(TIME_PERIOD_TAGS)}

    **Materiality** {INSTRUCTIONS}:  
    {json.dumps(MATERIALITY_TAGS)}

    **Region of Origin** {INSTRUCTIONS}:  
    {json.dumps(REGION_TAGS)}

    **Colour** {INSTRUCTIONS}:  
    {json.dumps(COLOUR_TAGS)}

    **Purpose** {INSTRUCTIONS}:  
    {json.dumps(PURPOSE_TAGS)}

    **Themes** {INSTRUCTIONS}:  
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
    "type": ["TypeTagHere"]
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

def tag_chunk(text, header, seed, temp):
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
        model=os.environ.get("AZURE_OPENAI_DEPLOYEMENT", "gpt-4o"),
        stream=True,
        seed=seed, 
        temperature=temp
    )

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

def topic_tagger(input_file, output_dir=None, seed=123, temp=0):
    """_summary_

    Args:
        input_file (_type_): _description_
        output_dir (_type_, optional): _description_. Defaults to None.
    """

    with open(input_file, "r") as f:
        data = json.load(f)
    
    if output_dir is None:
        output_file = input_file  
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, os.path.basename(input_file))

        
    for item in data.values(): 
        chunk_text_list = item.get('text', '')
        chunk_text = " ".join(chunk_text_list)
        header = item.get('header', '')
        llm_tags = tag_chunk(chunk_text, header, seed, temp)
        
        # update tags in JSON
        item['time_period'] = llm_tags.get('time_period', [])
        item['materiality'] = llm_tags.get('materiality', [])
        item['region'] = llm_tags.get('region', [])
        item['colour'] = llm_tags.get('colour', [])
        item['purpose'] = llm_tags.get('purpose', [])
        item['themes'] = llm_tags.get('themes', [])
        # item['explanation'] = llm_tags.get('explanation', '')
    
    # Extract base name
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create output file name with suffix
    output_filename = f"{base_name}_seed{seed}_temp{temp}.json"

    if output_dir is None:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, output_filename)
    
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print("Completed tagging for", input_file)
    print("Saved output to", output_file)