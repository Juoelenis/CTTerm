from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from market.data import get_ticker, fetch_ohlcv
from charts.candles import render_candles


APP_NAME = "CarlosTraderTerminal"
VERSION = "0.2.0"

console = Console()


def banner():
    console.print(
        Panel(
            "[bold cyan]CarlosTraderTerminal[/bold cyan]\n"
            "[dim]CTTerm v0.2.0 | Market Data Terminal[/dim]\n"
            "[green]Public market data | Paper trading project[/green]",
            border_style="cyan",
        )
    )


def show_help():
    table = Table(title="CTTerm Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("help", "Show available commands")
    table.add_row("quote [PAIR]", "Display current market price")
    table.add_row("chart [PAIR] [TF] [LIMIT]", "Display ASCII candlestick chart")
    table.add_row("version", "Show CTTerm version")
    table.add_row("clear", "Clear terminal")
    table.add_row("exit / quit", "Exit CTTerm")

    console.print(table)


def quote(symbol="BTC/USDT"):
    try:
        data = get_ticker(symbol)

        if isinstance(data, dict) and "error" in data:
            console.print(f"[red]{data['error']}[/red]")
            return

        table = Table(title=f"{symbol} Market Data")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Last Price", str(data["last"]))
        table.add_row("24h High", str(data["high"]))
        table.add_row("24h Low", str(data["low"]))
        table.add_row("24h Change", str(data["percentage"]))
        table.add_row("24h Volume", str(data["baseVolume"]))

        console.print(table)

    except Exception as error:
        console.print(f"[red]Quote error: {error}[/red]")


def chart(symbol="BTC/USDT", timeframe="1h", limit=30):
    console.print(
        f"\n[cyan]Fetching {limit} candles for "
        f"{symbol} ({timeframe})...[/cyan]"
    )

    try:
        candles = fetch_ohlcv(symbol, timeframe, limit)

        if isinstance(candles, dict) and "error" in candles:
            console.print(f"[red]{candles['error']}[/red]")
            return

        if not candles:
            console.print("[yellow]No candle data returned.[/yellow]")
            return

        chart_output = render_candles(candles, height=16)

        console.print(
            Panel(
                chart_output,
                title=f"{symbol} | {timeframe}",
                border_style="cyan",
            )
        )

    except Exception as error:
        console.print(f"[red]Chart error: {error}[/red]")


def process_command(command):
    parts = command.strip().split()

    if not parts:
        return True

    action = parts[0].lower()

    if action == "help":
        show_help()

    elif action == "version":
        console.print(
            f"[cyan]{APP_NAME} v{VERSION}[/cyan]"
        )

    elif action == "quote":
        symbol = parts[1].upper() if len(parts) > 1 else "BTC/USDT"
        quote(symbol)

    elif action == "chart":
        symbol = parts[1].upper() if len(parts) > 1 else "BTC/USDT"
        timeframe = parts[2] if len(parts) > 2 else "1h"

        try:
            limit = int(parts[3]) if len(parts) > 3 else 30

            if not 5 <= limit <= 100:
                console.print(
                    "[yellow]Limit must be between 5 and 100.[/yellow]"
                )
                return True

            chart(symbol, timeframe, limit)

        except ValueError:
            console.print(
                "[red]Invalid candle limit. Use a number.[/red]"
            )

    elif action == "clear":
        console.clear()
        banner()

    elif action in ("exit", "quit"):
        console.print(
            "\n[bold yellow]CTTerm shutting down. Goodbye![/bold yellow]"
        )
        return False

    else:
        console.print(
            f"[red]Unknown command: {action}[/red]"
        )
        console.print("[dim]Type 'help' for commands.[/dim]")

    return True
  
def main():
    console.clear()
    banner()

    console.print(
        "[dim]Type 'help' to see available commands.[/dim]\n"
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
            console.print(
                "\n[yellow]CTTerm shutting down.[/yellow]"
            )
            break


if __name__ == "__main__":
    main()
