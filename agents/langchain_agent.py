"""
LangChain 集成智能体
使用 LangChain 框架构建强大的 AI Agent

【前端类比】
LangChain 就像一个 "AI 开发框架"，类似 React/Vue 之于前端开发
它提供了：
- 组件化（Prompts = 模板组件）
- 状态管理（Memory = 状态管理）
- 工具链（Tools = 中间件/插件）
- 工作流（Chains = 组合函数/Pipeline）

这个模块相当于用 LangChain "框架"重写了基础 Agent
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI  # 类似 axios，用于调用 API
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage  # 消息类型定义
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 模板系统
# 注意：LangChain 1.x 版本移除了 langchain.chains，直接使用 LLM 即可

from .base_agent import BaseAgent
from config.settings import settings


class LangChainAgent(BaseAgent):
    """
    基于 LangChain 的智能体
    
    【前端类比】
    就像一个用 React + Redux 重写的组件，比原生组件更强大
    - BaseAgent = 原生 JavaScript 组件
    - LangChainAgent = React 组件（有框架支持）
    
    优势：
    - 更好的模板系统（类似 JSX/Vue template）
    - 更灵活的消息处理
    - 更容易扩展
    """
    
    def __init__(
        self, 
        name: str = "LangChain助手", 
        model: str = None,
        system_prompt: str = None,
        temperature: float = 0.7
    ):
        """
        初始化 LangChain Agent
        
        【前端类比】
        就像 React 组件的 constructor，接收 props 并初始化 state
        
        Args:
            name: Agent 名称（类似组件 displayName）
            model: LLM 模型名称（类似配置项）
            system_prompt: 系统提示词（类似组件的默认配置）
            temperature: 温度参数，控制创造性 0-1（类似动画的 easing 强度）
        """
        super().__init__(name)
        
        # 配置模型
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature
        
        # 初始化 LLM（类似创建 axios 实例）
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL,  # 支持 DeepSeek 等兼容 API
            max_tokens=2048,  # 增加最大输出长度
            timeout=60  # 增加超时时间
        )
        
        # 系统提示词（类似组件的默认文案）
        self.system_prompt = system_prompt or (
            f"你是一个名为 {name} 的 AI 助手。"
            "你的任务是帮助用户解决问题，提供准确、有用的信息。"
            "请保持友好、专业的态度。"
        )
        
        # 创建提示模板（类似 Vue 的 template 或 React 的 JSX）
        # 这个模板定义了对话的结构：系统消息 + 历史消息
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),  # 系统指令
            MessagesPlaceholder(variable_name="messages"),  # 占位符，填入历史消息
        ])
        
        # 创建链（类似组合函数：prompt -> llm）
        # 这就像前端的 pipeline：input -> transform1 -> transform2 -> output
        self.chain = self.prompt | self.llm
    
    def process(self, message: str) -> str:
        """
        处理用户输入并返回响应
        
        【前端类比】
        就像 React 组件中处理用户输入的方法：
        ```javascript
        handleSubmit = (message) => {
          // 1. 更新 state（添加用户消息）
          this.addMessage('user', message);
          
          // 2. 调用 API
          const response = await api.call(messages);
          
          // 3. 更新 state（添加 AI 回复）
          this.addMessage('assistant', response);
          
          return response;
        }
        ```
        
        Args:
            message: 用户输入的消息
            
        Returns:
            AI 的回复消息
        """
        try:
            # 添加用户消息到历史（类似更新 state）
            self.add_to_history("user", message)
            
            # 转换历史记录为 LangChain 消息格式（类似数据格式化）
            langchain_messages = self._convert_to_langchain_messages()
            
            # 调用链（类似调用 API）
            # 这就像：axios.post('/chat', { messages })
            response = self.chain.invoke({"messages": langchain_messages})
            
            # 获取响应内容
            assistant_message = response.content
            
            # 添加 AI 响应到历史（类似更新 state）
            self.add_to_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _convert_to_langchain_messages(self) -> List:
        """
        将对话历史转换为 LangChain 消息格式
        
        【前端类比】
        就像数据转换函数，把内部格式转换为 API 需要的格式
        类似：
        ```javascript
        // 内部格式
        const history = [
          {role: 'user', content: '你好'},
          {role: 'assistant', content: '你好！'}
        ];
        
        // 转换为 API 格式
        const apiMessages = history.map(msg => {
          if (msg.role === 'user') return new HumanMessage(msg.content);
          if (msg.role === 'assistant') return new AIMessage(msg.content);
        });
        ```
        
        Returns:
            LangChain 消息对象列表
        """
        messages = []
        for msg in self.conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
        return messages
    
    def reset(self):
        """重置对话历史"""
        super().reset()


class LangChainToolAgent(LangChainAgent):
    """
    支持工具调用的 LangChain 智能体
    
    【前端类比】
    就像带有 middleware 的 React 组件
    """
    
    def __init__(
        self, 
        name: str = "工具助手",
        tools: List[Any] = None,
        **kwargs
    ):
        super().__init__(name=name, **kwargs)
        self.tools = tools or []
        
        # 检查 Agent Executor 是否可用
        try:
            from langchain.agents import create_tool_calling_agent, AgentExecutor
            from langchain_community.tools import Tool
            self.agent_executor_available = True
        except ImportError:
            self.agent_executor_available = False
            print("警告: Agent Executor 不可用，将使用简单对话模式")
        
        # 如果有工具且 Agent Executor 可用，创建带有工具支持的链
        if self.tools and self.agent_executor_available:
            from langchain.agents import create_tool_calling_agent, AgentExecutor
            from langchain_community.tools import Tool
            
            # 转换工具为 LangChain 格式
            langchain_tools = []
            for tool in self.tools:
                if isinstance(tool, dict):
                    langchain_tools.append(Tool(
                        name=tool["name"],
                        func=tool["func"],
                        description=tool["description"]
                    ))
                else:
                    langchain_tools.append(tool)
            
            try:
                # 创建工具调用 agent
                self.agent = create_tool_calling_agent(
                    llm=self.llm,
                    tools=langchain_tools,
                    prompt=self.prompt
                )
                
                self.agent_executor = AgentExecutor(
                    agent=self.agent,
                    tools=langchain_tools,
                    verbose=True
                )
            except Exception as e:
                print(f"设置工具调用失败: {e}")
                self.agent_executor = None
    
    def process(self, message: str) -> str:
        """处理用户输入，支持工具调用"""
        try:
            if not hasattr(self, 'agent_executor'):
                # 如果没有工具，使用父类方法
                return super().process(message)
            
            # 添加用户消息到历史
            self.add_to_history("user", message)
            
            # 转换历史记录
            langchain_messages = self._convert_to_langchain_messages()
            
            # 调用 agent executor
            response = self.agent_executor.invoke({
                "messages": langchain_messages
            })
            
            # 获取响应
            assistant_message = response.get("output", "")
            
            # 添加 AI 响应到历史
            self.add_to_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(error_msg)
            return error_msg
