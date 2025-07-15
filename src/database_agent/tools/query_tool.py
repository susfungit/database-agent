import logging
from typing import Dict, Any
from datetime import datetime
from ..llm_integration import LLMIntegration

class QueryTool:
    """MCP tool for SQL query generation."""
    
    def __init__(self, llm_integration: LLMIntegration):
        self.llm_integration = llm_integration
        self.logger = logging.getLogger(__name__)
    
    async def generate_query(self, prompt: str) -> Dict[str, Any]:
        """Generate SQL query from natural language prompt."""
        try:
            self.logger.info(f"Generating SQL for prompt: {prompt[:50]}...")
            
            # Generate SQL using LLM
            sql_query = await self.llm_integration.generate_sql(prompt)
            
            # Format response
            result = {
                "sql_query": sql_query,
                "explanation": f"Generated SQL query for: {prompt}",
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"Query generated successfully: {sql_query[:50]}...")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in query tool: {e}")
            return {
                "error": str(e),
                "sql_query": None,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_tool_schema(self) -> Dict[str, Any]:
        """Get MCP tool schema definition."""
        return {
            "name": "generate_sql_query",
            "description": "Generate SQL queries from natural language descriptions",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Natural language description of the desired SQL query"
                    }
                },
                "required": ["prompt"]
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "Generated SQL query"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Explanation of the generated query"
                    },
                    "error": {
                        "type": "string",
                        "description": "Error message if generation failed"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Original prompt"
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "Timestamp of generation"
                    }
                }
            }
        } 