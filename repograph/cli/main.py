import typer

from repograph.cli.commands.ask import ask_command
from repograph.cli.commands.eval import (
    eval_command,
)
from repograph.cli.commands.index import (
    index_command,
)
from repograph.cli.commands.search import (
    search_command,
)

from repograph.cli.commands.status import (
    status_command,
)
from repograph.cli.commands.version import (
    version_command,
)

app = typer.Typer()

app.command(name="index")(index_command)
app.command(name="ask")(ask_command)
app.command(name="search")(search_command)
app.command(name="eval")(eval_command)
app.command(name="status")(status_command)
app.command(name="version")(version_command)


if __name__ == "__main__":
    app()
