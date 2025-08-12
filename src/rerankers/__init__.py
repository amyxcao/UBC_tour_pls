from ..interfaces import Reranker


class DefaultReranker(Reranker):
    """Default reranker that simply returns the documents as they are."""

    def __init__(self, config: dict = None):
        super().__init__(config)

    def process(self, documents: list[dict]) -> list[dict]:
        """Return the documents as they are."""
        return documents
