"""
离线演示模式 - 不需要 API Key
展示 MCP 工具和 Agent 编排功能
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tools.mcp_tools import MCPServerManager, load_mcp_tools
from agents.agent_orchestrator import AgentOrchestrator


def demo_mcp_tools():
    """演示 MCP 工具"""
    print("=" * 60)
    print("MCP 工具演示")
    print("=" * 60)
    print()
    
    # 发现 MCP 服务器
    manager = MCPServerManager()
    
    servers = manager.list_servers()
    print(f"发现的 MCP 服务器: {servers}")
    print()
    
    for server_name in servers:
        print(f"服务器: {server_name}")
        tools = manager.list_tools(server_name)
        print(f"  可用工具数量: {len(tools)}")
        
        for tool in tools[:3]:  # 只显示前3个
            print(f"    - {tool.get('name')}: {tool.get('description', '')[:50]}")
        
        if len(tools) > 3:
            print(f"    ... 还有 {len(tools) - 3} 个工具")
        print()


def demo_agent_orchestration():
    """演示 Agent 编排（不使用 LLM）"""
    print("=" * 60)
    print("Agent 编排演示")
    print("=" * 60)
    print()
    
    # 创建编排器
    orchestrator = AgentOrchestrator(name="演示编排器")
    
    print("1. 创建编排器")
    print(f"   名称: {orchestrator.name}")
    print()
    
    print("2. Agent 注册功能（模拟）")
    print("   在实际使用中，你会注册真实的 Agent:")
    print("   - coding_agent (编程专家)")
    print("   - math_agent (数学专家)")
    print("   - writing_agent (写作专家)")
    print()
    
    print("3. 任务路由策略")
    print("   - route_task(): 将任务发送给特定 Agent")
    print("   - broadcast_task(): 广播给所有 Agent")
    print("   - collaborative_task(): 多 Agent 协作")
    print()
    
    print("4. 任务分解功能")
    print("   复杂任务可以分解为:")
    print("   - 数据收集 → 数据分析 → 报告生成")
    print()


def demo_project_structure():
    """展示项目结构"""
    print("=" * 60)
    print("项目结构概览")
    print("=" * 60)
    print()
    
    structure = """
PyCharmMiscProject/
│
├── agents/                      # Agent 模块
│   ├── base_agent.py           # 基础抽象类
│   ├── chat_agent.py           # 基础对话 Agent
│   ├── langchain_agent.py      # LangChain 集成 ⭐
│   ├── advanced_agent.py       # 高级 Agent ⭐
│   └── agent_orchestrator.py   # Agent 编排器 ⭐
│
├── tools/                       # 工具模块
│   ├── calculator.py           # 计算工具
│   └── mcp_tools.py            # MCP 工具集成 ⭐
│
├── config/                      # 配置模块
│   └── settings.py             # 应用配置
│
├── examples/                    # 示例代码
│   └── full_stack_demo.py      # 完整演示
│
└── docs/                        # 文档
    ├── FRONTEND_GUIDE.md       # 前端开发者指南 📖
    ├── QUICKSTART.md           # 快速开始
    └── ARCHITECTURE.md         # 架构设计
    """
    
    print(structure)
    print()
    print("⭐ = 本次新增的核心组件")
    print("📖 = 推荐阅读的文档")
    print()


def next_steps():
    """下一步操作"""
    print("=" * 60)
    print("下一步操作")
    print("=" * 60)
    print()
    
    print("1️⃣  配置 API Key（启用完整功能）")
    print("   创建 .env 文件:")
    print("   OPENAI_API_KEY=sk-your-key-here")
    print()
    
    print("2️⃣  阅读文档")
    print("   📖 FRONTEND_GUIDE.md - 前端开发者友好指南")
    print("   📖 QUICKSTART.md - 快速上手")
    print()
    
    print("3️⃣  查看代码注释")
    print("   所有代码都有【前端类比】注释")
    print("   帮助你理解 AI 概念")
    print()
    
    print("4️⃣  运行完整示例（配置 API Key 后）")
    print("   python run.py")
    print()
    
    print("5️⃣  开始开发")
    print("   - 修改示例代码")
    print("   - 创建自己的 Agent")
    print("   - 添加工具")
    print()


def main():
    """主函数"""
    print()
    print("=" * 60)
    print("AI Agent 技术栈 - 离线演示")
    print("（不需要 API Key）")
    print("=" * 60)
    print()
    
    # 演示各个功能
    demo_mcp_tools()
    print()
    
    demo_agent_orchestration()
    print()
    
    demo_project_structure()
    print()
    
    next_steps()
    
    print("=" * 60)
    print("演示结束")
    print("=" * 60)
    print()
    print("💡 提示: 配置 API Key 后可以体验完整的 AI 对话功能")
    print()


if __name__ == "__main__":
    main()
