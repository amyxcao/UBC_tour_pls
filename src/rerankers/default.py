from ..interfaces import Reranker, Query, MergedResult


class DefaultReranker(Reranker):
    """Default reranker that simply returns the documents as they are."""

    def __init__(self, config: dict = None):
        super().__init__(config)

    def process(
        self, query: Query, documents: list[MergedResult]
    ) -> list[MergedResult]:
        """Return the documents as they are."""
        return [document for document in documents if document.final_score > 0.5]
