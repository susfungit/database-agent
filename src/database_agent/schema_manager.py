import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

class SchemaManager:
    """Manages database schema information and provides context for SQL generation."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.schema_cache = {}
        self.last_refresh = None
        self.refresh_interval = config.get("schema", {}).get("refresh_interval", 3600)  # 1 hour default
        self.schema_enabled = config.get("schema", {}).get("enabled", False)
        self.graph_builder = None
        self.schema_graph = None
        if self.schema_enabled:
            self._initialize_schema()
        else:
            self.logger.info("Schema integration disabled in config")

    def _initialize_schema(self):
        try:
            from schema_graph_builder import SchemaGraphBuilder
            schema_config = self.config.get("schema", {})
            database_url = schema_config.get("database_url")
            if not database_url:
                self.logger.warning("No database_url provided in schema config")
                return
            self.graph_builder = SchemaGraphBuilder(database_url)
            self.logger.info("Schema graph builder initialized successfully")
            self._load_schema()
        except ImportError as e:
            self.logger.error(f"Failed to import schema-graph-builder: {e}")
            self.logger.info("Please install with: pip install -e ../schema-graph-builder")
            self.schema_enabled = False
        except Exception as e:
            self.logger.error(f"Failed to initialize schema: {e}")
            self.schema_enabled = False

    def _load_schema(self):
        try:
            if not self.graph_builder:
                return
            self.schema_graph = self.graph_builder.build_graph()
            tables = self._extract_tables()
            relationships = self._extract_relationships()
            self.schema_cache = {
                "tables": tables,
                "relationships": relationships,
                "metadata": {
                    "loaded_at": datetime.now().isoformat(),
                    "table_count": len(tables),
                    "relationship_count": len(relationships)
                }
            }
            self.last_refresh = datetime.now()
            self.logger.info(f"Schema loaded: {len(tables)} tables, {len(relationships)} relationships")
        except Exception as e:
            self.logger.error(f"Failed to load schema: {e}")
            self.schema_cache = {}

    def _extract_tables(self) -> List[Dict[str, Any]]:
        tables = []
        try:
            for table_name, table_info in self.schema_graph.get_tables().items():
                tables.append({
                    "name": table_name,
                    "columns": list(table_info.get("columns", {}).keys()),
                    "primary_key": table_info.get("primary_key"),
                    "indexes": table_info.get("indexes", []),
                    "row_count": table_info.get("row_count", 0)
                })
        except Exception as e:
            self.logger.error(f"Failed to extract tables: {e}")
        return tables

    def _extract_relationships(self) -> List[Dict[str, Any]]:
        relationships = []
        try:
            for rel in self.schema_graph.get_relationships():
                relationships.append({
                    "from_table": rel.get("from_table"),
                    "to_table": rel.get("to_table"),
                    "from_column": rel.get("from_column"),
                    "to_column": rel.get("to_column"),
                    "type": rel.get("type", "foreign_key"),
                    "confidence": rel.get("confidence", 1.0)
                })
        except Exception as e:
            self.logger.error(f"Failed to extract relationships: {e}")
        return relationships

    async def get_schema_context(self, prompt: str) -> Dict[str, Any]:
        if not self.schema_enabled:
            return {}
        if self._should_refresh_schema():
            await self._refresh_schema_async()
        # For now, just return all tables and relationships
        return {
            "tables": self.schema_cache.get("tables", []),
            "relationships": self.schema_cache.get("relationships", [])
        }

    def _should_refresh_schema(self) -> bool:
        if not self.last_refresh:
            return True
        time_since_refresh = datetime.now() - self.last_refresh
        return time_since_refresh.total_seconds() > self.refresh_interval

    async def _refresh_schema_async(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._load_schema)

    def get_schema_summary(self) -> Dict[str, Any]:
        if not self.schema_enabled:
            return {"enabled": False, "message": "Schema integration disabled"}
        return {
            "enabled": True,
            "tables": len(self.schema_cache.get("tables", [])),
            "relationships": len(self.schema_cache.get("relationships", [])),
            "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
            "cache_valid": not self._should_refresh_schema()
        }

    async def health_check(self) -> Dict[str, Any]:
        try:
            summary = self.get_schema_summary()
            return {
                "status": "healthy" if summary.get("enabled", False) else "disabled",
                "schema_summary": summary,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            } 