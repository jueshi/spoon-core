import asyncio
import json
import sys
from typing import Dict, Any

# In a real scenario, this would import the transport layer to communicate with the MCP server.
# For this exercise, we import the server instance directly to simulate an in-process call.
from stock_mcp_server import server as stock_server

class MCPClient:
    """
    A lightweight MCP Client abstraction.

    In a real-world SpoonOS agent, this would handle JSON-RPC over Stdio or HTTP.
    Here, it directly calls the imported Python server object to facilitate testing.
    """
    def __init__(self, server_name: str):
        self.server_name = server_name
        # In a real implementation, we would connect to the server here.
        pass

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Simulates an async call to the MCP tool.
        """
        # Simulate network/IPC latency if desired, but not strictly necessary.
        # await asyncio.sleep(0.1)

        # Direct in-process call to the imported server instance
        # In a distributed setup, this would be: await self.transport.send_request(...)
        print(f"[MCPClient] Calling {self.server_name} -> {tool_name}({arguments})")
        result = stock_server.call_tool(tool_name, arguments)
        return result

class StockAgent:
    """
    SpoonOS Agent specialized for Stock queries.
    """
    def __init__(self):
        self.stock_mcp = MCPClient(server_name="stock-mcp")

    async def handle_request(self, user_input: str) -> str:
        """
        Parses user input, calls the stock quote tool, and formats the response.
        """
        # Simple parsing: assume the last token is the symbol if present.
        parts = user_input.strip().split()
        if not parts:
            symbol = "AAPL" # Default
        else:
            # Heuristic: if the last word looks like a ticker (uppercase, alpha), use it.
            # Otherwise default to AAPL if the input is ambiguous.
            # For this simple agent, we'll just take the last word.
            possible_symbol = parts[-1]
            # Clean up punctuation just in case
            symbol = ''.join(filter(str.isalnum, possible_symbol))

            # If the user just said "quote" or "price" with no symbol, fallback?
            # Let's stick to the requirement: "treat the last token as the stock symbol if present"
            if not symbol:
                symbol = "AAPL"

        # Call the tool
        result = await self.stock_mcp.call_tool(
            tool_name="get_stock_quote",
            arguments={"symbol": symbol}
        )

        # Handle errors
        if "error" in result:
            return f"Error fetching quote for {symbol}: {result['error']}"

        # Format the success response
        # Expected output format:
        # AAPL on 2025-01-10:
        #   Open:  190.12
        #   High:  192.34
        #   Low:   189.50
        #   Close: 191.80
        #   Vol:   123456789

        output = (
            f"{result['symbol']} on {result['date']}:\n"
            f"  Open:  {result['open']:.2f}\n"
            f"  High:  {result['high']:.2f}\n"
            f"  Low:   {result['low']:.2f}\n"
            f"  Close: {result['close']:.2f}\n"
            f"  Vol:   {result['volume']}"
        )

        return output

async def main():
    agent = StockAgent()

    print("--- SpoonOS Stock Agent (Local Test) ---")
    print("Enter a query like 'quote MSFT' or 'price of NVDA'. (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ("exit", "quit"):
                break

            if not user_input.strip():
                continue

            response = await agent.handle_request(user_input)
            print(f"Agent:\n{response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
