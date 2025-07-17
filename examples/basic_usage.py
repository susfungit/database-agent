#!/usr/bin/env python3
"""
Basic usage example for the Database Agent MCP Server - Phase 2A.
Demonstrates SQL generation, schema integration, and health monitoring.
"""

import sys
import os
import asyncio
import json

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database_agent.agent import DatabaseAgent
from src.database_agent.schema_manager import SchemaManager
from src.utils.config_loader import ConfigLoader

async def main():
    """Example usage of the Database Agent with schema integration."""
    print("🚀 Database Agent MCP Server - Phase 2A Example")
    print("=" * 50)
    print("\n📋 Loading configuration...")
    config = ConfigLoader.load_config("config/llm_config.yaml")
    
    # Initialize agent
    print("🔧 Initializing Database Agent...")
    agent = DatabaseAgent(config)
    
    # Health check
    print("\n🏥 Performing health check...")
    health = await agent.health_check()
    print(f"Agent Health Status: {health['status']}")
    
    if health['status'] != 'healthy':
        print("❌ Agent is not healthy. Exiting.")
        return
    
    # Schema integration check
    print("\n🧩 Checking schema integration...")
    schema_manager = SchemaManager(config)
    schema_health = await schema_manager.health_check()
    print(f"Schema Health Status: {schema_health['status']}")
    
    if schema_health['status'] == 'healthy':
        schema_summary = schema_health['schema_summary']
        print(f"📊Schema Summary:")
        print(f"   - Tables: {schema_summary.get('tables', 0)}")
        print(f"   - Relationships: {schema_summary.get('relationships', 0)}")
        print(f"   - Last Refresh: {schema_summary.get('last_refresh', 'Never')}")
        print(f"  - Cache Valid: {schema_summary.get('cache_valid', False)}")
    elif schema_health['status'] == 'disabled':
        print("ℹ️  Schema integration is disabled in configuration")
    else:
        print(f"⚠️  Schema integration issue: {schema_health.get('error', 'Unknown error')}")   
    # Test SQL generation with various prompts
    test_prompts = [
        "Show me all users",
        "Get orders from last month",
        "Users who made orders",
        "Count of orders per user",
        "Find products with highest sales",
        "List customers with no orders"
    ]
    
    print("\n🔍 Testing SQL generation...")
    print("-" * 30)
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Prompt: {prompt}")
        try:
            result = await agent.generate_sql_query(prompt)
            
            if result.get("error"):
                print(f"   ❌ Error: {result['error']}")
            else:
                print(f"  ✅ SQL: {result['sql_query']}")            
                print(f"   📝 Explanation: {result['explanation']}")
                print(f"   ⏰Timestamp: {result['timestamp']}")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")  # Show available tools
    print("\n🛠️  Available MCP Tools:")
    print("-" * 30)
    tools = agent.get_available_tools()
    for tool in tools['tools']:
        print(f"   • {tool['name']}: {tool['description']}")
        if 'inputSchema' in tool:
            print(f"     Input Schema: {json.dumps(tool['inputSchema'], indent=6)}")
    
    # Schema context example (if schema is available)
    if schema_health['status'] == 'healthy':
        print("\n📋 Schema Context Example:")
        print("-" * 30)
        try:
            schema_context = await schema_manager.get_schema_context("Show me all users")
            print(f"   Tables available: {len(schema_context.get('tables'))}")
            print(f"   Relationships available: {len(schema_context.get('relationships', []))}")
            
            if schema_context.get('tables'):
                print("   Sample tables:")
                for table in schema_context['tables'][:3]:  # Show first 3 tables
                    print(f"     - {table['name']} ({len(table.get('columns', []))})")
        except Exception as e:
            print(f"   ⚠️  Could not retrieve schema context: {e}")
    
    # Configuration summary
    print("\n⚙️  Configuration Summary:")
    print("-" * 30)
    llm_config = config.get('llm', {})
    schema_config = config.get('schema', {})
    
    print(f"   LLM Provider: {llm_config.get('provider', 'Not configured')}")
    print(f"   LLM Model: {llm_config.get('model', 'Not configured')}")
    print(f"   Schema Enabled: {schema_config.get('enabled', False)}")
    if schema_config.get('enabled'):
        print(f"   Database URL: {schema_config.get('database_url', 'Not configured')}")
        print(f"   Refresh Interval: {schema_config.get('refresh_interval', 3600)} seconds")
    
    print("\n✅ Example completed successfully!") 
    print("\n💡 Next Steps:")
    print("   • Configure a real database URL in config/llm_config.yaml")
    print("   • Enable schema integration for schema-aware SQL generation")
    print("   • Try the FastAPI server: python src/mcp_server.py")
    print("   • Check the API documentation at http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")    
        print("Please check your configuration and dependencies.") 