from typing_extensions import Any


def recall_at_k(k=5):
    """A function that returns a metric function to calculate recall at k."""

    def recall_at_k_score(
        reference_context: list[str], retrieved_context: list[str]
    ) -> float:
        """A metric function to calculate recall at k.
        - Args:
            reference_context (list[str]): The ground truth context.
            retrieved_context (list[str]): The retrieved context.
        - Returns:
            float: The recall at k score.

        - Example:
            >>> reference_context = ["doc1", "doc2", "doc3"]
            >>> retrieved_context = ["doc1", "doc4", "doc5"]
            >>> recall_at_k_score(reference_context, retrieved_context)
            0.3333
        """
        retrieved_set = set(retrieved_context[:k])
        reference_set = set(reference_context)

        # calculate recall value
        score = (
            len(retrieved_set.intersection(reference_set)) / len(reference_set)
            if reference_set
            else 0.0
        )
        return score

    return recall_at_k_score
