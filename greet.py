import typer

app = typer.Typer()

@app.command()
def greet(name: str, age: int = 20):
    typer.echo(f"Hello {name}, you are {age} years old")

@app.command("bye")
def goodbye(name: str):
    typer.echo(f"Goodbye, {name}")

if __name__ == "__main__":
    app()

