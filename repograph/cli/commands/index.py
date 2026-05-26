import typer
from pathlib import Path
from rich import print

def index_command(repo_path: str = typer.Argument(".", help="Path to the repository to index")):
    
    repo = Path(repo_path)
    if not repo.exists():
        print("[red]Repo path does not exist[/red]")
        raise typer.Exit(code=1)
    print(f"[green]Indexing repository:[/green] {repo.resolve()}")
