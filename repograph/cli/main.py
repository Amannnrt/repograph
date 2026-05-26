import typer 

from repograph.cli.commands.index import index_command 
app = typer.Typer()

@app.callback()
def main():
    """
    RepoGrah CLI
    """
    pass


app.command(name="index")(index_command)

if __name__ == "__main__":
    app()

    

