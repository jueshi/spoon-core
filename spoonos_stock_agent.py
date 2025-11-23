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

    def extract_symbol(self, user_input: str) -> str:
        """
        Extracts stock symbol from natural language input.
        Looks for uppercase words that could be stock symbols.
        """
        # Common stock symbols pattern (1-5 uppercase letters)
        import re
        
        # Look for uppercase words that could be stock symbols
        symbol_pattern = r'\b[A-Z]{1,5}\b'
        matches = re.findall(symbol_pattern, user_input.upper())
        
        if matches:
            # Return the first match (most likely to be the symbol)
            return matches[0]
        
        # Fallback: look for common tech stock symbols in the text
        common_symbols = {
            'msft', 'aapl', 'googl', 'goog', 'amzn', 'tsla', 'nvda', 'meta', 
            'nflx', 'amd', 'intc', 'crm', 'orcl', 'adbe', 'pypl', 'uber',
            'lyft', 'snap', 'twtr', 'pinterest', 'zoom', 'shopify', 'spotify'
        }
        
        words = user_input.lower().split()
        for word in words:
            # Clean up punctuation
            clean_word = ''.join(filter(str.isalnum, word))
            if clean_word in common_symbols:
                return clean_word.upper()
        
        # Default fallback
        return "AAPL"

    async def handle_request(self, user_input: str) -> str:
        """
        Parses user input, calls the appropriate stock tool, and formats the response.
        Supports both quote and historical data requests.
        """
        user_input = user_input.strip()
        original_input = user_input
        user_input = user_input.lower()
        
        if not user_input:
            return "Please provide a stock symbol or request."
        
        # Extract symbol using improved logic
        symbol = self.extract_symbol(original_input)

        # Determine if this is a historical data request
        historical_keywords = ["historical", "history", "past", "data", "chart"]
        period_keywords = {
            "1d": ["1d", "1 day", "daily"],
            "5d": ["5d", "5 day", "5 days"],
            "1mo": ["1mo", "1 month", "monthly"],
            "3mo": ["3mo", "3 month", "3 months", "quarter", "quarterly"],
            "6mo": ["6mo", "6 month", "6 months"],
            "1y": ["1y", "1 year", "yearly", "year"],
            "2y": ["2y", "2 year", "2 years"],
            "5y": ["5y", "5 year", "5 years"],
            "max": ["max", "maximum", "all time"]
        }
        
        is_historical = any(keyword in user_input for keyword in historical_keywords)
        
        # Determine period if historical
        period = "1mo"  # default
        if is_historical:
            for period_key, keywords in period_keywords.items():
                if any(keyword in user_input for keyword in keywords):
                    period = period_key
                    break
        
        # Determine interval
        interval = "1d"  # default
        if "1m" in user_input or "minute" in user_input:
            interval = "1m"
        elif "5m" in user_input or "5 minute" in user_input:
            interval = "5m"
        elif "1h" in user_input or "hour" in user_input:
            interval = "1h"
        elif "1d" in user_input or "daily" in user_input:
            interval = "1d"
        elif "1wk" in user_input or "weekly" in user_input:
            interval = "1wk"

        # Choose the appropriate tool
        if is_historical:
            result = await self.stock_mcp.call_tool(
                tool_name="get_stock_historical_data",
                arguments={"symbol": symbol, "period": period, "interval": interval}
            )
            
            # Handle errors
            if "error" in result:
                return f"Error fetching historical data for {symbol}: {result['error']}"
            
            # Format historical data response
            output = f"Historical data for {symbol} ({result['period']}, {result['interval']}):\n"
            output += f"Data points: {result['data_points']}\n\n"
            
            # Show first 5 and last 5 data points
            data = result['data']
            if len(data) <= 10:
                for point in data:
                    output += f"{point['date']}: O={point['open']:.2f} H={point['high']:.2f} L={point['low']:.2f} C={point['close']:.2f} V={point['volume']:,}\n"
            else:
                # Show first 5
                for point in data[:5]:
                    output += f"{point['date']}: O={point['open']:.2f} H={point['high']:.2f} L={point['low']:.2f} C={point['close']:.2f} V={point['volume']:,}\n"
                output += "...\n"
                # Show last 5
                for point in data[-5:]:
                    output += f"{point['date']}: O={point['open']:.2f} H={point['high']:.2f} L={point['low']:.2f} C={point['close']:.2f} V={point['volume']:,}\n"
            
            return output
        else:
            # Use the existing quote tool
            result = await self.stock_mcp.call_tool(
                tool_name="get_stock_quote",
                arguments={"symbol": symbol}
            )

            # Handle errors
            if "error" in result:
                return f"Error fetching quote for {symbol}: {result['error']}"

            # Format the success response
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
