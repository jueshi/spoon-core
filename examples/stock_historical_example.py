import asyncio
import sys
import os

# Ensure we can import from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spoonos_stock_agent import StockAgent

async def main():
    print("--- Stock Historical Data MCP Example ---")

    agent = StockAgent()

    # Example 1: Historical data for 1 month
    symbol = "MSFT"
    print(f"\nQuerying: 'historical data for {symbol} for 1 month'")
    response = await agent.handle_request(f"historical data for {symbol} for 1 month")
    print(f"Result:\n{response}")

    # Example 2: Historical data for 1 year with daily intervals
    symbol = "AAPL"
    print(f"\nQuerying: 'show me {symbol} historical data for 1 year daily'")
    response = await agent.handle_request(f"show me {symbol} historical data for 1 year daily")
    print(f"Result:\n{response}")

    # Example 3: Historical data for 5 years
    symbol = "NVDA"
    print(f"\nQuerying: '{symbol} 5 year historical data'")
    response = await agent.handle_request(f"{symbol} 5 year historical data")
    print(f"Result:\n{response}")

    # Example 4: Recent 5 days of data
    symbol = "TSLA"
    print(f"\nQuerying: '{symbol} past 5 days data'")
    response = await agent.handle_request(f"{symbol} past 5 days data")
    print(f"Result:\n{response}")

    # Example 5: Quarterly data (3 months)
    symbol = "GOOGL"
    print(f"\nQuerying: '{symbol} quarterly historical data'")
    response = await agent.handle_request(f"{symbol} quarterly historical data")
    print(f"Result:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())