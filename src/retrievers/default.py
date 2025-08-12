from pinecone import Pinecone
from ..interfaces import Retriever, Query, MergedResult
from ..embeddings.default import DefaultDenseEmbeddingModel, DefaultSparseEmbeddingModel
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class DefaultRetriever(Retriever):
    def __init__(self, config: dict = None):
        super().__init__(config)
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", ""))
        # Initialize Pinecone client or any other necessary components here
        self.dense_db = pc.Index("museum-ai-dense")
        self.sparse_db = pc.Index("museum-ai-sparse")
        self.dense_embedding_model = DefaultDenseEmbeddingModel({})
        self.sparse_embedding_model = DefaultSparseEmbeddingModel({})
        self.enable_parent_document_retrieval = self.config.get(
            "enable_parent_document_retrieval", False
        )

    def process(self, query: list[Query], k=20, **kwargs) -> list[dict]:
        query = query[0]  # TODO : support multiple queries in the future

        # Determine the type of query and use the appropriate way
        if query["metadata"].get("type", "text") == "text":
            # Use dense embeddings for text queries
            results = self._retrieve_with_text(query, k)

        elif query["metadata"].get("type", "text") == "image":
            # Use dense embeddings for image queries
            results = self._retrieve_with_image(query, k)

        if self.enable_parent_document_retrieval:
            results = self._retrieve_parent_documents(results, query, k)

        return results

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

    def _retrieve_with_text(self, query: Query, k=20, **kwargs) -> list[dict]:
        dense_results = self.dense_db.query(
            namespace="umag",
            top_k=k,
            include_values=False,
            include_metadata=True,
            vector=self.dense_embedding_model.encode_text([query["content"]])[0],
        )

        sparse_results = self.sparse_db.query(
            namespace="umag",
            top_k=k,
            include_values=True,
            include_metadata=True,
            sparse_vector=self.sparse_embedding_model.encode_text([query["content"]])[
                0
            ],
        )

        # Merge dense and sparse results
        merged_results = self._merge_results(dense_results, sparse_results, **kwargs)

        return merged_results

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

    def _retrieve_by_section_id(self, section_id: str) -> list[dict]:
        results = self.dense_db.query(
            namespace="umag",
            top_k=9999,
            include_values=False,
            include_metadata=True,
            filter={"section_id": section_id},
            vector=[0.0] * 512,
        )

        return results.get("matches", [])

    def _calculate_section_relevance_score(
        self, section_id: str, query: Query, retrieved_results: list[dict]
    ) -> float: ...

    def _merge_results(
        self,
        dense_results,
        sparse_results,
        dense_weight=0.3,
        sparse_weight=0.7,
        fusion_method="weighted_sum",
    ) -> list[dict]:
        """
        合并dense和sparse检索结果并去重

        Args:
            dense_result: dense数据库的检索结果
            sparse_result: sparse数据库的检索结果
            dense_weight: dense结果的权重
            sparse_weight: sparse结果的权重
            normalize_scores: 是否对分数进行归一化
            fusion_method: 融合方法 ("weighted_sum", "rrf", "max")

        Returns:
            合并并去重后的结果列表
        """

        # 提取matches
        dense_matches = dense_results.get("matches", [])
        sparse_matches = sparse_results.get("matches", [])

        # 用于存储所有文档的字典，key为id
        document_map = {}

        # 处理dense结果
        if dense_matches:
            dense_scores = [match["score"] for match in dense_matches]
            dense_max = max(dense_scores) if dense_scores else 1.0
            dense_min = min(dense_scores) if dense_scores else 0.0
            dense_range = dense_max - dense_min if dense_max != dense_min else 1.0

        for rank, match in enumerate(dense_matches):
            chunk_id = match["id"]
            score = match["score"]

            # normalize score to 1
            if dense_matches:
                normalized_score = (score - dense_min) / dense_range
            else:
                normalized_score = score

            document_map[chunk_id] = MergedResult(
                id=chunk_id,
                content=match["metadata"].get("content", ""),
                metadata=match["metadata"],
                dense_score=normalized_score,
                sparse_score=None,
                sources=["dense"],
            )

            # 设置dense排名用于RRF
            document_map[chunk_id].metadata["dense_rank"] = rank

        # 处理sparse结果
        if sparse_matches:
            sparse_scores = [match["score"] for match in sparse_matches]
            sparse_max = max(sparse_scores) if sparse_scores else 1.0
            sparse_min = min(sparse_scores) if sparse_scores else 0.0
            sparse_range = sparse_max - sparse_min if sparse_max != sparse_min else 1.0

        for rank, match in enumerate(sparse_matches):
            doc_id = match["id"]
            score = match["score"]

            # 分数归一化
            if sparse_matches:
                normalized_score = (score - sparse_min) / sparse_range
            else:
                normalized_score = score

            if doc_id in document_map:
                # 文档已存在，更新sparse分数和来源
                document_map[doc_id].sparse_score = normalized_score
                document_map[doc_id].sources.append("sparse")
            else:
                # 新文档
                document_map[doc_id] = MergedResult(
                    id=doc_id,
                    content=match["metadata"].get("content", ""),
                    metadata=match["metadata"],
                    dense_score=None,
                    sparse_score=normalized_score,
                    sources=["sparse"],
                )

            # 设置sparse排名用于RRF
            document_map[doc_id].metadata["sparse_rank"] = rank

        # 计算最终分数
        for doc in document_map.values():
            doc.final_score = self._calculate_final_score(
                doc, dense_weight, sparse_weight, fusion_method
            )

        # 按最终分数排序
        merged_results = sorted(
            document_map.values(), key=lambda x: x.final_score, reverse=True
        )

        return merged_results

    def _calculate_final_score(
        self,
        doc: MergedResult,
        dense_weight: float,
        sparse_weight: float,
        fusion_method: str,
    ) -> float:
        """计算文档的最终分数"""

        dense_score = doc.dense_score or 0.0
        sparse_score = doc.sparse_score or 0.0

        if fusion_method == "weighted_sum":
            # 加权求和
            final_score = dense_score * dense_weight + sparse_score * sparse_weight

        elif fusion_method == "rrf":
            # Reciprocal Rank Fusion
            k = 60  # RRF参数
            rrf_score = 0.0

            if doc.dense_score is not None:
                dense_rank = doc.metadata.get("dense_rank", 0)
                rrf_score += dense_weight / (k + dense_rank + 1)

            if doc.sparse_score is not None:
                sparse_rank = doc.metadata.get("sparse_rank", 0)
                rrf_score += sparse_weight / (k + sparse_rank + 1)

            final_score = rrf_score

        elif fusion_method == "max":
            # 取最大分数
            final_score = max(dense_score * dense_weight, sparse_score * sparse_weight)

        else:
            raise ValueError(f"Unknown fusion method: {fusion_method}")

        return final_score
