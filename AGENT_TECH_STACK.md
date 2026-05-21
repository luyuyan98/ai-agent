# AI Agent 完整技术栈

基于 **LangChain + LLM + MCP Skills** 构建的完整 AI Agent 技术栈。

## 📋 目录

- [项目概述](#项目概述)
- [技术架构](#技术架构)
- [核心组件](#核心组件)
- [快速开始](#快速开始)
- [使用示例](#使用示例)
- [项目结构](#项目结构)

## 🎯 项目概述

本项目提供了一套完整的 AI Agent 开发框架，包含：

- ✅ **多类型 Agent**: 基础对话、LangChain集成、工具调用、高级推理
- ✅ **LangChain 集成**: 完整的 LangChain 框架支持
- ✅ **MCP Tools 支持**: Model Context Protocol 工具集成
- ✅ **Agent 编排**: 多 Agent 协作和任务分解
- ✅ **记忆管理**: 对话历史和上下文管理
- ✅ **工具系统**: 可扩展的工具调用机制

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────┐
│                  Agent Orchestrator                  │
│              (多 Agent 编排与协作)                     │
└──────────────────┬──────────────────────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
┌──────▼──────┐ ┌──▼────────┐ ┌▼────────────┐
│Basic Agent  │ │LangChain  │ │Advanced     │
│(基础对话)    │ │Agent      │ │Agent        │
│             │ │(LC集成)    │ │(工具+记忆)   │
└─────────────┘ └───────────┘ └─────────────┘
                       │              │
                  ┌────▼──────────────▼────┐
                  │   Tool System          │
                  │  - Calculator          │
                  │  - MCP Tools           │
                  │  - Custom Tools        │
                  └────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │   LLM Backend   │
                  │  (OpenAI/etc)   │
                  └─────────────────┘
```

## 🔧 核心组件

### 1. Agent 层 (`agents/`)

#### BaseAgent
所有 Agent 的抽象基类，定义基本接口。

#### ChatAgent
基于 OpenAI API 的基础对话 Agent。

#### LangChainAgent
集成 LangChain 框架的 Agent，支持：
- LangChain 提示模板
- 消息历史管理
- 链式调用

#### LangChainToolAgent
支持工具调用的 LangChain Agent，可以：
- 自动选择和使用工具
- 执行复杂任务
- 返回结构化结果

#### AdvancedAgent
高级 Agent，具备：
- 工具调用能力
- 长期记忆管理
- 动态工具添加/移除
- 自定义系统提示

#### ReasoningAgent
专门的推理 Agent，用于：
- 复杂问题分析
- 分步推理
- 逻辑推导

#### AgentOrchestrator
多 Agent 编排器，支持：
- Agent 注册和管理
- 任务路由
- 广播任务
- 协作任务执行
- 任务分解

### 2. 工具层 (`tools/`)

#### Calculator
数学计算工具，支持基本运算。

#### MCP Tools
Model Context Protocol 工具集成：
- **MCPServerManager**: 发现和管理 MCP 服务器
- **MCPToolWrapper**: 将 MCP 工具包装为 LangChain 格式
- **MCPClient**: 简化的 MCP 客户端

支持的 MCP 服务器（根据配置）：
- `github`: GitHub API 操作
- `fetch`: 网页内容获取
- `playwright`: 浏览器自动化

### 3. 配置层 (`config/`)

集中管理应用配置：
- OpenAI API 密钥
- 模型选择
- 日志级别

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
LOG_LEVEL=INFO
```

### 3. 运行示例

```bash
python examples/full_stack_demo.py
```

## 💡 使用示例

### 示例 1: 基础对话

```python
from agents.chat_agent import ChatAgent

agent = ChatAgent(name="助手")
response = agent.process("你好！")
print(response)
```

### 示例 2: LangChain Agent

```python
from agents.langchain_agent import LangChainAgent

agent = LangChainAgent(
    name="LangChain助手",
    temperature=0.7
)
response = agent.process("什么是 LangChain？")
print(response)
```

### 示例 3: 带工具的 Agent

```python
from agents.langchain_agent import LangChainToolAgent
from tools.calculator import calculate

tools = [{
    "name": "计算器",
    "func": calculate,
    "description": "执行数学计算"
}]

agent = LangChainToolAgent(name="工具助手", tools=tools)
response = agent.process("计算 25 * 4 + 100")
print(response)
```

### 示例 4: 高级 Agent（带记忆）

```python
from agents.advanced_agent import AdvancedAgent

agent = AdvancedAgent(
    name="高级助手",
    enable_memory=True,
    max_memory_turns=20
)

# 第一轮
agent.process("我的名字是张三")

# 第二轮 - 会记住之前的对话
response = agent.process("我叫什么名字？")
print(response)  # 应该回答"张三"
```

### 示例 5: Agent 编排

```python
from agents.agent_orchestrator import AgentOrchestrator
from agents.langchain_agent import LangChainAgent

# 创建编排器
orchestrator = AgentOrchestrator()

# 创建并注册多个 Agent
coding_agent = LangChainAgent(name="编程专家")
math_agent = LangChainAgent(name="数学专家")

orchestrator.register_agent(coding_agent, role="编程")
orchestrator.register_agent(math_agent, role="数学")

# 路由任务
response = orchestrator.route_task(
    "如何用 Python 实现排序？",
    target_agent="编程专家"
)

# 广播任务
results = orchestrator.broadcast_task("介绍一下你自己")

# 协作任务
collab = orchestrator.collaborative_task(
    "分析并解决这个问题",
    agent_sequence=["编程专家", "数学专家"]
)
```

### 示例 6: MCP 工具集成

```python
from tools.mcp_tools import MCPServerManager, load_mcp_tools

# 发现 MCP 服务器
manager = MCPServerManager()
servers = manager.list_servers()

# 加载 MCP 工具
mcp_tools = load_mcp_tools(["github", "fetch"])

# 在 Agent 中使用
from agents.advanced_agent import AdvancedAgent
agent = AdvancedAgent(name="MCP助手", tools=mcp_tools)
```

### 示例 7: 任务分解

```python
from agents.agent_orchestrator import AgentOrchestrator, TaskDecomposer

orchestrator = AgentOrchestrator()
# ... 注册 Agent ...

decomposer = TaskDecomposer(orchestrator)

# 分解并执行复杂任务
results = decomposer.execute_decomposed_task(
    "分析销售数据并生成月度报告",
    role_to_agent={
        "数据分析": "分析师",
        "报告生成": "报告生成器"
    }
)
```

## 📁 项目结构

```
PyCharmMiscProject/
├── agents/                      # Agent 模块
│   ├── __init__.py
│   ├── base_agent.py           # 基础 Agent 抽象类
│   ├── chat_agent.py           # 基础对话 Agent
│   ├── langchain_agent.py      # LangChain 集成 Agent
│   ├── advanced_agent.py       # 高级 Agent（工具+记忆）
│   └── agent_orchestrator.py   # Agent 编排器
├── tools/                       # 工具模块
│   ├── __init__.py
│   ├── calculator.py           # 计算工具
│   └── mcp_tools.py            # MCP 工具集成
├── config/                      # 配置模块
│   ├── __init__.py
│   └── settings.py             # 应用配置
├── utils/                       # 工具函数
│   ├── __init__.py
│   └── helpers.py
├── examples/                    # 示例代码
│   └── full_stack_demo.py      # 完整技术栈演示
├── .env.example                 # 环境变量示例
├── .gitignore
├── requirements.txt             # 依赖包
└── script.py                    # 主脚本
```

## 🔌 扩展开发

### 添加自定义工具

```python
def my_custom_tool(param: str) -> str:
    """我的自定义工具"""
    return f"处理结果: {param}"

# 在 Agent 中使用
tools = [{
    "name": "我的工具",
    "func": my_custom_tool,
    "description": "工具描述"
}]

agent = AdvancedAgent(name="助手", tools=tools)
```

### 创建自定义 Agent

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="自定义Agent")
        # 初始化逻辑
    
    def process(self, message: str) -> str:
        # 自定义处理逻辑
        return "响应"
```

## 📝 注意事项

1. **API Key 安全**: 不要将 `.env` 文件提交到版本控制系统
2. **依赖管理**: 定期更新依赖包以获取最新功能和安全补丁
3. **错误处理**: 所有 Agent 都有基本的错误处理，建议在生产环境中添加更完善的异常处理
4. **性能优化**: 对于高并发场景，考虑使用异步版本的 LangChain

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
