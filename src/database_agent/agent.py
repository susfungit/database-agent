import logging
from typing import Dict, Any, Optional
from datetime import datetime
from .llm_integration import LLMIntegration
from .tools.query_tool import QueryTool

class DatabaseAgent:
    """Core database agent that coordinates LLM and tools."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_integration = LLMIntegration(config)
        self.query_tool = QueryTool(self.llm_integration)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Database Agent initialized successfully")
    
    async def generate_sql_query(self, prompt: str) -> Dict[str, Any]:
        """Generate SQL query from natural language prompt."""
        try:
            self.logger.info(f"Generating SQL for prompt: {prompt[:50]}...")
            result = await self.query_tool.generate_query(prompt)
            self.logger.info("SQL generation completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error generating SQL: {e}")
            return {
                "error": str(e), 
                "sql_query": None,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the agent."""
        try:
            llm_status = await self.llm_integration.health_check()
            return {
                "status": "healthy",
                "llm_status": llm_status,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get list of available MCP tools."""
        return {
            "tools": [
                {
                    "name": "generate_sql_query",
                    "description": "Generate SQL queries from natural language",
                    "schema": self.query_tool.get_tool_schema()
                }
            ],
            "version": "1.0.0"
        } 