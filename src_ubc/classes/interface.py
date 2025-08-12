from abc import ABC, abstractmethod

import torch
from PIL.Image import Image
from typing import Dict, List, Any, Optional, TypedDict, Any
from dataclasses import dataclass, asdict


class Query(TypedDict):
    """Query Data Structure"""

    content: str
    metadata: dict[str, Any]


@dataclass
class MergedResult:
    """Result After Merging Dense, Sparse, and Tag Results"""

    id: str
    content: str
    metadata: Dict[str, Any]
    sources: List[str]  # 记录来源：['dense', 'sparse']
    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    tag_score: Optional[float] = None
    final_score: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


# INTERFACES


class BaseEmbeddingModel(ABC):
    """Base class for embedding models"""

    def __init__(self, config: Optional[dict[str, Any]] = None):
        self.config = config or {}
        self.device = self.config.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )

    @abstractmethod
    def encode_text(self, texts: list[str]):
        """Generate embeddings for the given text"""
        ...

    # optional method for image embeddings
    def encode_image(self, images: list[str] | list[Image]):
        """Generate embeddings for the given images"""
        raise NotImplementedError("This model does not support image embeddings.")


class BaseComponent(ABC):
    """Base class for all components in the pipeline"""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}

    @abstractmethod
    def process(self, *args, **kwargs):
        """Process method to be implemented by subclasses"""
        ...


class QueryRewriter(BaseComponent):
    """Base class for query rewriters"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

    @abstractmethod
    def process(self, query: Query) -> list[Query]:
        """Rewrite the query"""
        ...


class Retriever(BaseComponent):
    """Base class for retrievers"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

    @abstractmethod
    def process(self, query: list[Query], **kwargs) -> list[MergedResult]:
        """Retrieve documents based on the query"""
        ...


class Reranker(BaseComponent):
    """Base class for rerankers"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

    @abstractmethod
    def process(
        self, query: Query, documents: list[MergedResult]
    ) -> list[MergedResult]:
        """Rerank the retrieved documents based on the query"""
        ...


class PromptBuilder(BaseComponent):
    """Base class for prompt builders"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

    @abstractmethod
    def process(
        self,
        query: Query,
        documents: list[MergedResult],
        conversations: Optional[list[dict]] = None,
    ) -> str:
        """Build a prompt based on the query and documents"""
        ...


class Generator(BaseComponent):
    """Base class for generators"""

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

    @abstractmethod
    def process(self, prompt: str) -> str:
        """Generate a response based on the prompt"""
        ...
