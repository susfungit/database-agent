import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database_agent.agent import DatabaseAgent
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

# Pydantic models for API
class SQLQueryRequest(BaseModel):
    prompt: str

class SQLQueryResponse(BaseModel):
    sql_query: str
    explanation: str
    prompt: str
    timestamp: str
    error: str = None

class HealthResponse(BaseModel):
    status: str
    llm_status: Dict[str, Any]
    timestamp: str
    version: str

class DatabaseAgentMCPServer:
    """Main MCP server for database agent functionality."""
    
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        self.config = ConfigLoader.load_config(config_path)
        self.logger = setup_logger(__name__, self.config.get("logging", {}))
        self.agent = DatabaseAgent(self.config)
        self.app = FastAPI(title="Database Agent MCP Server", version="1.0.0")
        self._setup_routes()
        self.logger.info("Database Agent MCP Server initialized")
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/")
        async def root():
            return {"message": "Database Agent MCP Server", "version": "1.0.0"}
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            try:
                health = await self.agent.health_check()
                return HealthResponse(**health)
            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/generate-sql", response_model=SQLQueryResponse)
        async def generate_sql_query(request: SQLQueryRequest):
            """Generate SQL query from natural language prompt."""
            try:
                result = await self.agent.generate_sql_query(request.prompt)
                
                if result.get("error"):
                    raise HTTPException(status_code=400, detail=result["error"])
                
                return SQLQueryResponse(**result)
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error generating SQL: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/tools")
        async def get_tools():
            """Get available MCP tools."""
            try:
                return self.agent.get_available_tools()
            except Exception as e:
                self.logger.error(f"Error getting tools: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start(self, host: str = None, port: int = None):
        """Start the MCP server."""
        host = host or self.config.get("server", {}).get("host", "localhost")
        port = port or self.config.get("server", {}).get("port", 8000)
        
        self.logger.info(f"Starting MCP server on {host}:{port}")
        
        import uvicorn
        config = uvicorn.Config(
            self.app,
            host=host,
            port=port,
            log_level=self.config.get("logging", {}).get("level", "info").lower()
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def stop(self):
        """Stop the MCP server."""
        self.logger.info("Stopping MCP server")
        # Add any cleanup logic here

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database Agent MCP Server")
    parser.add_argument("--config", default="config/llm_config.yaml", help="Config file path")
    parser.add_argument("--host", help="Server host")
    parser.add_argument("--port", type=int, help="Server port")
    
    args = parser.parse_args()
    
    try:
        server = DatabaseAgentMCPServer(args.config)
        asyncio.run(server.start(args.host, args.port))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        exit(1)

if __name__ == "__main__":
    main() 