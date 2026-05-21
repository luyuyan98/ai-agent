"""测试安装是否成功"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def test_imports():
    """测试所有导入"""
    try:
        import openai
        print(f"✓ OpenAI {openai.__version__}")
    except ImportError as e:
        print(f"✗ OpenAI 导入失败: {e}")
    
    try:
        import langchain
        print(f"✓ LangChain {langchain.__version__}")
    except ImportError as e:
        print(f"✗ LangChain 导入失败: {e}")
    
    try:
        from langchain_openai import ChatOpenAI
        print("✓ langchain-openai")
    except ImportError as e:
        print(f"✗ langchain-openai 导入失败: {e}")
    
    try:
        from langchain_community.tools import Tool
        print("✓ langchain-community")
    except ImportError as e:
        print(f"✗ langchain-community 导入失败: {e}")
    
    try:
        import dotenv
        print("✓ python-dotenv")
    except ImportError as e:
        print(f"✗ python-dotenv 导入失败: {e}")
    
    try:
        from agents import ChatAgent, LangChainAgent, AdvancedAgent
        print("✓ agents 模块")
    except ImportError as e:
        print(f"✗ agents 模块导入失败: {e}")
    
    try:
        from tools import calculate, MCPServerManager
        print("✓ tools 模块")
    except ImportError as e:
        print(f"✗ tools 模块导入失败: {e}")


if __name__ == "__main__":
    print("测试安装...\n")
    test_imports()
    print("\n完成！")
