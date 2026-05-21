"""
简单测试 - 只测试导入
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("测试导入...")
print()

try:
    print("1. 导入 base_agent...")
    from agents.base_agent import BaseAgent
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

try:
    print("2. 导入 chat_agent...")
    from agents.chat_agent import ChatAgent
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

try:
    print("3. 导入 langchain_agent...")
    from agents.langchain_agent import LangChainAgent, LangChainToolAgent
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

try:
    print("4. 导入 advanced_agent...")
    from agents.advanced_agent import AdvancedAgent, ReasoningAgent
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

try:
    print("5. 导入 agent_orchestrator...")
    from agents.agent_orchestrator import AgentOrchestrator
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

try:
    print("6. 导入 tools...")
    from tools import calculate, MCPServerManager
    print("   ✅ 成功")
except Exception as e:
    print(f"   ❌ 失败: {e}")

print()
print("=" * 60)
print("如果都显示 ✅，说明修复成功！")
print("=" * 60)
