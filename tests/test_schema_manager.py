import pytest
from unittest.mock import patch, MagicMock
from src.database_agent.schema_manager import SchemaManager
import asyncio

@pytest.fixture
def mock_config():
    return {
        "schema": {
            "enabled": True,
            "database_url": "sqlite:///:memory:",
            "refresh_interval": 3600
        }
    }

@pytest.fixture
def mock_schema_graph():
    mock_graph = MagicMock()
    mock_graph.get_tables.return_value = {
        "users": {"columns": {"id": {}, "name": {}}, "primary_key": "id", "indexes": [], "row_count": 10},
        "orders": {"columns": {"id": {}, "user_id": {}}, "primary_key": "id", "indexes": [], "row_count": 5}
    }
    mock_graph.get_relationships.return_value = [
        {"from_table": "orders", "to_table": "users", "from_column": "user_id", "to_column": "id", "type": "foreign_key", "confidence": 1.0}
    ]
    return mock_graph

@patch("src.database_agent.schema_manager.SchemaManager._initialize_schema")
def test_schema_manager_init(mock_init, mock_config):
    sm = SchemaManager(mock_config)
    mock_init.assert_called_once()

@patch("schema_graph_builder.SchemaGraphBuilder")
def test_load_schema(mock_builder, mock_config, mock_schema_graph):
    mock_builder.return_value.build_graph.return_value = mock_schema_graph
    sm = SchemaManager(mock_config)
    sm.graph_builder = mock_builder.return_value
    sm.schema_graph = mock_schema_graph
    sm._load_schema()
    assert "tables" in sm.schema_cache
    assert "relationships" in sm.schema_cache
    assert sm.schema_cache["tables"][0]["name"] == "users"
    assert sm.schema_cache["relationships"][0]["from_table"] == "orders"

@patch("src.database_agent.schema_manager.SchemaManager._should_refresh_schema", return_value=False)
def test_get_schema_context_no_refresh(mock_refresh, mock_config, mock_schema_graph):
    sm = SchemaManager(mock_config)
    sm.schema_enabled = True
    sm.schema_cache = {
        "tables": [{"name": "users"}],
        "relationships": [{"from_table": "orders", "to_table": "users"}]
    }
    ctx = asyncio.run(sm.get_schema_context("Show me all users"))
    assert "tables" in ctx
    assert "relationships" in ctx

@patch("src.database_agent.schema_manager.SchemaManager._should_refresh_schema", return_value=True)
@patch("src.database_agent.schema_manager.SchemaManager._refresh_schema_async")
def test_get_schema_context_with_refresh(mock_async, mock_refresh, mock_config, mock_schema_graph):
    sm = SchemaManager(mock_config)
    sm.schema_enabled = True
    sm.schema_cache = {
        "tables": [{"name": "users"}],
        "relationships": [{"from_table": "orders", "to_table": "users"}]
    }
    ctx = asyncio.run(sm.get_schema_context("Show me all users"))
    mock_async.assert_called_once()
    assert "tables" in ctx

@patch("src.database_agent.schema_manager.SchemaManager._load_schema")
def test_schema_manager_health_check(mock_load, mock_config):
    sm = SchemaManager(mock_config)
    sm.schema_enabled = True
    sm.schema_cache = {"tables": [], "relationships": []}
    sm.last_refresh = None
    result = asyncio.run(sm.health_check())
    assert "status" in result
    assert "schema_summary" in result 