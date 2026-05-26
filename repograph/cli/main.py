import typer 

from repograph.cli.commands.index import index_command
from repograph.cli.commands.ask import ask_command


app = typer.Typer()

app.command(name="index")(index_command)
app.command(name="ask")(ask_command)

if __name__ == "__main__":
    app()

    

