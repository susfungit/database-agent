#!/usr/bin/env python3
"""
Basic usage example for the Database Agent MCP Server.
"""

import asyncio
from src.database_agent.agent import DatabaseAgent
from src.utils.config_loader import ConfigLoader

async def main():
    """Example usage of the Database Agent."""
    
    # Load configuration
    config = ConfigLoader.load_config("config/llm_config.yaml")
    
    # Initialize agent
    print("Initializing Database Agent...")
    agent = DatabaseAgent(config)
    
    # Health check
    print("\nPerforming health check...")
    health = await agent.health_check()
    print(f"Health status: {health['status']}")
    
    if health['status'] != 'healthy':
        print("Agent is not healthy. Exiting.")
        return
    
    # Test SQL generation
    test_prompts = [
        "Show me all users",
        "Get orders from last month",
        "Users who made orders",
        "Count of orders per user"
    ]
    
    print("\nTesting SQL generation...")
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        try:
            result = await agent.generate_sql_query(prompt)
            if result.get("error"):
                print(f"Error: {result['error']}")
            else:
                print(f"SQL: {result['sql_query']}")
                print(f"Explanation: {result['explanation']}")
        except Exception as e:
            print(f"Exception: {e}")
    
    # Show available tools
    print("\nAvailable tools:")
    tools = agent.get_available_tools()
    for tool in tools['tools']:
        print(f"- {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    asyncio.run(main()) 