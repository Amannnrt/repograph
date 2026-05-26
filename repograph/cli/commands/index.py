import typer
from pathlib import Path
from rich import print
from repograph.indexing.loader import RepositoryLoader 

def index_command(repo_path: str = typer.Argument(".", help="Path to the repository to index")):
    loader = RepositoryLoader()
    repo = Path(repo_path)
    if not repo.exists():
        print("[red]Repo path does not exist[/red]")
        raise typer.Exit(code=1)
    
    files = loader.load(repo)
    print(f"[green]Loaded {len(files)} source files[/green]")

    for file in files[:5]:
        print(f" - {file.path}")

        
