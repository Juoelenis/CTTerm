
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from market.data import get_ticker

console = Console()

VERSION = "0.1.0"
APP_NAME = "CarlosTraderTerminal"


def banner():
    console.print(
        Panel(
            f"[bold green]CTTerm[/bold green]\n"
            f"[dim]{APP_NAME}[/dim]\n"
            f"[green]Version {VERSION}[/green]",
            border_style="green",
            expand=False
        )
    )


def show_help():
    console.print("""
[bold green]Available commands[/bold green]

  quote [PAIR]    Fetch market data
  help            Show this help menu
  clear           Clear terminal
  version         Display version
  exit            Exit CTTerm

[dim]Example: quote BTC/USDT[/dim]
""")


def quote(symbol="BTC/USDT"):
    console.print(f"\n[dim]Fetching {symbol}...[/dim]")

    data = get_ticker(symbol)

    if not data or "error" in data:
        error = data.get("error", "Unknown market data error") if data else "No data returned"
        console.print(f"[bold red]Market error:[/bold red] {error}")
        return

    table = Table(
        title=f"{data['symbol']} MARKET DATA",
        border_style="green"
    )

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white", justify="right")

    table.add_row("Last price", str(data["price"]))
    table.add_row(
        "24H Change",
        f"{data['change']}%" if data["change"] is not None else "N/A"
    )
    table.add_row("24H High", str(data["high"] or "N/A"))
    table.add_row("24H Low", str(data["low"] or "N/A"))
    table.add_row("Volume", str(data["volume"] or "N/A"))

    console.print(table)


def process_command(command):
    parts = command.strip().split()

    if not parts:
        return True

    action = parts[0].lower()

    if action == "help":
        show_help()

    elif action == "quote":
        symbol = parts[1] if len(parts) > 1 else "BTC/USDT"
        quote(symbol)

    elif action == "clear":
        console.clear()
        banner()

    elif action == "version":
        console.print(f"[green]CTTerm v{VERSION}[/green]")

    elif action in ("exit", "quit"):
        console.print("[yellow]CTTerm shutting down.[/yellow]")
        return False

    else:
        console.print(
            f"[red]Unknown command:[/red] {action}"
        )
        console.print("[dim]Type 'help' for available commands.[/dim]")

    return True


def main():
    console.clear()
    banner()

    console.print(
        "[dim]Welcome to CTTerm. Type 'help' to begin.[/dim]\n"
    )

    running = True

    while running:
        try:
            command = console.input(
                "[bold green]CTTerm > [/bold green]"
            )

            running = process_command(command)

        except KeyboardInterrupt:
            console.print(
                "\n[yellow]Use 'exit' to shut down CTTerm.[/yellow]"
            )

        except EOFError:
            console.print("\n[yellow]CTTerm shutting down.[/yellow]")
            break


if __name__ == "__main__":
    main()

