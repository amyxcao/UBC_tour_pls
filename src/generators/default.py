from ..interfaces import Generator
from openai import AzureOpenAI
from typing_extensions import Iterator, Optional
import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class DefaultGenerator(Generator):
    """Default generator that simply returns the prompt as the response."""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        self.client = AzureOpenAI(
            api_version=os.environ.get("API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.environ.get(
                "AZURE_OPENAI_ENDPOINT", "https://openai-ai-museum.openai.azure.com/"
            ),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        )

    def process(self, prompt: str) -> Iterator[str]:
        """Return the prompt as the response."""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=16384,
                model=os.environ.get(
                    "AZURE_OPENAI_DEPLOYEMENT", "gpt-4o"
                ),  # Default to gpt-4o if not specified
                stream=True,
            )

            sentence_buffer = ""
            sentence_endings = re.compile(r"[.!?。！？;；]+")

            for chunk in response:
                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content
                if not content:
                    continue

                sentence_buffer += content

                # 检查是否包含句子结束符
                if sentence_endings.search(sentence_buffer):
                    # 按句子结束符分割文本
                    sentences = sentence_endings.split(sentence_buffer)

                    # 除了最后一个片段，其他都是完整的句子
                    for i in range(len(sentences) - 1):
                        sentence = sentences[i].strip()
                        if sentence:  # 避免空句子
                            # 找到对应的结束符并添加回去
                            ending_match = list(
                                sentence_endings.finditer(sentence_buffer)
                            )
                            if i < len(ending_match):
                                sentence += ending_match[i].group()
                            yield sentence

                    # keep the remaining part in the buffer
                    sentence_buffer = sentences[-1].strip() if sentences else ""

            # processing the remaining part in the buffer
            if sentence_buffer:
                yield sentence_buffer
        except Exception as e:
            print(f"Error generating response: {e}")
            yield "An error occurred while generating the response."
