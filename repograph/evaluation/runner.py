import json
from pathlib import Path

from rich import print
from rich.table import Table

from repograph.evaluation.metrics import (
    EvaluationMetrics,
)
from repograph.retrieval.retriever import (
    Retriever,
)


DATASET_PATH = (
    Path(__file__)
    .parent
    / "dataset"
    / "eval_dataset.json"
)



class EvaluationRunner:

    def __init__(self):

        self.retriever = Retriever()
        self.metrics = EvaluationMetrics()

    def load_dataset(self):

        if not DATASET_PATH.exists():
            raise FileNotFoundError(
                f"Dataset not found: {DATASET_PATH}"
            )

        with open(DATASET_PATH, "r") as file:
            return json.load(file)

    def find_correct_rank(
        self,
        results,
        expected_file: str,
        expected_function: str,
    ):

        for rank, result in enumerate(
            results,
            start=1,
        ):

            payload = result.payload

            file_match = (
                payload["file_path"]
                == expected_file
            )

            symbol_match = (
                payload["name"]
                == expected_function
                or payload["name"].endswith(
                    f".{expected_function}"
                )
            )

            if file_match and symbol_match:
                return rank

        return None

    def run(self):

        dataset = self.load_dataset()

        table = Table(
            title="RepoGraph Evaluation"
        )

        table.add_column("Question")
        table.add_column("Expected")
        table.add_column("Rank")
        table.add_column("Status")

        for sample in dataset:

            question = sample["question"]
            expected_function = (
                sample["expected_function"]
            )
            expected_file = (
                sample["expected_file"]
            )

            results = self.retriever.search(
                query=question,
                limit=5,
            )

            rank = self.find_correct_rank(
                results=results,
                expected_file=expected_file,
                expected_function=expected_function,
            )

            self.metrics.update(rank)

            table.add_row(
                question,
                expected_function,
                str(rank) if rank else "-",
                "PASS" if rank else "FAIL",
            )

        print()
        print(table)
        print()

        summary = self.metrics.summary()

        print("[bold green]Evaluation Summary[/bold green]")
        print(
            f"Queries : {summary['queries']}"
        )
        print(
            f"Hit@1  : {summary['hit@1']}"
        )
        print(
            f"Hit@5  : {summary['hit@5']}"
        )
        print(
            f"MRR     : {summary['mrr']}"
        )
