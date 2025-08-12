prompt = """You are an expert question generator for information retrieval systems. Your task is to create questions that can be **directly answered** using information from specific text chunks. 

### Input
- A list of text chunks from a document (each chunk is a string)
- Chunks are provided in order

### Instructions
1. **Answerability**: Each question MUST be answerable using EXACTLY these text chunks.
2. **Chunk Coverage**:
   - Generate {question_num} questions
   - Prioritize chunks with substantive information
   - Skip chunks with no meaningful content (e.g., formatting elements)
3. **Question Quality**:
   - Questions should be clear, concise, and self-contained
   - Cover key entities, facts, and concepts in the chunk
   - Include diverse question types (what, why, how, who, when)
4. **Output Format**: 
   ```json
   [
       \"question_1\",
       \"question_2\",
       ...
       \"question_n\"
   ]
   ```

text_chunks (for reference):
---
{reference_context}
---
"""

import os
import re
import json
import random
from openai import AzureOpenAI


class DatasetCreater:
    def __init__(self):
        self.dataset_name = "default"
        self.data_path = None

        self.client = AzureOpenAI(
            api_version=os.environ.get("API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.environ.get(
                "AZURE_OPENAI_ENDPOINT", "https://openai-ai-museum.openai.azure.com/"
            ),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        )
        self.prompt = prompt

    def _generate_questions(self, reference_context: list[str], question_num=5):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(
                        question_num=question_num, reference_context=reference_context
                    ),
                }
            ],
            max_tokens=16384,
            model=os.environ.get("AZURE_OPENAI_DEPLOYEMENT", "gpt-4o"),
        )

        return self._extract_json(response.choices[0].message.content)

    def _extract_json(self, text):
        if not text:
            return None
        match = re.search(r"```json\s*([\s\S]+?)\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = text
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None

    def _sample_reference_context(self, data_path, reference_num=1, section_id=None):
        with open(data_path, "r") as f:
            contents = json.load(f)

        section_ids = list(contents.keys())
        if section_id is None:
            section_id = random.choice(section_ids)

        section = contents[section_id]
        chunks = []
        for content in section:
            if "text" in content:
                text = content["text"]
                if text.strip():
                    chunks.append(text.strip())

        start_idx = random.randint(0, max(len(chunks) - reference_num, 0))
        reference_context = chunks[start_idx : start_idx + reference_num]
        return reference_context

    def create(
        self,
        dataset_name,
        data_path,
        reference_num=5,
        question_num=10,
        output_path=None,
    ):
        self.dataset_name = dataset_name
        self.data_path = data_path

        dataset = {
            "dataset_name": self.dataset_name,
            "data_path": self.data_path,
            "data": [],
        }
        reference_context = self._sample_reference_context(
            data_path, reference_num=reference_num
        )
        questions = self._generate_questions(
            reference_context, question_num=question_num
        )

        if not questions:
            print("No questions generated. Exiting.")
            return dataset

        for i, question in enumerate(questions):
            dataset["data"].append(
                {
                    "question": question,
                    "reference_context": reference_context,
                }
            )

        # Save the dataset to a file if output_path is provided
        if output_path:
            with open(output_path, "w") as f:
                json.dump(dataset, f, indent=4)
            print(f"Dataset saved to {output_path}")

        return dataset
