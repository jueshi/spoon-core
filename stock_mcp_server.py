import yfinance as yf
from typing import Dict, Any, Callable
import datetime
import json

class MCPServer:
    """
    A minimal MCP-style server abstraction.
    Allows registering tools and calling them.
    """
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        """Registers a tool with the server."""
        self.tools[name] = func
        print(f"[{self.name}] Registered tool: {name}")

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Calls a registered tool."""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found."}

        try:
            return self.tools[tool_name](arguments)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def run(self):
        """
        Starts the server. For this minimal implementation, it's just a placeholder
        or could implement a simple input loop to test tools directly.
        In a real MCP implementation, this would handle IPC/STDIO/HTTP.
        """
        print(f"[{self.name}] Server running. Waiting for calls (simulated).")

def get_stock_quote_tool(args: dict) -> dict:
    """
    Fetches the latest daily OHLCV data for a given stock symbol using yfinance.

    Args:
        args: A dictionary containing 'symbol' (str). Defaults to 'AAPL'.

    Returns:
        A dictionary with stock data or an error message.
    """
    symbol = args.get("symbol", "AAPL").upper()

    try:
        ticker = yf.Ticker(symbol)
        # Fetch 1 day of history
        hist = ticker.history(period="1d")

        if hist.empty:
            return {"symbol": symbol, "error": f"No data found for symbol '{symbol}'."}

        # Get the latest row
        latest = hist.iloc[-1]

        # Format the date
        # The index is usually a Timestamp
        date_str = str(latest.name.date())

        return {
            "symbol": symbol,
            "date": date_str,
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "close": float(latest["Close"]),
            "volume": int(latest["Volume"])
        }

    except Exception as e:
        return {"symbol": symbol, "error": f"Failed to fetch data: {str(e)}"}

# Global server instance for easy import or standalone run
server = MCPServer("stock-mcp")
server.register_tool("get_stock_quote", get_stock_quote_tool)

if __name__ == "__main__":
    # Minimal standalone test
    server.run()

    # Simulate a call
    test_symbol = "MSFT"
    print(f"\nTesting with symbol: {test_symbol}")
    result = server.call_tool("get_stock_quote", {"symbol": test_symbol})
    print(json.dumps(result, indent=2))
