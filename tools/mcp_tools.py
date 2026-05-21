"""
MCP (Model Context Protocol) Tools 集成模块
提供与 MCP 服务器的交互能力

【前端类比】
MCP 就像前端的 "插件系统" 或 "中间件"
- MCP Server = 插件提供者（类似 npm 包）
- MCP Tool = 具体功能（类似 lodash 的工具函数）
- MCPServerManager = 插件管理器（类似 webpack 的 plugin 管理）

例如：
- GitHub MCP Server = GitHub API 插件包
- fetch_html tool = 获取网页的工具函数
- playwright tools = 浏览器自动化工具集

这让你可以像安装 npm 包一样，轻松扩展 AI 的能力
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class MCPServerManager:
    """
    MCP 服务器管理器
    
    【前端类比】
    就像 npm 的包管理器或 webpack 的 plugin 管理器
    - 发现已安装的插件（MCP 服务器）
    - 加载插件的工具（tools）
    - 提供插件信息查询
    
    类似：
    ```javascript
    class PluginManager {
      constructor() {
        this.plugins = {};  // 已安装的插件
        this.discoverPlugins();  // 扫描 node_modules
      }
      
      listPlugins() { return Object.keys(this.plugins); }
      getPluginTools(pluginName) { return this.plugins[pluginName].tools; }
    }
    ```
    """
    
    def __init__(self, mcps_dir: str = None):
        """
        初始化 MCP 服务器管理器
        
        【前端类比】
        就像初始化插件管理器，指定插件目录
        类似 webpack 配置 plugins 目录
        
        Args:
            mcps_dir: MCP 服务器目录路径，默认为用户主目录下的 .lingma/mcps
                     类似 node_modules 目录
        """
        if mcps_dir is None:
            # 默认 MCP 目录（类似 node_modules）
            home_dir = Path.home()
            self.mcps_dir = home_dir / ".lingma" / "mcps"
        else:
            self.mcps_dir = Path(mcps_dir)
        
        self.servers = {}  # 已发现的服务器（类似已安装的插件）
        self._discover_servers()  # 扫描并加载服务器
    
    def _discover_servers(self):
        """
        发现可用的 MCP 服务器
        
        【前端类比】
        就像扫描 node_modules 目录，找出所有已安装的 npm 包
        或者像 webpack 扫描 plugins 目录
        
        流程：
        1. 遍历 mcps 目录下的所有子目录
        2. 检查每个子目录是否有元数据文件（类似 package.json）
        3. 读取元数据和工具定义
        4. 注册到 servers 列表中
        """
        if not self.mcps_dir.exists():
            print(f"MCP 目录不存在: {self.mcps_dir}")
            return
        
        for server_dir in self.mcps_dir.iterdir():
            if server_dir.is_dir():
                metadata_file = server_dir / "SERVER_METADATA.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            server_name = server_dir.name
                            self.servers[server_name] = {
                                "name": server_name,
                                "path": str(server_dir),
                                "metadata": metadata,
                                "tools": self._load_tools(server_dir)
                            }
                    except Exception as e:
                        print(f"加载服务器 {server_name} 失败: {e}")
    
    def _load_tools(self, server_dir: Path) -> List[Dict]:
        """
        加载服务器的工具定义
        
        【前端类比】
        就像读取 npm 包的 exports，找出包提供的所有函数
        或者像读取 webpack plugin 提供的 hooks
        
        每个工具定义包含：
        - name: 工具名称（类似函数名）
        - description: 工具描述（类似 JSDoc）
        - inputSchema: 参数定义（类似 TypeScript 类型定义）
        
        Args:
            server_dir: 服务器目录路径
            
        Returns:
            工具定义列表
        """
        tools = []
        tools_dir = server_dir / "tools"
        
        if tools_dir.exists():
            for tool_file in tools_dir.glob("*.json"):
                try:
                    with open(tool_file, 'r', encoding='utf-8') as f:
                        tool_def = json.load(f)
                        tools.append(tool_def)
                except Exception as e:
                    print(f"加载工具文件 {tool_file} 失败: {e}")
        
        return tools
    
    def list_servers(self) -> List[str]:
        """列出所有可用的服务器"""
        return list(self.servers.keys())
    
    def get_server_info(self, server_name: str) -> Optional[Dict]:
        """获取服务器信息"""
        return self.servers.get(server_name)
    
    def list_tools(self, server_name: str) -> List[Dict]:
        """列出服务器的所有工具"""
        server = self.servers.get(server_name)
        if server:
            return server["tools"]
        return []
    
    def get_tool_schema(self, server_name: str, tool_name: str) -> Optional[Dict]:
        """获取工具的 JSON Schema"""
        tools = self.list_tools(server_name)
        for tool in tools:
            if tool.get("name") == tool_name:
                return tool.get("inputSchema", {})
        return None


class MCPToolWrapper:
    """
    MCP 工具包装器，用于与 LangChain 集成
    
    【前端类比】
    就像适配器模式（Adapter Pattern），把 MCP 工具转换为 LangChain 能识别的格式
    类似：
    - 把 jQuery 插件适配为 React 组件
    - 把 CommonJS 模块转换为 ES Module
    
    作用：
    - 保持原始工具功能不变
    - 提供统一的接口给 LangChain 使用
    - 类似前端的 "桥接层" 或 "兼容层"
    """
    
    def __init__(self, server_name: str, tool_def: Dict):
        """
        初始化 MCP 工具包装器
        
        Args:
            server_name: MCP 服务器名称（类似包名 @github/tools）
            tool_def: 工具定义字典（类似 package.json）
        """
        self.server_name = server_name
        self.tool_def = tool_def
        self.name = tool_def.get("name", "unknown")  # 工具名称
        self.description = tool_def.get("description", "")  # 工具描述
        self.schema = tool_def.get("inputSchema", {})  # 参数 schema
    
    def to_langchain_tool(self):
        """转换为 LangChain Tool 格式"""
        from langchain_community.tools import Tool
        
        # 创建一个简单的调用函数（实际使用时需要实现真正的 MCP 调用）
        def mcp_tool_func(input_str: str) -> str:
            return f"MCP Tool '{self.name}' called with: {input_str}"
        
        return Tool(
            name=self.name,
            func=mcp_tool_func,
            description=self.description
        )
    
    def get_required_parameters(self) -> List[str]:
        """获取必需参数列表"""
        required = self.schema.get("required", [])
        return required
    
    def get_properties(self) -> Dict:
        """获取参数属性定义"""
        return self.schema.get("properties", {})


def load_mcp_tools(server_names: List[str] = None) -> List[Any]:
    """
    加载 MCP 工具
    
    Args:
        server_names: 要加载的服务器名称列表，None 表示加载所有
    
    Returns:
        LangChain Tool 列表
    """
    manager = MCPServerManager()
    all_tools = []
    
    servers_to_load = server_names or manager.list_servers()
    
    for server_name in servers_to_load:
        tools = manager.list_tools(server_name)
        for tool_def in tools:
            wrapper = MCPToolWrapper(server_name, tool_def)
            all_tools.append(wrapper.to_langchain_tool())
    
    return all_tools


# 示例：直接使用 MCP 工具
class MCPClient:
    """简化的 MCP 客户端"""
    
    def __init__(self):
        self.manager = MCPServerManager()
    
    def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Any:
        """
        调用 MCP 工具
        
        Args:
            server_name: 服务器名称
            tool_name: 工具名称
            arguments: 工具参数
        
        Returns:
            工具执行结果
        """
        # 这里应该实现真正的 MCP 协议调用
        # 目前返回模拟数据
        return {
            "server": server_name,
            "tool": tool_name,
            "arguments": arguments,
            "result": "模拟执行结果"
        }
    
    def browse_github(self, query: str) -> str:
        """浏览 GitHub 示例"""
        result = self.call_tool("github", "search_repositories", {"query": query})
        return f"GitHub 搜索结果: {result}"
    
    def fetch_webpage(self, url: str) -> str:
        """获取网页内容示例"""
        result = self.call_tool("fetch", "fetch_html", {"url": url})
        return f"网页内容: {result}"
