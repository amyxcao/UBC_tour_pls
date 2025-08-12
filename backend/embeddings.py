import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor, AutoTokenizer
from transformers import AutoModelForMaskedLM

from backend.interfaces import BaseEmbeddingModel



class DefaultDenseEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your dense embedding model here
        self.model_name = "BAAI/BGE-VL-base"  # or "BAAI/BGE-VL-large"
        self.model = AutoModel.from_pretrained(
            self.model_name, trust_remote_code=True
        ).to(self.device)
        self.preprocessor = AutoProcessor.from_pretrained(
            self.model_name, trust_remote_code=True
        )

    def encode_text(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        inputs = self.preprocessor(
            text=texts, return_tensors="pt", truncation=True, padding=True
        ).to(self.device)
        return self.model.get_text_features(**inputs).cpu().tolist()

    def encode_image(self, images: list[str] | list[Image.Image]) -> list[float]:
        if not images:
            return []
        if isinstance(images[0], str):
            images = [Image.open(image_path).convert("RGB") for image_path in images]
        inputs = self.preprocessor(images=images, return_tensors="pt").to(self.device)
        return self.model.get_image_features(**inputs).cpu().tolist()


class DefaultSparseEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your sparse embedding model here
        self.model_name = "naver/splade-v3"
        self.model = AutoModelForMaskedLM.from_pretrained(self.model_name).to(
            self.device
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def encode_text(self, texts: list[str]) -> list[dict]:
        if not texts:
            return []
        tokens = self.tokenizer(
            texts, return_tensors="pt", truncation=True, padding=True
        ).to(self.device)
        outputs = self.model(**tokens)
        sparse_embedding = (
            torch.max(
                torch.log(1 + torch.relu(outputs.logits))
                * tokens.attention_mask.unsqueeze(-1),
                dim=1,
            )[0]
            .detach()
            .cpu()
        )

        # convert to pinecone sparse format
        res = []
        for i in range(len(sparse_embedding)):
            indices = sparse_embedding[i].nonzero().squeeze().tolist()
            values = sparse_embedding[i, indices].tolist()
            res.append({"indices": indices, "values": values})
        return res
