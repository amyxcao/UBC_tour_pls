import os

import numpy as np
from dotenv import find_dotenv, load_dotenv  # 3P
from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
from pinecone import (
    Pinecone,  # 3P
    ServerlessSpec,
)
from pinecone_text.sparse import BM25Encoder

from survey import (
    Preferences,  # or: from src_ubc.survey import Preferences
)
from utils import get_number_tag_matches  # (better: import only what you need)

load_dotenv(find_dotenv())


class DefaultRetriever:
    def __init__(self):
        index_name = "umag-hybrid-search"
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY_UBC"))
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=3072,  # dimensionality of dense model
                metric="dotproduct",  # sparse values supported only for dotproduct
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        index = pc.Index(index_name)

        bm25_encoder = BM25Encoder.default()

        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
            azure_endpoint=os.environ["AZURE_OPENAI_EMBEDDING_ENDPOINT"],
        )
        # Initialize Pinecone client or any other necessary components here
        self.retriever = PineconeHybridSearchRetriever(
            embeddings=embeddings, sparse_encoder=bm25_encoder, index=index, top_k=100
        )

    def _search_tags(self, tags: Preferences, top_k=100):
        """
        Perform a metadata search based on the provided Preferences object.

        Args:
            tags: A Preferences object with attributes:
                - time_period: List[str]
                - themes: List[str]
                - exhibits: List[str]
                - art_medium: List[str]
                - additional_interests: List[str]
            top_k: Number of results to return.

        Returns:
            List of matching documents from dense_db.
        """
        # Convert the Preferences object to a dictionary.
        tag_dict = tags.__dict__

        # Remove any keys with empty lists.
        tag_dict = {k: v for k, v in tag_dict.items() if v}

        # Dummy vector for metadata filtering (using the dimensions expected by your dense index)
        dummy_vector = np.zeros(3072).tolist()

        # Build metadata filter conditions. Each condition looks for documents where a given field contains at least one of the values.
        filter_conditions = []
        for key, values in tag_dict.items():
            filter_conditions.append({key: {"$in": values}})

        # Use $or operator so that if any condition matches the document is returned
        metadata_filter = {"$or": filter_conditions} if filter_conditions else {}

        # Perform the semantic search using the dummy vector and only filter by metadata.
        response = self.retriever.index.query(
            vector=dummy_vector,
            top_k=top_k,
            include_metadata=True,
            filter=metadata_filter,
        )

        for i in range(len(response.matches)):
            # normalize the score based on the number of preferences
            response.matches[i]["score"] = (
                get_number_tag_matches(tags, response.matches[i])
                / tags.count_preferences()
            )

        # sort matches by tag score
        response.matches.sort(key=lambda match: match["score"], reverse=True)

        final_result = []
        for res in response["matches"]:
            context = res["metadata"].pop("context")
            metadata = res["metadata"]
            if "score" not in metadata and "score" in res:
                metadata["score"] = res["score"]
            final_result.append(Document(page_content=context, metadata=metadata))

        return final_result

    def _retrieve_with_text(
        self,
        query: str,
        tags: Preferences,
        k=20,
    ):
        db_size = self.retriever.index.describe_index_stats()["namespaces"][""][
            "vector_count"
        ]

        tag_results = self._search_tags(tags, top_k=db_size)
        db_results = self.retriever.invoke(query)

        tag_contents = [d.page_content for d in tag_results]
        db_contents = [d.page_content for d in db_results]

        # Extract only text from the top k results
        relevant_content = set(tag_contents)
        relevant_content.update(set(db_contents))

        return list(relevant_content)
