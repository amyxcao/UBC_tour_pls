from ..interfaces import PromptBuilder, MergedResult


class DefaultPromptBuilder(PromptBuilder):
    """Default prompt builder that simply returns the query text as the prompt."""

    def __init__(self, config: dict = None):
        super().__init__(config)

    def process(
        self,
        query_text: str,
        documents: list[MergedResult],
        conversations: list[dict] = None,
    ) -> str:
        """Return the query text as the prompt."""
        prompt = open(
            r"D:\HKU\Inno Wing RA\UBC Exchange\code\src\prompt_builders\prompt.txt", "r"
        ).read()
        prompt = prompt.format(
            user_query=query_text,
            retrieved_documents=self._format_documents(documents),
            history_conversation=self._format_conversations(
                conversations
            ),  # Assuming no chat history for this example
        )
        return prompt

    def _format_documents(self, documents: list[MergedResult]) -> str:
        """Format the retrieved documents into a string."""
        return (
            "\n".join(
                f"Document {i + 1}: {doc.content}" for i, doc in enumerate(documents)
            )
            if documents
            else "No documents retrieved."
        )

    def _format_conversations(self, conversations: list[dict]) -> str:
        """Format the conversation history into a string."""
        return (
            "\n".join(f"{conv['role']}: {conv['content']}" for conv in conversations)
            if conversations
            else "No conversation history."
        )
