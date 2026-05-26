from rich import print

from repograph.evaluation.runner import (
    EvaluationRunner,
)


def eval_command():

    print(
        "[cyan]Running retrieval evaluation...[/cyan]"
    )

    runner = EvaluationRunner()

    runner.run()
