import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from bot.orders import place_order
from bot.exceptions import TradingBotException
import json

app = typer.Typer(
    help="Binance Futures Testnet Trading Bot CLI",
    add_completion=False,
    no_args_is_help=True
)
console = Console()

@app.command()
def order(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET, LIMIT, or STOP"),
    quantity: float = typer.Argument(..., help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price for LIMIT orders"),
    stop_price: float = typer.Option(None, "--stop-price", "-s", help="Stop price for STOP/STOP_MARKET orders")
):
    """
    Place a Futures order on the Binance Testnet.
    """
    # Create an order summary table
    summary_table = Table(title="Order Summary", show_header=True, header_style="bold magenta")
    summary_table.add_column("Property", style="cyan", no_wrap=True)
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Symbol", symbol.upper())
    summary_table.add_row("Side", side.upper())
    summary_table.add_row("Type", order_type.upper())
    summary_table.add_row("Quantity", str(quantity))
    if price:
        summary_table.add_row("Price", str(price))
    if stop_price:
        summary_table.add_row("Stop Price", str(stop_price))

    console.print(summary_table)
    
    # Interactive confirmation prompt
    confirm = typer.confirm("Do you want to proceed with placing this order?")
    if not confirm:
        rprint("[bold red]Order cancelled by user.[/bold red]")
        raise typer.Abort()

    # Spinner animation execution
    with console.status("[bold blue]Placing order on Binance Testnet...", spinner="dots"):
        try:
            response = place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            
            # Format output gorgeously
            result_str = json.dumps(response, indent=2)
            panel = Panel(
                f"[bold green]Order Placed Successfully![/bold green]\n\n{result_str}",
                title="API Success Response",
                border_style="green"
            )
            console.print(panel)
            
        except TradingBotException as e:
            panel = Panel(
                f"[bold red]Error: {str(e)}[/bold red]",
                title="API Failed Response",
                border_style="red"
            )
            console.print(panel)
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[bold red]Critical Internal Error: {str(e)}[/bold red]")
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
