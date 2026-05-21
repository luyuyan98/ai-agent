# AI Agent 技术栈架构文档

## 🏛️ 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│                  (examples/full_stack_demo.py)               │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
┌───────▼────────┐              ┌────────▼──────────┐
│   Direct Use   │              │  Orchestrator     │
│  (单个Agent)    │              │  (多Agent协作)     │
└───────┬────────┘              └────────┬──────────┘
        │                                │
        │                        ┌───────▼────────┐
        │                        │ Task           │
        │                        │ Decomposer     │
        │                        └───────┬────────┘
        │                                │
        └────────┬───────────────────────┘
                 │
    ┌────────────┼────────────┬────────────────┐
    │            │            │                │
┌───▼────┐ ┌────▼─────┐ ┌───▼──────┐ ┌──────▼──────┐
│Chat    │ │LangChain │ │Advanced  │ │Reasoning    │
│Agent   │ │Agent     │ │Agent     │ │Agent        │
└───┬────┘ └────┬─────┘ └───┬──────┘ └──────┬──────┘
    │           │            │               │
    │      ┌────▼────────────▼───────────────▼──────┐
    │      │         LangChain Framework             │
    │      │  - ChatOpenAI                           │
    │      │  - Prompts & Chains                     │
    │      │  - Agent Executor                       │
    │      │  - Memory Management                    │
    │      └────┬────────────────────────────────────┘
    │           │
    │      ┌────▼────────────────┐
    │      │   Tool System       │
    │      │  - Calculator       │
    │      │  - MCP Tools        │
    │      │  - Custom Tools     │
    │      └────┬────────────────┘
    │           │
    │      ┌────▼────────────────┐
    │      │   LLM Backend       │
    │      │  (OpenAI API)       │
    │      └─────────────────────┘
    │
    └─────────────────────────────────┐
                                      │
                              ┌───────▼────────┐
                              │ Configuration  │
                              │ - .env         │
                              │ - settings.py  │
                              └────────────────┘
```

## 📦 模块依赖关系

```
agents/
├── base_agent.py (抽象基类)
│   ├── chat_agent.py (基础实现)
│   ├── langchain_agent.py (LangChain集成)
│   │   └── advanced_agent.py (高级功能)
│   └── agent_orchestrator.py (编排器)
│       └── TaskDecomposer (任务分解)

tools/
├── calculator.py (计算工具)
└── mcp_tools.py (MCP工具集成)
    ├── MCPServerManager (服务器管理)
    ├── MCPToolWrapper (工具包装)
    └── MCPClient (客户端)

config/
└── settings.py (配置管理)
```

## 🔄 数据流

### 1. 简单对话流程

```
User Input
    ↓
ChatAgent.process()
    ↓
Add to History
    ↓
OpenAI API Call
    ↓
Get Response
    ↓
Add to History
    ↓
Return to User
```

### 2. 工具调用流程

```
User Input
    ↓
AdvancedAgent.process()
    ↓
LLM Analyzes Intent
    ↓
Need Tool? ──── No ──→ Direct Response
    ↓ Yes
Select Tool
    ↓
Execute Tool
    ↓
Get Tool Result
    ↓
LLM Processes Result
    ↓
Generate Final Response
    ↓
Return to User
```

### 3. 多Agent协作流程

```
Complex Task
    ↓
AgentOrchestrator
    ↓
Task Decomposer (可选)
    ↓
Split into Subtasks
    ↓
Route to Agents ──→ Agent 1 processes
    │                   ↓
    │               Agent 2 processes
    │                   ↓
    │               Agent N processes
    ↓
Collect Results
    ↓
Aggregate/Sequence
    ↓
Return Final Result
```

### 4. MCP工具集成流程

```
User Request
    ↓
Agent with MCP Tools
    ↓
LLM Decides to Use MCP Tool
    ↓
MCPServerManager
    ↓
Discover Available Servers
    ↓
Load Tool Definitions
    ↓
MCPToolWrapper
    ↓
Convert to LangChain Format
    ↓
Execute via MCP Protocol
    ↓
Return Result
    ↓
LLM Interprets Result
    ↓
Generate Response
```

## 🎯 核心设计模式

### 1. 策略模式 (Strategy Pattern)
不同的 Agent 类型提供不同的处理策略：
- `ChatAgent`: 简单对话策略
- `LangChainAgent`: LangChain链式策略
- `AdvancedAgent`: 工具增强策略
- `ReasoningAgent`: 分步推理策略

### 2. 组合模式 (Composite Pattern)
`AgentOrchestrator` 组合多个 Agent，统一接口进行调度。

### 3. 适配器模式 (Adapter Pattern)
`MCPToolWrapper` 将 MCP 工具适配为 LangChain 工具格式。

### 4. 模板方法模式 (Template Method Pattern)
`BaseAgent` 定义处理流程模板，子类实现具体逻辑。

### 5. 工厂模式 (Factory Pattern)
`load_mcp_tools()` 作为工厂函数创建工具实例。

## 🔑 关键技术点

### 1. LangChain 集成

```python
# 提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])

# 链式调用
chain = prompt | llm

# Agent Executor
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

### 2. 记忆管理

```python
class MemoryManager:
    - ConversationBufferMemory (LangChain)
    - 最大轮数限制
    - 上下文保存和检索
```

### 3. 工具系统

```python
# 工具定义格式
{
    "name": "工具名称",
    "func": 可调用函数,
    "description": "工具描述"
}

# LangChain Tool 转换
Tool(name=..., func=..., description=...)
```

### 4. MCP 协议支持

```python
# 服务器发现
MCPServerManager._discover_servers()

# 工具加载
MCPServerManager._load_tools()

# 工具包装
MCPToolWrapper.to_langchain_tool()
```

## 🚀 扩展点

### 1. 添加新 Agent 类型

```python
from agents.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def process(self, message: str) -> str:
        # 自定义实现
        pass
```

### 2. 添加工具

```python
def new_tool(param: str) -> str:
    """工具描述"""
    return result

# 注册到 Agent
agent.add_tool({
    "name": "新工具",
    "func": new_tool,
    "description": "描述"
})
```

### 3. 自定义编排策略

```python
class CustomOrchestrator(AgentOrchestrator):
    def custom_routing_strategy(self, task: str) -> str:
        # 自定义路由逻辑
        pass
```

### 4. 集成其他 LLM

```python
# 替换 ChatOpenAI 为其他 LLM
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-2")
```

## 📊 性能考虑

### 1. 并发处理
- 使用异步版本的 LangChain (`alangchain`)
- 批量处理多个请求

### 2. 缓存策略
- 缓存常见问题的回答
- 缓存工具执行结果

### 3. 记忆优化
- 限制历史长度
- 使用摘要记忆
- 定期清理无用上下文

### 4. 工具调用优化
- 预加载常用工具
- 懒加载重型工具
- 并行执行独立工具

## 🔒 安全考虑

1. **API Key 管理**: 使用环境变量，不硬编码
2. **工具沙箱**: 限制工具的执行权限
3. **输入验证**: 验证用户输入和工具参数
4. **速率限制**: 防止 API 滥用
5. **错误处理**: 捕获并妥善处理异常

## 📈 监控与日志

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.info(f"Processing message: {message}")
logger.debug(f"Tool result: {result}")
```

## 🎓 最佳实践

1. **单一职责**: 每个 Agent 专注于特定任务
2. **松耦合**: Agent 之间通过编排器交互
3. **可配置**: 使用配置文件管理参数
4. **可测试**: 编写单元测试
5. **文档化**: 清晰的注释和文档
6. **错误处理**: 完善的异常处理机制
7. **可扩展**: 预留扩展接口
