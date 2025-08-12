from pinecone import Pinecone  # 3P
from dotenv import load_dotenv, find_dotenv  # 3P
import os
import numpy as np
from typing import Dict
from collections import defaultdict

from backend.interfaces import Retriever, Query, MergedResult
from backend.embeddings import DefaultDenseEmbeddingModel, DefaultSparseEmbeddingModel
from backend.survey import Preferences            # or: from backend.src_ubc.survey import Preferences
from backend.utils import *                       # (better: import only what you need)

load_dotenv(find_dotenv())


class DefaultRetriever(Retriever):
    def __init__(self, config: dict = None):
        super().__init__(config)
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY_UBC", ""))
        # Initialize Pinecone client or any other necessary components here
        self.dense_db = pc.Index("museum-ai-dense")
        self.sparse_db = pc.Index("museum-ai-sparse")
        self.dense_embedding_model = DefaultDenseEmbeddingModel({})
        self.sparse_embedding_model = DefaultSparseEmbeddingModel({})

    def process(self, query: str, k=20, dense_weight=.2, sparse_weight=.8) -> list[dict]:
        results = self._retrieve_with_text(query, dense_weight, sparse_weight, k)
        return results

    # DO NOT NEED
    def _retrieve_parent_documents(self, results: list[dict], query: Query, k: int = 5):
        section_id_freqency = {}
        for result in results:
            section_id = result["metadata"].get("section_id")
            if section_id:
                section_id_freqency[section_id] = (
                    section_id_freqency.get(section_id, 0) + 1
                )
        # Sort section IDs by frequency
        sorted_section_ids = sorted(
            section_id_freqency.items(), key=lambda x: x[1], reverse=True
        )
        # Retrieve top k section IDs
        top_section_ids = [section_id for section_id, _ in sorted_section_ids[:k]]
        section_results = []
        for section_id in top_section_ids:
            section_results.extend(self._retrieve_by_section_id(section_id))


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
        dummy_vector = np.zeros(512).tolist()

        # Build metadata filter conditions. Each condition looks for documents where a given field contains at least one of the values.
        filter_conditions = []
        for key, values in tag_dict.items():
            filter_conditions.append({key: {"$in": values}})
        
        # Use $or operator so that if any condition matches the document is returned
        metadata_filter = {"$or": filter_conditions} if filter_conditions else {}

        # Perform the semantic search using the dummy vector and only filter by metadata.
        response = self.dense_db.query(
            namespace="umag",
            vector=dummy_vector,
            top_k=top_k,
            include_metadata=True,
            filter=metadata_filter
        )
        
        for i in range(len(response.matches)):
            # normalize the score based on the number of preferences
            response.matches[i]['score'] = get_number_tag_matches(tags, response.matches[i]) / tags.count_preferences()
                
        # sort matches by tag score
        response.matches.sort(key=lambda match: match['score'], reverse=True)
        return response.matches
    
    def _rrf_merge(self, dense_results, sparse_results, tag_results, dense_weight=.3, sparse_weight=.2, tag_weight=.5, k=60):
        def rank_dict(results):
            return {doc['id']: rank for rank, doc in enumerate(results)}

        # Create rank mappings
        dense_ranks = rank_dict(dense_results)
        sparse_ranks = rank_dict(sparse_results)
        tag_ranks = rank_dict(tag_results)

        # Create lookup for original docs and scores
        id_to_doc = {}
        dense_scores = {doc['id']: doc.get('score', 0) for doc in dense_results}
        sparse_scores = {doc['id']: doc.get('score', 0) for doc in sparse_results}
        tag_scores = {doc['id']: doc.get('score', 0) for doc in tag_results}

        for result_set in [sparse_results, dense_results, tag_results]:
            for doc in result_set:
                if doc['id'] not in id_to_doc:
                    id_to_doc[doc['id']] = doc

        merged = {}

        # Merge all IDs
        all_ids = set(sparse_ranks) | set(dense_ranks) | set(tag_ranks)
        for id_ in all_ids:
            sparse_rank = sparse_ranks.get(id_)
            dense_rank = dense_ranks.get(id_)
            tag_rank = tag_ranks.get(id_)

            sparse_score_rrf = 1 / (k + sparse_rank) if sparse_rank is not None else 0
            dense_score_rrf = 1 / (k + dense_rank) if dense_rank is not None else 0
            tag_score_rrf = 1 / (k + tag_rank) if tag_rank is not None else 0

            final_score = sparse_score_rrf*sparse_weight + dense_score_rrf*dense_weight + tag_score_rrf*tag_weight

            base_doc = id_to_doc[id_]
            merged[id_] = {
                'id': id_,
                'metadata': base_doc.get('metadata', {}),
                'original_sparse_score': sparse_scores.get(id_, 0),
                'original_dense_score': dense_scores.get(id_, 0),
                'original_tag_score': tag_scores.get(id_, 0),
                'sparse_rrf_score': sparse_score_rrf,
                'dense_rrf_score': dense_score_rrf,
                'tag_rrf_score': tag_score_rrf,
                'final_score': final_score,
                'sparse_rank': sparse_rank,
                'dense_rank': dense_rank,
                'tag_rank': tag_rank,
            }

        return sorted(merged.values(), key=lambda x: x['final_score'], reverse=True)

    def _retrieve_with_text(self, query: str, tags: Preferences, dense_weight=.25, sparse_weight=.25, tag_weight=.5, k=20) -> list[dict]:
        db_size = self.dense_db.describe_index_stats(namespace="umag")['namespaces']['umag']['vector_count']
        tag_results = self._search_tags(tags, top_k=db_size)
   
        # if there are no additional interests, only use tag results
        if len(tags.additional_interests) != 0:
            dense_results = self.dense_db.query(
                namespace="umag",
                top_k=50,
                include_values=False,
                include_metadata=True,
                vector=self.dense_embedding_model.encode_text([query])[0],
            ).matches
            
            sparse_results = self.sparse_db.query(
                namespace="umag",
                top_k=50,
                include_values=True,
                include_metadata=True,
                sparse_vector=self.sparse_embedding_model.encode_text([query])[0],
            ).matches
            
            merged_results = self._rrf_merge(sparse_results, dense_results, tag_results, dense_weight, sparse_weight, tag_weight)
        
        else:
            dense_results = []
            sparse_results = []
            merged_results = self._rrf_merge(sparse_results, dense_results, tag_results, dense_weight=0, sparse_weight=0, tag_weight=1)
    
        # Extract only text from the top k results
        relevant_content = []
        
        for results in merged_results[:k]:
            try: 
                relevant_content.append(results['metadata']['content']) 
            except KeyError:
            # Skip this result if 'metadata' or 'content' key is missing
                continue
            
        return relevant_content
        
        # For debugging purposes, you can uncomment the following lines to see the merged results
        # # extract chunk id and text from top k results
        # final_results = []
        # for results in merged_results[:k]:
        #     try:
        #         result_dict = {
        #             'id': results['id'],
        #             'text': results['metadata']['content'],
        #             'final_score': results['final_score'],
        #             'dense_score': results['original_dense_score'],
        #             'sparse_score': results['original_sparse_score'],
        #             'tag_score': results['original_tag_score'],
        #             'rrf_dense_score': results['dense_rrf_score'],
        #             'rrf_sparse_score': results['sparse_rrf_score'],
        #             'rrf_tag_score': results['tag_rrf_score'],
        #             'dense_rank': results['dense_rank'],
        #             'sparse_rank': results['sparse_rank'],
        #             'tag_rank': results['tag_rank'],
        #         }
        #         final_results.append(result_dict)
        #     except KeyError:
        #         # Skip this result if 'metadata' or 'content' key is missing
        #         continue
        # return final_results
        

    def _retrieve_with_image(self, query: Query, k=20) -> list[dict]:
        dense_results = self.dense_db.query(
            namespace="umag",
            top_k=k,
            include_values=False,
            include_metadata=True,
            vector=self.dense_embedding_model.encode_image([query["content"]])[
                0
            ].tolist(),
        )

        return [
            MergedResult(
                id=match["id"],
                content=match["metadata"].get("img_path", ""),
                metadata=match["metadata"],
                dense_score=match["score"],
                sparse_score=None,
                final_score=match["score"],
                sources=["dense"],
            )
            for match in dense_results.get("matches", [])
        ]

    