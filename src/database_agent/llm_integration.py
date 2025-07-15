import logging
from typing import Dict, Any, List
from llmwrapper import get_llm

class LLMIntegration:
    """Integration with your existing llmwrapper."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM using your existing llmwrapper."""
        try:
            llm_config = self.config.get("llm", {})
            provider = llm_config.get("provider", "openai")
            
            # Use your existing llmwrapper
            llm = get_llm(provider, llm_config)
            self.logger.info(f"LLM initialized with provider: {provider}")
            return llm
        except ImportError as e:
            self.logger.error(f"Failed to import llmwrapper: {e}")
            raise Exception("llmwrapper not available. Please install with: pip install -e ../llmwrapper")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    async def generate_sql(self, prompt: str) -> str:
        """Generate SQL using LLM."""
        try:
            system_prompt = self._get_sql_system_prompt()
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # Handle both sync and async LLM calls
            if hasattr(self.llm, 'chat') and callable(getattr(self.llm, 'chat')):
                response = self.llm.chat(messages)
            else:
                raise Exception("LLM chat method not available")
                
            self.logger.info("SQL generated successfully")
            return response
        except Exception as e:
            self.logger.error(f"Error generating SQL with LLM: {e}")
            raise
    
    def _get_sql_system_prompt(self) -> str:
        """Get the system prompt for SQL generation."""
        return """
        You are a SQL expert. Your task is to generate SQL queries based on user requests.
        
        Guidelines:
        1. Generate only SQL queries, no explanations in the response
        2. Use standard SQL syntax
        3. Assume common table names like users, orders, products, etc.
        4. Use proper JOINs when multiple tables are needed
        5. Include appropriate WHERE clauses for filtering
        6. Use appropriate date functions for time-based queries
        
        Examples:
        - "Show me all users" → "SELECT * FROM users;"
        - "Get orders from last month" → "SELECT * FROM orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH);"
        - "Users who made orders" → "SELECT u.* FROM users u JOIN orders o ON u.user_id = o.user_id;"
        - "Count of orders per user" → "SELECT u.user_id, u.name, COUNT(o.order_id) as order_count FROM users u LEFT JOIN orders o ON u.user_id = o.user_id GROUP BY u.user_id, u.name;"
        """
    
    async def health_check(self) -> Dict[str, Any]:
        """Check LLM health."""
        try:
            # Simple test query
            if hasattr(self.llm, 'chat') and callable(getattr(self.llm, 'chat')):
                test_response = self.llm.chat([
                    {"role": "user", "content": "Generate: SELECT 1;"}
                ])
                return {"status": "healthy", "test_response": test_response}
            else:
                return {"status": "unhealthy", "error": "LLM chat method not available"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)} 