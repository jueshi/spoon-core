import asyncio
import sys
import os

# Ensure we can import from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spoonos_stock_agent import StockAgent

async def main():
    print("--- Stock Quote MCP Example ---")

    agent = StockAgent()

    # Example 1: Simple quote
    symbol = "MSFT"
    print(f"\nQuerying: 'quote {symbol}'")
    response = await agent.handle_request(f"quote {symbol}")
    print(f"Result:\n{response}")

    # Example 2: Another symbol
    symbol = "NVDA"
    print(f"\nQuerying: 'price of {symbol}'")
    response = await agent.handle_request(f"price of {symbol}")
    print(f"Result:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())
