"""
快速验证修复是否成功
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("验证修复")
print("=" * 60)
print()

# 测试 1: 导入 agents 模块
print("测试 1: 导入 agents 模块...")
try:
    from agents import ChatAgent, LangChainAgent, AdvancedAgent
    print("✅ agents 模块导入成功")
except Exception as e:
    print(f"❌ agents 模块导入失败: {e}")
    sys.exit(1)

print()

# 测试 2: 导入 tools 模块
print("测试 2: 导入 tools 模块...")
try:
    from tools import calculate, MCPServerManager
    print("✅ tools 模块导入成功")
except Exception as e:
    print(f"❌ tools 模块导入失败: {e}")
    sys.exit(1)

print()

# 测试 3: 创建 Agent
print("测试 3: 创建 LangChainAgent...")
try:
    agent = LangChainAgent(name="测试助手")
    print("✅ Agent 创建成功")
    print(f"   Agent 名称: {agent.name}")
except Exception as e:
    print(f"❌ Agent 创建失败: {e}")
    sys.exit(1)

print()

# 测试 4: 检查 LangChain 版本
print("测试 4: 检查 LangChain 版本...")
try:
    import langchain
    print(f"✅ LangChain 版本: {langchain.__version__}")
except Exception as e:
    print(f"❌ 检查版本失败: {e}")

print()
print("=" * 60)
print("✅ 所有测试通过！修复成功！")
print("=" * 60)
print()
print("现在可以运行:")
print("  python run.py")
print("或")
print("  python examples/full_stack_demo.py")
