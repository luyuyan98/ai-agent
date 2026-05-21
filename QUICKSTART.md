# 快速开始指南

## 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

## 2️⃣ 配置环境变量

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
LOG_LEVEL=INFO
```

## 3️⃣ 运行示例

```bash
python examples/full_stack_demo.py
```

## 4️⃣ 快速使用

### 最简单的对话 Agent

```python
from agents import ChatAgent

agent = ChatAgent(name="助手")
response = agent.process("你好！")
print(response)
```

### 使用 LangChain Agent

```python
from agents import LangChainAgent

agent = LangChainAgent(name="LC助手")
response = agent.process("什么是人工智能？")
print(response)
```

### 带工具的 Agent

```python
from agents import AdvancedAgent
from tools import calculate

tools = [{
    "name": "计算器",
    "func": calculate,
    "description": "执行数学计算"
}]

agent = AdvancedAgent(name="工具助手", tools=tools)
response = agent.process("计算 100 + 200")
print(response)
```

### 多 Agent 协作

```python
from agents import AgentOrchestrator, LangChainAgent

# 创建编排器
orchestrator = AgentOrchestrator()

# 创建并注册 Agent
agent1 = LangChainAgent(name="助手1")
agent2 = LangChainAgent(name="助手2")

orchestrator.register_agent(agent1, role="通用")
orchestrator.register_agent(agent2, role="专家")

# 路由任务
response = orchestrator.route_task("你好", target_agent="助手1")
print(response)
```

## 5️⃣ 核心组件速览

| 组件 | 用途 | 导入方式 |
|------|------|----------|
| `ChatAgent` | 基础对话 | `from agents import ChatAgent` |
| `LangChainAgent` | LangChain集成 | `from agents import LangChainAgent` |
| `AdvancedAgent` | 高级功能（工具+记忆） | `from agents import AdvancedAgent` |
| `ReasoningAgent` | 推理专用 | `from agents import ReasoningAgent` |
| `AgentOrchestrator` | 多Agent编排 | `from agents import AgentOrchestrator` |
| `calculate` | 计算工具 | `from tools import calculate` |
| `MCPServerManager` | MCP工具管理 | `from tools import MCPServerManager` |

## 6️⃣ 常见问题

### Q: 如何添加自定义工具？

```python
def my_tool(param: str) -> str:
    return f"结果: {param}"

tools = [{
    "name": "我的工具",
    "func": my_tool,
    "description": "工具描述"
}]

agent = AdvancedAgent(tools=tools)
```

### Q: 如何启用记忆功能？

```python
agent = AdvancedAgent(enable_memory=True, max_memory_turns=20)
```

### Q: 如何使用 MCP 工具？

```python
from tools import load_mcp_tools

mcp_tools = load_mcp_tools(["github"])
agent = AdvancedAgent(tools=mcp_tools)
```

## 📚 更多文档

详细文档请查看 [AGENT_TECH_STACK.md](AGENT_TECH_STACK.md)
