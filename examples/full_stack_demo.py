"""
完整 AI Agent 技术栈示例
展示 LangChain + LLM + MCP Skills 的集成使用
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv

from agents.chat_agent import ChatAgent
from agents.langchain_agent import LangChainAgent, LangChainToolAgent
from agents.advanced_agent import AdvancedAgent, ReasoningAgent
from agents.agent_orchestrator import AgentOrchestrator, TaskDecomposer
from tools.calculator import calculate
from tools.mcp_tools import MCPServerManager, load_mcp_tools

# 加载环境变量
load_dotenv()


def example_1_basic_chat():
    """示例 1: 基础对话 Agent"""
    print("=" * 60)
    print("示例 1: 基础对话 Agent")
    print("=" * 60)
    
    try:
        agent = ChatAgent(name="基础助手")
        
        # 测试对话
        response = agent.process("你好，请介绍一下自己")
        print(f"用户: 你好，请介绍一下自己")
        print(f"AI: {response}\n")
        
        response = agent.process("Python 中如何实现列表推导式？")
        print(f"用户: Python 中如何实现列表推导式？")
        print(f"AI: {response}\n")
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_2_langchain_agent():
    """示例 2: LangChain Agent"""
    print("=" * 60)
    print("示例 2: LangChain Agent")
    print("=" * 60)
    
    try:
        agent = LangChainAgent(
            name="LangChain助手",
            temperature=0.7
        )
        
        response = agent.process("什么是 LangChain？它有什么优势？")
        print(f"用户: 什么是 LangChain？它有什么优势？")
        print(f"AI: {response}\n")
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_3_tool_agent():
    """示例 3: 带工具的 Agent"""
    print("=" * 60)
    print("示例 3: 带工具的 Agent")
    print("=" * 60)
    
    try:
        # 定义工具
        tools = [
            {
                "name": "计算器",
                "func": calculate,
                "description": "执行数学计算，输入数学表达式字符串"
            }
        ]
        
        agent = LangChainToolAgent(
            name="工具助手",
            tools=tools
        )
        
        response = agent.process("计算 25 * 4 + 100 的结果")
        print(f"用户: 计算 25 * 4 + 100 的结果")
        print(f"AI: {response}\n")
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_4_advanced_agent():
    """示例 4: 高级 Agent（支持记忆和工具）"""
    print("=" * 60)
    print("示例 4: 高级 Agent")
    print("=" * 60)
    
    try:
        # 定义工具
        tools = [
            {
                "name": "计算器",
                "func": calculate,
                "description": "执行数学计算"
            }
        ]
        
        agent = AdvancedAgent(
            name="高级助手",
            tools=tools,
            enable_memory=True,
            max_memory_turns=10
        )
        
        # 第一轮对话
        response = agent.process("我的名字是张三")
        print(f"用户: 我的名字是张三")
        print(f"AI: {response}\n")
        
        # 第二轮对话（测试记忆）
        response = agent.process("我叫什么名字？")
        print(f"用户: 我叫什么名字？")
        print(f"AI: {response}\n")
        
        # 使用工具
        response = agent.process("帮我计算 123 * 456")
        print(f"用户: 帮我计算 123 * 456")
        print(f"AI: {response}\n")
        
        print(agent.get_memory_summary())
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_5_reasoning_agent():
    """示例 5: 推理 Agent"""
    print("=" * 60)
    print("示例 5: 推理 Agent")
    print("=" * 60)
    
    try:
        agent = ReasoningAgent(name="推理专家")
        
        result = agent.process_with_reasoning(
            "如果一个房间里有3个人，每个人有2只手，每只手有5个手指，"
            "那么这个房间里总共有多少个手指？"
        )
        
        print(f"问题: 如果一个房间里有3个人...")
        print(f"推理结果:\n{result['reasoning']}\n")
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_6_mcp_tools():
    """示例 6: MCP 工具集成"""
    print("=" * 60)
    print("示例 6: MCP 工具集成")
    print("=" * 60)
    
    try:
        # 发现 MCP 服务器
        manager = MCPServerManager()
        
        servers = manager.list_servers()
        print(f"发现的 MCP 服务器: {servers}\n")
        
        if servers:
            # 列出第一个服务器的工具
            first_server = servers[0]
            tools = manager.list_tools(first_server)
            print(f"服务器 '{first_server}' 的工具:")
            for tool in tools:
                print(f"  - {tool.get('name')}: {tool.get('description', '')}")
            print()
            
            # 尝试加载 MCP 工具
            mcp_tools = load_mcp_tools([first_server])
            print(f"加载了 {len(mcp_tools)} 个 MCP 工具\n")
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_7_agent_orchestration():
    """示例 7: Agent 编排（多 Agent 协作）"""
    print("=" * 60)
    print("示例 7: Agent 编排")
    print("=" * 60)
    
    try:
        # 创建编排器
        orchestrator = AgentOrchestrator(name="主编排器")
        
        # 创建多个 Agent
        general_agent = LangChainAgent(name="通用助手", temperature=0.7)
        coding_agent = LangChainAgent(
            name="编程专家",
            system_prompt="你是一个专业的编程专家，擅长解答编程相关问题。"
        )
        math_agent = AdvancedAgent(
            name="数学专家",
            tools=[{
                "name": "计算器",
                "func": calculate,
                "description": "执行数学计算"
            }]
        )
        
        # 注册 Agent
        orchestrator.register_agent(general_agent, role="通用问答")
        orchestrator.register_agent(coding_agent, role="编程相关")
        orchestrator.register_agent(math_agent, role="数学计算")
        
        print(f"\n已注册的 Agent:")
        for agent_info in orchestrator.list_agents():
            print(f"  - {agent_info['name']}: {agent_info['role']}")
        print()
        
        # 路由任务
        print("任务 1: 路由到编程专家")
        response = orchestrator.route_task(
            "如何用 Python 实现快速排序？",
            target_agent="编程专家"
        )
        print(f"响应: {response[:200]}...\n")
        
        # 广播任务
        print("任务 2: 广播给所有 Agent")
        results = orchestrator.broadcast_task("简单介绍一下你自己")
        for name, resp in results.items():
            print(f"  {name}: {resp[:100]}...")
        print()
        
        # 协作任务
        print("任务 3: 协作任务")
        collab_result = orchestrator.collaborative_task(
            "分析这个问题：如何优化 Python 代码性能？",
            agent_sequence=["编程专家", "通用助手"]
        )
        
        for agent_name, result in collab_result["results"].items():
            print(f"  {agent_name}: {result[:150]}...")
        print()
        
    except Exception as e:
        print(f"错误: {e}\n")


def example_8_task_decomposition():
    """示例 8: 任务分解"""
    print("=" * 60)
    print("示例 8: 任务分解")
    print("=" * 60)
    
    try:
        # 创建编排器和任务分解器
        orchestrator = AgentOrchestrator()
        
        analysis_agent = LangChainAgent(
            name="分析师",
            system_prompt="你是一个数据分析师，擅长数据分析。"
        )
        report_agent = LangChainAgent(
            name="报告生成器",
            system_prompt="你是一个报告生成专家，擅长撰写专业报告。"
        )
        
        orchestrator.register_agent(analysis_agent, role="数据分析")
        orchestrator.register_agent(report_agent, role="报告生成")
        
        decomposer = TaskDecomposer(orchestrator)
        
        # 分解并执行复杂任务
        complex_task = "分析销售数据并生成月度报告"
        print(f"复杂任务: {complex_task}\n")
        
        results = decomposer.execute_decomposed_task(
            complex_task,
            role_to_agent={
                "数据收集": "分析师",
                "数据分析": "分析师",
                "报告生成": "报告生成器"
            }
        )
        
        print("子任务执行结果:")
        for i, result in enumerate(results, 1):
            print(f"\n子任务 {i}:")
            print(f"  描述: {result['subtask']}")
            print(f"  角色: {result['role']}")
            print(f"  Agent: {result['agent']}")
            print(f"  结果: {result['result'][:150]}...")
        
    except Exception as e:
        print(f"错误: {e}\n")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("完整 AI Agent 技术栈演示")
    print("LangChain + LLM + MCP Skills")
    print("=" * 60 + "\n")
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中设置您的 OpenAI API Key\n")
    
    examples = [
        ("基础对话 Agent", example_1_basic_chat),
        ("LangChain Agent", example_2_langchain_agent),
        ("带工具的 Agent", example_3_tool_agent),
        ("高级 Agent", example_4_advanced_agent),
        ("推理 Agent", example_5_reasoning_agent),
        ("MCP 工具集成", example_6_mcp_tools),
        ("Agent 编排", example_7_agent_orchestration),
        ("任务分解", example_8_task_decomposition),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"示例 '{name}' 执行失败: {e}\n")
    
    print("=" * 60)
    print("所有示例执行完毕")
    print("=" * 60)


if __name__ == "__main__":
    main()
