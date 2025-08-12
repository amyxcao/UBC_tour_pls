import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

from datasets import Dataset as HFDataset
from ragas import evaluate, EvaluationDataset
from ragas.metrics import answer_relevancy, context_precision, context_recall

from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

load_dotenv()

azure_embeddings = AzureOpenAIEmbeddings(
    api_key=os.getenv("AZURE_OPENAI_KEY_2"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_2"),
    api_version=os.getenv("AZURE_OPENAI_VERSION_2"),
    deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    chunk_size=1000
)

llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_2"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_2"),
    api_version=os.getenv("AZURE_OPENAI_VERSION_2"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_2"),
    model_name="gpt-4",
    temperature=0,
)

def evaluate_talking_points(talking_points: dict, retrieved_contexts: list[str], survey: dict, survey_id: str):
    answer = "\n".join([
        f"### {theme['title']}\n" + "\n".join(f"- {pt}" for pt in theme["points"])
        for theme in talking_points["themes"]
    ])

    sample_dict = {
        "user_input": f"I am a volunteer tour guide majoring in {survey['major']}. What should I say about {', '.join(survey['topics_of_interest'])} in a {survey['exhibit_name']} exhibit for a {survey['class_subject']} class of {survey['age_group']} year olds?",
        "response": answer,
        "retrieved_contexts": retrieved_contexts,
        "reference": answer
    }

    hf_dataset = HFDataset.from_dict({k: [v] for k, v in sample_dict.items()})
    eval_dataset = EvaluationDataset.from_hf_dataset(hf_dataset)

    ragas_results = evaluate(
        eval_dataset,
        metrics=[
            answer_relevancy,
            context_precision,
            context_recall
        ],
        llm=llm,
        embeddings=azure_embeddings,
    )

    # Extra alignment check
    survey_prompt = f"""
You are a museum education expert.

Here is the survey from a volunteer tour guide:
{json.dumps(survey, indent=2)}

Below is the generated output for the guide’s tour. Please rate how well it reflects the survey intent on a scale of 1–5, and explain why.

--- OUTPUT ---
{answer}

Your evaluation:
"""

    survey_eval = llm.invoke(survey_prompt)

    return {
        "survey_id": survey_id,
        "type": "talking_points",
        "ragas": ragas_results.to_pandas().to_dict(orient="records"),
        "survey_alignment": survey_eval.content.strip(),
        "timestamp": datetime.now().isoformat()
    }