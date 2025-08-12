from src.query_rewriters.default import DefaultQueryRewriter
from src.interfaces import Query
from PIL import Image
from typeguard import check_type
from typeguard import TypeCheckError

rewriter = DefaultQueryRewriter()
text_query = {
    "content": "What is the capital of France?",
    "metadata": {
        "type": "text",
    },
}

image_path_query = {
    "content": r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg",
    "metadata": {
        "type": "image",
    },
}

image_query = {
    "content": Image.open(
        r"output\Objectifying_China\auto\images\0bf9d41010da900a0abb7048118e147c6e962eec73c6962affcf498cec014420.jpg"
    ),
    "metadata": {
        "type": "image",
    },
}


def test_1():
    res = rewriter.process(text_query)
    assert check_type(res, Query)


def test_2():
    res = rewriter.process(image_path_query)
    assert check_type(res, Query)


def test_3():
    res = rewriter.process(image_query)
    try:
        check_type(res, Query)
        assert False
    except TypeCheckError:
        assert True
