import typer
from rich.console import Console

from foodagent.agent import build_model, chat
from foodagent.config import load_settings
from foodagent.sessions import SessionStore

app = typer.Typer(help="food-order-agent: agente conversacional de pedidos de comida")
console = Console()


@app.command()
def chat_repl() -> None:
    """Abre um chat no terminal com o agente de pedidos."""
    settings = load_settings()
    model = build_model(settings)
    store = SessionStore()
    session = store.get("cli")

    console.print("[bold cyan]food-order-agent[/bold cyan] — digite 'sair' para encerrar\n")
    while True:
        message = console.input("[bold green]você:[/bold green] ")
        if message.strip().lower() in {"sair", "exit", "quit"}:
            break
        resposta = chat(model, session, message, settings)
        console.print(f"[bold magenta]agente:[/bold magenta] {resposta}\n")


if __name__ == "__main__":
    app()
