from src.embeddings.default import (
    DefaultDenseEmbeddingModel,
    DefaultSparseEmbeddingModel,
)
from PIL import Image

dense_embedding_model = DefaultDenseEmbeddingModel(config={})
sparse_embedding_model = DefaultSparseEmbeddingModel(config={})


def test1():
    texts = ["Hello world", "This is a test"]
    embeddings = dense_embedding_model.encode_text(texts)
    assert len(embeddings) == len(texts)
    assert all(isinstance(embedding, list) for embedding in embeddings)
    assert all(len(embedding) == 512 for embedding in embeddings)


def test2():
    texts = []
    embeddings = dense_embedding_model.encode_text(texts)
    assert embeddings == []


def test3():
    images = [
        r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg",
        r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg",
    ]
    embeddings = dense_embedding_model.encode_image(images)
    assert len(embeddings) == len(images)
    assert all(isinstance(embedding, list) for embedding in embeddings)
    assert all(len(embedding) == 512 for embedding in embeddings)


def test4():
    images = [
        Image.open(
            r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg"
        ),
        Image.open(
            r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg"
        ),
    ]
    embeddings = dense_embedding_model.encode_image(images)
    assert len(embeddings) == len(images)
    assert all(isinstance(embedding, list) for embedding in embeddings)
    assert all(len(embedding) == 512 for embedding in embeddings)


def test5():
    texts = ["Hello world", "This is a test"]
    embeddings = sparse_embedding_model.encode_text(texts)
    assert len(embeddings) == len(texts)
    assert all(isinstance(embedding, dict) for embedding in embeddings)
    assert all(
        "values" in embedding and "indices" in embedding for embedding in embeddings
    )
