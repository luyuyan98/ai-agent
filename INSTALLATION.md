# 安装与故障排除指南

## 📦 安装步骤

### 1. 确保 Python 版本

```bash
python --version
# 建议 Python 3.9 或更高版本
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 或者使用 conda
conda create -n ai-agent python=3.10
conda activate ai-agent
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```python
python -c "import langchain; print(langchain.__version__)"
python -c "import openai; print(openai.__version__)"
```

## 🔧 常见问题与解决方案

### 问题 1: ImportError - 找不到模块

**错误信息**:
```
ModuleNotFoundError: No module named 'langchain_community'
```

**解决方案**:
```bash
pip install langchain-community
```

### 问题 2: 导入错误 - 找不到引用

**错误信息**:
```
在 'langchain.agents' 中找不到引用 'create_tool_calling_agent'
```

**解决方案**:
确保安装了正确版本的 LangChain：
```bash
pip install --upgrade langchain langchain-openai langchain-community
```

### 问题 3: OpenAI API Key 未设置

**错误信息**:
```
ValueError: 请设置 OPENAI_API_KEY 环境变量
```

**解决方案**:
创建 `.env` 文件：
```env
OPENAI_API_KEY=sk-your-api-key-here
```

或在代码中设置：
```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

### 问题 4: 版本冲突

**错误信息**:
```
Conflict errors during installation
```

**解决方案**:
```bash
# 清除缓存并重新安装
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### 问题 5: MCP 工具加载失败

**错误信息**:
```
MCP 目录不存在
```

**解决方案**:
这是正常的，如果你不使用 MCP 工具可以忽略。要使用 MCP 工具，需要配置 MCP 服务器。

## ✅ 安装验证脚本

创建 `test_installation.py`:

```python
"""测试安装是否成功"""

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
```

运行测试：
```bash
python test_installation.py
```

## 🚀 快速测试

### 测试 1: 基础导入

```python
from agents import ChatAgent
print("导入成功！")
```

### 测试 2: 创建 Agent

```python
from agents import LangChainAgent
import os

os.environ["OPENAI_API_KEY"] = "your-key-here"
agent = LangChainAgent(name="测试助手")
print("Agent 创建成功！")
```

### 测试 3: 完整流程

```bash
python examples/full_stack_demo.py
```

## 📋 依赖清单

核心依赖：
- `openai>=1.0.0` - OpenAI SDK
- `langchain>=0.1.0` - LangChain 框架
- `langchain-openai>=0.0.5` - LangChain OpenAI 集成
- `langchain-community>=0.0.10` - LangChain 社区工具
- `python-dotenv>=1.0.0` - 环境变量管理
- `pydantic>=2.0.0` - 数据验证
- `mcp>=0.1.0` - MCP 协议支持（可选）

## 🔍 调试技巧

### 1. 查看详细错误信息

```python
import traceback
try:
    # 你的代码
    pass
except Exception as e:
    traceback.print_exc()
```

### 2. 检查包版本

```bash
pip list | findstr langchain
pip list | findstr openai
```

### 3. 清理重新安装

```bash
pip uninstall langchain langchain-openai langchain-community
pip install langchain langchain-openai langchain-community
```

## 💡 最佳实践

1. **使用虚拟环境**: 避免依赖冲突
2. **固定版本**: 在生产环境中固定依赖版本
3. **定期更新**: 保持依赖最新以获得安全补丁
4. **阅读文档**: 查看官方文档了解最新 API

## 📞 获取帮助

如果遇到问题：

1. 查看本文档的常见问题部分
2. 运行安装验证脚本
3. 检查 Python 和 pip 版本
4. 查看官方文档：
   - [LangChain Docs](https://python.langchain.com/)
   - [OpenAI Docs](https://platform.openai.com/docs)

## 🎯 下一步

安装成功后：

1. 阅读 [QUICKSTART.md](QUICKSTART.md)
2. 运行示例代码
3. 开始开发你的 AI Agent 应用
