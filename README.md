# Database Agent MCP Server - Phase 1

A natural language to SQL query generator with MCP (Model Context Protocol) server capabilities. This is Phase 1 of a planned AI agent that will eventually provide autonomous database interaction capabilities.

**Current Phase**: SQL Query Generator  
**Future Vision**: Autonomous Database AI Agent

## 🚀 Features (Phase 1)

### Current Capabilities
- **Natural Language to SQL**: Convert natural language prompts to SQL queries
- **LLMWrapper Integration**: Uses your existing `llmwrapper` for LLM interactions
- **MCP Protocol**: Implements Model Context Protocol for tool integration
- **FastAPI Server**: RESTful API endpoints for easy integration
- **Health Monitoring**: Built-in health checks and monitoring
- **Comprehensive Logging**: Detailed logging with configurable levels
- **Configuration Management**: YAML-based configuration with environment variable overrides

### Planned Features (Phase 2+)
- **Schema-Aware Generation**: Use database schema for context-aware SQL generation
- **Query Execution**: Execute generated SQL and return results
- **Autonomous Decision Making**: Plan and execute multi-step database operations
- **Memory & Learning**: Remember user preferences and learn from interactions
- **Interactive Refinement**: Ask clarifying questions and refine queries
- **Relationship Detection**: Automatic foreign key relationship inference

## 📋 Prerequisites

- Python 3.8+
- Your existing `llmwrapper` library (installed with `pip install -e ../llmwrapper`)
- Your existing `schema-graph-builder` library (installed with `pip install -e ../schema-graph-builder`)
- OpenAI API key (or other LLM provider)

## 🔧 Installation

1. **Clone and setup the project:**
```bash
# Navigate to the database-agent directory
cd database-agent

# Install dependencies
pip install -r requirements.txt

# Install your existing packages in development mode
pip install -e ../llmwrapper
pip install -e ../schema-graph-builder
```

2. **Set up environment variables:**
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your API keys
nano .env
```

3. **Configure your LLM provider:**
```yaml
# Edit config/llm_config.yaml
llm:
  provider: "openai"  # or anthropic, gemini, grok, ollama
  model: "gpt-4"      # Model name for your provider
  api_key: ""         # Will be overridden by OPENAI_API_KEY env var
```

## 🚀 Quick Start

### 1. Start the Server

```bash
# Start with default configuration
python src/mcp_server.py

# Or with custom config
python src/mcp_server.py --config config/llm_config.yaml --host 0.0.0.0 --port 8000
```

### 2. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Generate SQL query (Phase 1: SQL generation only)
curl -X POST http://localhost:8000/generate-sql \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Show me all users who made orders in the last month"}'

# Get available tools
curl http://localhost:8000/tools
```

### 3. Run the Example

```bash
# Run the basic usage example
python examples/basic_usage.py
```

### 4. What You'll Get (Phase 1)

Currently, the system will:
- ✅ Convert natural language to SQL queries
- ✅ Provide explanations of generated queries
- ✅ Handle errors gracefully
- ✅ Return structured responses

**Note**: This is Phase 1 - the system generates SQL but doesn't execute it yet. Query execution will be added in Phase 2.

## 📖 API Reference

### Endpoints

#### `GET /`
- **Description**: Server information
- **Response**: `{"message": "Database Agent MCP Server", "version": "1.0.0"}`

#### `GET /health`
- **Description**: Health check
- **Response**: Health status with LLM status and timestamp

#### `POST /generate-sql`
- **Description**: Generate SQL from natural language (Phase 1: Generation only)
- **Request Body**:
  ```json
  {
    "prompt": "Show me all users who made orders in the last month"
  }
  ```
- **Response**:
  ```json
  {
    "sql_query": "SELECT u.* FROM users u JOIN orders o ON u.user_id = o.user_id WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH);",
    "explanation": "Generated SQL query for: Show me all users who made orders in the last month",
    "prompt": "Show me all users who made orders in the last month",
    "timestamp": "2024-01-15T10:30:45.123456"
  }
  ```
- **Note**: This endpoint generates SQL but doesn't execute it. Query execution will be added in Phase 2.

#### `GET /tools`
- **Description**: Get available MCP tools
- **Response**: List of available tools with schemas

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LLM_PROVIDER` | LLM provider (openai, anthropic, etc.) | openai |
| `LLM_MODEL` | Model name | gpt-4 |
| `SERVER_HOST` | Server host | localhost |
| `SERVER_PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |

### Configuration File

Edit `config/llm_config.yaml`:

```yaml
# LLM Configuration
llm:
  provider: "openai"
  model: "gpt-4"
  api_key: ""
  timeout: 30

# Server Configuration
server:
  host: "localhost"
  port: 8000
  debug: false

# Logging Configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/database_agent.log"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_database_agent.py -v
```

## 📁 Project Structure

```
database-agent/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
├── architecture_diagram.md  # System architecture documentation
├── config/
│   └── llm_config.yaml      # Configuration file
├── src/
│   ├── mcp_server.py        # Main MCP server (FastAPI)
│   ├── database_agent/
│   │   ├── agent.py         # Core database agent (Phase 1: SQL generator)
│   │   ├── llm_integration.py # LLMWrapper integration
│   │   ├── true_agent.py    # Future: True AI agent implementation
│   │   └── tools/
│   │       └── query_tool.py # MCP query tool
│   └── utils/
│       ├── config_loader.py # Configuration management
│       └── logger.py        # Logging setup
├── tests/
│   └── test_database_agent.py # Unit tests
└── examples/
    └── basic_usage.py       # Usage example
```

### Component Status
- **✅ Production Ready**: MCP server, LLM integration, basic agent
- **🔄 In Development**: Schema integration, query execution
- **📋 Planned**: Memory system, planning engine, autonomous capabilities

## 🔍 Troubleshooting

### Common Issues

1. **LLMWrapper not found**
   ```
   ModuleNotFoundError: No module named 'llmwrapper'
   ```
   - Install llmwrapper in development mode: `pip install -e ../llmwrapper`
   - Ensure you're in the database-agent directory when running the command

2. **API Key not set**
   ```
   Failed to initialize LLM: API key not provided
   ```
   - Set `OPENAI_API_KEY` environment variable
   - Or add it to your `.env` file

3. **Port already in use**
   ```
   Error: [Errno 48] Address already in use
   ```
   - Change the port in config or use `--port` argument
   - Kill the process using the port

4. **SQL not executing**
   ```
   Note: This is expected behavior in Phase 1
   ```
   - Phase 1 only generates SQL, doesn't execute it
   - Query execution will be added in Phase 2

### Logs

Logs are written to:
- Console output
- `logs/database_agent.log` (if configured)

Check logs for detailed error information.

## 🎯 Current Limitations (Phase 1)

- **No Query Execution**: Generated SQL is not executed against databases
- **No Schema Context**: SQL generation doesn't use database schema information
- **No Memory**: Each request is processed independently
- **No Validation**: Generated SQL is not validated against actual database structure
- **No Interactive Refinement**: Cannot ask clarifying questions

These limitations will be addressed in future phases.

## 🚀 Development Roadmap

### Phase 1: SQL Query Generator ✅ (Current)
- ✅ Natural language to SQL conversion
- ✅ MCP server with REST API
- ✅ LLM integration
- ✅ Basic error handling and logging

### Phase 2: Schema-Aware Generator (Next)
- 🔄 **Schema Integration**: Use your `schema-graph-builder` for database context
- 🔄 **Relationship Detection**: Automatic foreign key relationship inference
- 🔄 **Query Validation**: Validate generated SQL against schema
- 🔄 **Enhanced Prompts**: Schema-aware SQL generation
- 🔄 **Query Execution**: Execute queries and return results

### Phase 3: Autonomous Agent (Future)
- 🔄 **Memory System**: Remember conversation history and user preferences
- 🔄 **Planning Engine**: Break complex requests into executable steps
- 🔄 **Tool Orchestration**: Multiple specialized tools beyond SQL generation
- 🔄 **Interactive Capabilities**: Ask clarifying questions when requests are ambiguous
- 🔄 **Learning & Adaptation**: Improve responses based on user feedback

### Phase 4: Full AI Agent (Vision)
- 🔄 **Autonomous Decision Making**: Plan and execute multi-step operations
- 🔄 **Context Awareness**: Understand database state and user intent
- 🔄 **Proactive Suggestions**: Suggest optimizations and insights
- 🔄 **Natural Conversation**: Maintain context across multiple interactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 