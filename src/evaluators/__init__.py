from typing_extensions import Callable
from src.interfaces import Retriever
import json


class RetrieverEvaluator:
    def __init__(self):
        pass

    def evaluate(
        self,
        dataset,
        retriever: Retriever,
        metrics: dict[str, Callable],
        output_path=None,
    ):
        res = {"dataset_name": dataset["dataset_name"], "results": []}
        for item in dataset["data"]:
            retrieved_docs = retriever.process(
                [{"content": item["question"], "metadata": {"type": "text"}}]
            )
            retrieved_context = [doc.content for doc in retrieved_docs]

            scores = {}
            for metric_name, metric in metrics.items():
                score = metric(item["reference_context"], retrieved_context)
                scores[metric_name] = score

            res["results"].append(
                {
                    "question": item["question"],
                    "references": item["reference_context"],
                    "retrieved_context": retrieved_context,
                    "scores": scores,
                }
            )

        # Save results to a file
        if output_path is None:
            output_path = f"output/evaluation_results_{dataset['dataset_name']}.json"

        with open(output_path, "w") as f:
            json.dump(res, f, indent=4)
        print(f"Evaluation results saved to {output_path}")

        return res
