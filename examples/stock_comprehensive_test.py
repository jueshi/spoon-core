import asyncio
import sys
import os

# Ensure we can import from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spoonos_stock_agent import StockAgent

async def main():
    print("--- Stock Agent Comprehensive Test ---")

    agent = StockAgent()

    # Test 1: Simple quote (direct symbol)
    print(f"\n1. Testing simple quote: 'AAPL'")
    response = await agent.handle_request("AAPL")
    print(f"Result:\n{response}")

    # Test 2: Historical data - 1 month
    print(f"\n2. Testing historical data: 'MSFT historical data 1 month'")
    response = await agent.handle_request("MSFT historical data 1 month")
    print(f"Result:\n{response}")

    # Test 3: Historical data - 1 year
    print(f"\n3. Testing historical data: 'NVDA 1 year historical data'")
    response = await agent.handle_request("NVDA 1 year historical data")
    print(f"Result:\n{response}")

    # Test 4: Historical data - 5 days
    print(f"\n4. Testing historical data: 'TSLA past 5 days'")
    response = await agent.handle_request("TSLA past 5 days")
    print(f"Result:\n{response}")

    # Test 5: Historical data - quarterly (3 months)
    print(f"\n5. Testing historical data: 'GOOGL quarterly data'")
    response = await agent.handle_request("GOOGL quarterly data")
    print(f"Result:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())