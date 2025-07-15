# Database Agent Architecture Diagram

## System Overview (Phase 1 - Current State)

**Note**: This diagram shows the planned full architecture. Currently, only the SQL generation components are implemented in Phase 1.

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface Layer"
        UI[Web/Mobile UI]
        UI_PROMPT[User Natural Language Prompt]
    end

    %% MCP Server Layer
    subgraph "MCP Server Layer"
        MCP_SERVER[MCP Server]
        DB_AGENT[Database Agent]
        LLM_INTEGRATION[LLM Integration]
        QUERY_GENERATOR[Query Generator]
        QUERY_VALIDATOR[Query Validator]
        RESULT_PROCESSOR[Result Processor]
    end

    %% Schema Graph Layer
    subgraph "Schema Graph Layer"
        SCHEMA_BUILDER[Schema Graph Builder]
        SCHEMA_CACHE[Schema Cache]
        RELATIONSHIP_GRAPH[Relationship Graph]
        METADATA_STORE[Metadata Store]
    end

    %% Database Layer
    subgraph "Database Layer"
        DB1[(PostgreSQL)]
        DB2[(MySQL)]
        DB3[(SQL Server)]
        DB4[(Oracle)]
        DB5[(Other DBs)]
    end

    %% External Services
    subgraph "External Services"
        LLM_SERVICE[LLM Service<br/>OpenAI/Anthropic/etc.]
        AUTH_SERVICE[Authentication Service]
    end

    %% Data Flow
    UI_PROMPT --> UI
    UI --> MCP_SERVER
    MCP_SERVER --> DB_AGENT
    DB_AGENT --> LLM_INTEGRATION
    LLM_INTEGRATION --> LLM_SERVICE
    LLM_INTEGRATION --> RELATIONSHIP_GRAPH
    LLM_INTEGRATION --> QUERY_GENERATOR
    QUERY_GENERATOR --> QUERY_VALIDATOR
    QUERY_VALIDATOR --> DB1
    QUERY_VALIDATOR --> DB2
    QUERY_VALIDATOR --> DB3
    QUERY_VALIDATOR --> DB4
    QUERY_VALIDATOR --> DB5
    DB1 --> RESULT_PROCESSOR
    DB2 --> RESULT_PROCESSOR
    DB3 --> RESULT_PROCESSOR
    DB4 --> RESULT_PROCESSOR
    DB5 --> RESULT_PROCESSOR
    RESULT_PROCESSOR --> MCP_SERVER
    MCP_SERVER --> UI

    %% Schema Building Flow
    DB1 --> SCHEMA_BUILDER
    DB2 --> SCHEMA_BUILDER
    DB3 --> SCHEMA_BUILDER
    DB4 --> SCHEMA_BUILDER
    DB5 --> SCHEMA_BUILDER
    SCHEMA_BUILDER --> SCHEMA_CACHE
    SCHEMA_BUILDER --> RELATIONSHIP_GRAPH
    SCHEMA_BUILDER --> METADATA_STORE
    RELATIONSHIP_GRAPH --> LLM_INTEGRATION

    %% Authentication
    AUTH_SERVICE --> MCP_SERVER
    AUTH_SERVICE --> DB_AGENT

    %% Styling
    classDef uiLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef mcpLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef schemaLayer fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef dbLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef externalLayer fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class UI,UI_PROMPT uiLayer
    class MCP_SERVER,DB_AGENT,LLM_INTEGRATION,QUERY_GENERATOR,QUERY_VALIDATOR,RESULT_PROCESSOR mcpLayer
    class SCHEMA_BUILDER,SCHEMA_CACHE,RELATIONSHIP_GRAPH,METADATA_STORE schemaLayer
    class DB1,DB2,DB3,DB4,DB5 dbLayer
    class LLM_SERVICE,AUTH_SERVICE externalLayer
```

## Detailed Component Architecture

### Phase 1 Implementation Status
- **✅ Implemented**: MCP Server, LLM Integration, Basic Query Tool
- **🔄 Planned**: Schema Graph Engine, Query Execution, Result Processing
- **📋 Future**: Memory System, Planning Engine, Autonomous Decision Making

```mermaid
graph LR
    subgraph "Database Agent Core"
        subgraph "Input Processing"
            PROMPT_PARSER[Prompt Parser]
            CONTEXT_BUILDER[Context Builder]
        end

        subgraph "Query Generation"
            LLM_WRAPPER[LLM Wrapper]
            GRAPH_NAVIGATOR[Graph Navigator]
            SQL_BUILDER[SQL Builder]
        end

        subgraph "Query Execution"
            QUERY_EXECUTOR[Query Executor]
            CONNECTION_POOL[Connection Pool]
            TRANSACTION_MGR[Transaction Manager]
        end

        subgraph "Result Handling"
            RESULT_FORMATTER[Result Formatter]
            ERROR_HANDLER[Error Handler]
            EXPLANATION_GENERATOR[Explanation Generator]
        end
    end

    subgraph "Schema Graph Engine"
        subgraph "Graph Management"
            GRAPH_LOADER[Graph Loader]
            GRAPH_UPDATER[Graph Updater]
            GRAPH_QUERY[Graph Query Engine]
        end

        subgraph "Relationship Analysis"
            FK_DETECTOR[FK Detector]
            RELATIONSHIP_SCORER[Relationship Scorer]
            PATH_FINDER[Path Finder]
        end
    end

    subgraph "MCP Integration"
        MCP_HANDLER[MCP Handler]
        TOOL_REGISTRY[Tool Registry]
        RESPONSE_BUILDER[Response Builder]
    end

    %% Data Flow
    PROMPT_PARSER --> CONTEXT_BUILDER
    CONTEXT_BUILDER --> GRAPH_NAVIGATOR
    GRAPH_NAVIGATOR --> LLM_WRAPPER
    LLM_WRAPPER --> SQL_BUILDER
    SQL_BUILDER --> QUERY_EXECUTOR
    QUERY_EXECUTOR --> CONNECTION_POOL
    CONNECTION_POOL --> TRANSACTION_MGR
    TRANSACTION_MGR --> RESULT_FORMATTER
    RESULT_FORMATTER --> ERROR_HANDLER
    ERROR_HANDLER --> EXPLANATION_GENERATOR
    EXPLANATION_GENERATOR --> MCP_HANDLER

    %% Graph Integration
    GRAPH_LOADER --> GRAPH_QUERY
    GRAPH_UPDATER --> FK_DETECTOR
    FK_DETECTOR --> RELATIONSHIP_SCORER
    RELATIONSHIP_SCORER --> PATH_FINDER
    PATH_FINDER --> GRAPH_NAVIGATOR

    %% MCP Integration
    MCP_HANDLER --> TOOL_REGISTRY
    TOOL_REGISTRY --> RESPONSE_BUILDER

    %% Styling
    classDef coreLayer fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef graphLayer fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef mcpLayer fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px

    class PROMPT_PARSER,CONTEXT_BUILDER,LLM_WRAPPER,GRAPH_NAVIGATOR,SQL_BUILDER,QUERY_EXECUTOR,CONNECTION_POOL,TRANSACTION_MGR,RESULT_FORMATTER,ERROR_HANDLER,EXPLANATION_GENERATOR coreLayer
    class GRAPH_LOADER,GRAPH_UPDATER,GRAPH_QUERY,FK_DETECTOR,RELATIONSHIP_SCORER,PATH_FINDER graphLayer
    class MCP_HANDLER,TOOL_REGISTRY,RESPONSE_BUILDER mcpLayer
```

## Data Flow Sequence

### Phase 1: Current Implementation
```mermaid
sequenceDiagram
    participant U as User
    participant MCP as MCP Server
    participant AGENT as Database Agent
    participant LLM as LLM Service

    U->>MCP: Send natural language prompt
    MCP->>AGENT: Route to database agent
    AGENT->>LLM: Send prompt for SQL generation
    LLM-->>AGENT: Return SQL query
    AGENT-->>MCP: Return SQL + explanation
    MCP-->>U: Display generated SQL
```

### Phase 2+: Planned Full Flow
```mermaid
sequenceDiagram
    participant U as User
    participant UI as UI Interface
    participant MCP as MCP Server
    participant AGENT as Database Agent
    participant LLM as LLM Service
    participant GRAPH as Schema Graph
    participant DB as Database

    U->>UI: Enter natural language prompt
    UI->>MCP: Send prompt via MCP protocol
    MCP->>AGENT: Route to database agent
    
    AGENT->>GRAPH: Load schema graph
    GRAPH-->>AGENT: Return graph data
    
    AGENT->>LLM: Send prompt + schema context
    LLM-->>AGENT: Return SQL query
    
    AGENT->>AGENT: Validate query against schema
    AGENT->>DB: Execute validated query
    DB-->>AGENT: Return results
    
    AGENT->>AGENT: Format results
    AGENT->>AGENT: Generate explanation
    AGENT-->>MCP: Return formatted response
    MCP-->>UI: Send response via MCP protocol
    UI-->>U: Display results and explanation
```

## Schema Graph Structure

```mermaid
graph TD
    subgraph "Schema Graph Components"
        subgraph "Nodes (Tables)"
            TABLE1[Table: users<br/>Columns: 5<br/>Primary Key: user_id]
            TABLE2[Table: orders<br/>Columns: 8<br/>Primary Key: order_id]
            TABLE3[Table: products<br/>Columns: 6<br/>Primary Key: product_id]
            TABLE4[Table: order_items<br/>Columns: 4<br/>Primary Key: item_id]
        end

        subgraph "Edges (Relationships)"
            EDGE1[user_id → users.user_id<br/>Confidence: 0.95]
            EDGE2[order_id → orders.order_id<br/>Confidence: 0.98]
            EDGE3[product_id → products.product_id<br/>Confidence: 0.92]
        end

        subgraph "Metadata"
            META1[Column Types<br/>Constraints<br/>Indexes]
            META2[Table Sizes<br/>Row Counts<br/>Last Updated]
            META3[Access Patterns<br/>Query History<br/>Performance Metrics]
        end
    end

    %% Relationships
    TABLE2 -.->|EDGE1| TABLE1
    TABLE4 -.->|EDGE2| TABLE2
    TABLE4 -.->|EDGE3| TABLE3

    %% Metadata connections
    TABLE1 -.-> META1
    TABLE2 -.-> META1
    TABLE3 -.-> META1
    TABLE4 -.-> META1

    TABLE1 -.-> META2
    TABLE2 -.-> META2
    TABLE3 -.-> META2
    TABLE4 -.-> META2

    TABLE1 -.-> META3
    TABLE2 -.-> META3
    TABLE3 -.-> META3
    TABLE4 -.-> META3

    %% Styling
    classDef tableNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef edgeNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef metaNode fill:#e8f5e8,stroke:#388e3c,stroke-width:2px

    class TABLE1,TABLE2,TABLE3,TABLE4 tableNode
    class EDGE1,EDGE2,EDGE3 edgeNode
    class META1,META2,META3 metaNode
```

## Security and Access Control

```mermaid
graph TB
    subgraph "Security Layer"
        AUTH[Authentication]
        AUTHORIZATION[Authorization]
        AUDIT[Audit Logging]
        ENCRYPTION[Encryption]
    end

    subgraph "Access Control"
        ROLE_MANAGER[Role Manager]
        PERMISSION_CHECKER[Permission Checker]
        QUERY_FILTER[Query Filter]
        RESULT_FILTER[Result Filter]
    end

    subgraph "Data Protection"
        PII_DETECTOR[PII Detector]
        SENSITIVE_DATA_FILTER[Sensitive Data Filter]
        DATA_MASKING[Data Masking]
    end

    %% Security Flow
    AUTH --> AUTHORIZATION
    AUTHORIZATION --> ROLE_MANAGER
    ROLE_MANAGER --> PERMISSION_CHECKER
    PERMISSION_CHECKER --> QUERY_FILTER
    QUERY_FILTER --> PII_DETECTOR
    PII_DETECTOR --> SENSITIVE_DATA_FILTER
    SENSITIVE_DATA_FILTER --> DATA_MASKING
    DATA_MASKING --> RESULT_FILTER
    RESULT_FILTER --> AUDIT
    AUDIT --> ENCRYPTION

    %% Styling
    classDef securityLayer fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef accessLayer fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef protectionLayer fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px

    class AUTH,AUTHORIZATION,AUDIT,ENCRYPTION securityLayer
    class ROLE_MANAGER,PERMISSION_CHECKER,QUERY_FILTER,RESULT_FILTER accessLayer
    class PII_DETECTOR,SENSITIVE_DATA_FILTER,DATA_MASKING protectionLayer
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB_UI[Web UI]
        MOBILE_UI[Mobile UI]
        CLI_CLIENT[CLI Client]
    end

    subgraph "Load Balancer"
        LB[Load Balancer<br/>HAProxy/Nginx]
    end

    subgraph "Application Layer"
        MCP_SERVER1[MCP Server 1]
        MCP_SERVER2[MCP Server 2]
        MCP_SERVER3[MCP Server 3]
    end

    subgraph "Database Agent Layer"
        AGENT1[Database Agent 1]
        AGENT2[Database Agent 2]
        AGENT3[Database Agent 3]
    end

    subgraph "Cache Layer"
        REDIS[Redis Cache]
        SCHEMA_CACHE[Schema Cache]
    end

    subgraph "Database Layer"
        MASTER_DB[(Master DB)]
        SLAVE_DB1[(Slave DB 1)]
        SLAVE_DB2[(Slave DB 2)]
    end

    subgraph "Monitoring"
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana]
        LOGS[Log Aggregation]
    end

    %% Connections
    WEB_UI --> LB
    MOBILE_UI --> LB
    CLI_CLIENT --> LB
    
    LB --> MCP_SERVER1
    LB --> MCP_SERVER2
    LB --> MCP_SERVER3
    
    MCP_SERVER1 --> AGENT1
    MCP_SERVER2 --> AGENT2
    MCP_SERVER3 --> AGENT3
    
    AGENT1 --> REDIS
    AGENT2 --> REDIS
    AGENT3 --> REDIS
    
    AGENT1 --> SCHEMA_CACHE
    AGENT2 --> SCHEMA_CACHE
    AGENT3 --> SCHEMA_CACHE
    
    AGENT1 --> MASTER_DB
    AGENT2 --> MASTER_DB
    AGENT3 --> MASTER_DB
    
    MASTER_DB --> SLAVE_DB1
    MASTER_DB --> SLAVE_DB2
    
    AGENT1 --> PROMETHEUS
    AGENT2 --> PROMETHEUS
    AGENT3 --> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    AGENT1 --> LOGS
    AGENT2 --> LOGS
    AGENT3 --> LOGS

    %% Styling
    classDef clientLayer fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef appLayer fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef agentLayer fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef cacheLayer fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef dbLayer fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef monitoringLayer fill:#f1f8e9,stroke:#558b2f,stroke-width:2px

    class WEB_UI,MOBILE_UI,CLI_CLIENT clientLayer
    class LB,MCP_SERVER1,MCP_SERVER2,MCP_SERVER3 appLayer
    class AGENT1,AGENT2,AGENT3 agentLayer
    class REDIS,SCHEMA_CACHE cacheLayer
    class MASTER_DB,SLAVE_DB1,SLAVE_DB2 dbLayer
    class PROMETHEUS,GRAFANA,LOGS monitoringLayer
``` 