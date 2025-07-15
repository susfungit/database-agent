import pytest
from unittest.mock import Mock, patch
from src.database_agent.agent import DatabaseAgent

class TestDatabaseAgent:
    @pytest.fixture
    def mock_config(self):
        return {
            "llm": {
                "provider": "openai",
                "model": "gpt-4",
                "api_key": "test-key"
            }
        }
    
    @pytest.fixture
    def agent(self, mock_config):
        with patch('src.database_agent.llm_integration.get_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_llm.chat.return_value = "SELECT * FROM users;"
            mock_get_llm.return_value = mock_llm
            
            return DatabaseAgent(mock_config)
    
    @pytest.mark.asyncio
    async def test_generate_sql_query(self, agent):
        prompt = "Show me all users"
        result = await agent.generate_sql_query(prompt)
        
        assert "sql_query" in result
        assert result["sql_query"] is not None
        assert "SELECT" in result["sql_query"].upper()
        assert result["prompt"] == prompt
    
    @pytest.mark.asyncio
    async def test_health_check(self, agent):
        result = await agent.health_check()
        
        assert result["status"] == "healthy"
        assert "llm_status" in result
        assert "timestamp" in result
        assert result["version"] == "1.0.0"
    
    def test_get_available_tools(self, agent):
        tools = agent.get_available_tools()
        
        assert "tools" in tools
        assert len(tools["tools"]) == 1
        assert tools["tools"][0]["name"] == "generate_sql_query"
        assert tools["version"] == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_generate_sql_query_error(self, agent):
        # Mock LLM to raise an error
        agent.llm_integration.llm.chat.side_effect = Exception("LLM Error")
        
        prompt = "Show me all users"
        result = await agent.generate_sql_query(prompt)
        
        assert "error" in result
        assert result["sql_query"] is None
        assert result["prompt"] == prompt 