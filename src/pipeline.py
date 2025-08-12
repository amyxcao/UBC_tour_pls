from .interfaces import *
from typing_extensions import Any, Optional
from PIL import Image


class Pipeline:

    def __init__(
        self,
        query_rewriter: QueryRewriter,
        retriever: Retriever,
        reranker: Reranker,
        prompt_builder: PromptBuilder,
        generator: Generator,
        speaker: Speaker,
    ):
        self.query_rewriter = query_rewriter
        self.retriever = retriever
        self.reranker = reranker
        self.prompt_builder = prompt_builder
        self.generator = generator
        self.speaker = speaker

    def run(
        self, query: str, metadata: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        if metadata is None:
            if isinstance(query, Image.Image):
                metadata = {"type": "image"}
            else:
                metadata = {"type": "text"}

        # 1. create query object
        original_query = Query(content=query, metadata=metadata or {})

        # 2. rewrite query
        rewritten_queries = self.query_rewriter.process(original_query)

        # 3. retrieve
        documents = self.retriever.process(rewritten_queries)

        # 4. rerank
        ranked_documents = self.reranker.process(original_query, documents)

        # 5. build prompt
        prompt = self.prompt_builder.process(original_query, ranked_documents)

        # 6. generate answer
        answer = self.generator.process(prompt)

        # 7. speak answer if speaker is provided
        self.speaker.process(answer)

        return {
            "original_query": original_query["content"],
            "rewritten_queries": [q["content"] for q in rewritten_queries],
            "retrieved_documents": len(documents),
            "ranked_documents": [
                {"id": doc.id, "score": doc.final_score, "content": doc.content}
                for doc in ranked_documents
            ],
            "prompt": prompt[:50] + "...",
            "answer": answer,
        }
