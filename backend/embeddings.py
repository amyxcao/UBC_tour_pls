import os
from typing import Any, Dict, List, Union

# 3rd party imports kept light at import-time.
# Heavy libs (torch/transformers/Pillow) are imported lazily inside helpers.
from interfaces import BaseEmbeddingModel

# Avoid tokenizer multiprocessing warnings / extra threads
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Optional switch: set USE_LOCAL_EMBEDDINGS=0 on Render to disable these classes entirely.
USE_LOCAL = os.getenv("USE_LOCAL_EMBEDDINGS", "1") not in ("0", "false", "False")


def _torch_inference_mode():
    """Context manager that works whether torch is available or not."""
    import contextlib

    try:
        import torch  # noqa

        return __import__("torch").inference_mode()
    except Exception:
        return contextlib.nullcontext()


# ----------------------------
# Dense (vision+text) embeddings
# ----------------------------


class DefaultDenseEmbeddingModel(BaseEmbeddingModel):
    """
    Lazy-loads BGE-VL on first use to reduce startup memory.
    """

    _model = None
    _processor = None

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_name = config.get(
            "dense_model_name", "BAAI/BGE-VL-base"
        )  # base is much lighter than large
        if not USE_LOCAL:
            raise RuntimeError(
                "Local dense embeddings disabled. Set USE_LOCAL_EMBEDDINGS=1 to enable, "
                "or switch to a hosted embedding service."
            )

    def _ensure_loaded(self):
        if self.__class__._model is not None:
            return

        # Import heavy deps lazily
        from transformers import AutoModel, AutoProcessor

        model = AutoModel.from_pretrained(self.model_name, trust_remote_code=True)
        model.to(self.device)
        processor = AutoProcessor.from_pretrained(
            self.model_name, trust_remote_code=True
        )

        self.__class__._model = model
        self.__class__._processor = processor

    def encode_text(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        self._ensure_loaded()

        with _torch_inference_mode():
            inputs = self.__class__._processor(
                text=texts, return_tensors="pt", truncation=True, padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            feats = self.__class__._model.get_text_features(**inputs)
            return feats.detach().cpu().tolist()

    def encode_image(
        self, images: Union[List[str], List["Image.Image"]]
    ) -> List[List[float]]:
        if not images:
            return []
        self._ensure_loaded()

        # Lazy import Pillow + torch
        import torch  # noqa
        from PIL import Image

        # Accept file paths or PIL Images
        if isinstance(images[0], str):
            images = [Image.open(p).convert("RGB") for p in images]

        with _torch_inference_mode():
            inputs = self.__class__._processor(images=images, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            feats = self.__class__._model.get_image_features(**inputs)
            return feats.detach().cpu().tolist()


# ----------------------------
# Sparse (text) embeddings
# ----------------------------


class DefaultSparseEmbeddingModel(BaseEmbeddingModel):
    """
    Lazy-loads SPLADE on first use. Still heavy; consider hosted sparse alternatives if memory is tight.
    """

    _model = None
    _tokenizer = None

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_name = config.get("sparse_model_name", "naver/splade-v3")
        if not USE_LOCAL:
            raise RuntimeError(
                "Local sparse embeddings disabled. Set USE_LOCAL_EMBEDDINGS=1 to enable."
            )

    def _ensure_loaded(self):
        if self.__class__._model is not None:
            return

        from transformers import AutoModelForMaskedLM, AutoTokenizer

        tok = AutoTokenizer.from_pretrained(self.model_name)
        mdl = AutoModelForMaskedLM.from_pretrained(self.model_name)
        mdl.to(self.device)

        self.__class__._tokenizer = tok
        self.__class__._model = mdl

    def encode_text(self, texts: List[str]) -> List[Dict[str, List[float]]]:
        if not texts:
            return []
        self._ensure_loaded()

        import torch  # lazy

        tok = self.__class__._tokenizer
        mdl = self.__class__._model

        with _torch_inference_mode():
            tokens = tok(texts, return_tensors="pt", truncation=True, padding=True)
            tokens = {k: v.to(self.device) for k, v in tokens.items()}
            outputs = mdl(**tokens)

            # SPLADE-style sparse projection
            logits = outputs.logits
            attn = tokens["attention_mask"].unsqueeze(-1)
            # log(1 + relu(logits)) * mask, then max over sequence length
            sparse = torch.max(torch.log1p(torch.relu(logits)) * attn, dim=1).values
            sparse = sparse.detach().cpu()

        # Convert to Pinecone sparse format
        res: List[Dict[str, List[float]]] = []
        for row in sparse:
            nz = row.nonzero().squeeze().tolist()
            if isinstance(nz, int):  # handle scalar edge case
                nz = [nz]
            vals = row[nz].tolist() if nz else []
            res.append({"indices": nz, "values": vals})
        return res
