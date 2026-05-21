"""
高级 Agent 架构
支持工具调用、记忆管理、多步推理等高级功能

【前端类比】
这就像前端的 "高阶组件 (HOC)" 或 "自定义 Hooks"
- AdvancedAgent = 带有 Redux + Middleware + Memory 的增强组件
- BaseAgent = 基础组件
- 工具系统 = Middleware/Plugins
- 记忆管理 = Redux Persist / localStorage

类似于：
```javascript
// 基础组件
function BaseComponent() { ... }

// 用 HOC 增强
const EnhancedComponent = withRedux(
  withMemory(
    withTools(BaseComponent)
  )
);
```
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
# LangChain 1.x 版本的导入路径更新
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    # LangChain 新版本可能在不同位置
    try:
        from langchain_core.agents import create_tool_calling_agent
        from langchain.agents import AgentExecutor
    except ImportError:
        create_tool_calling_agent = None
        AgentExecutor = None

from langchain_community.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# LangChain 1.x 中 memory 模块已移动
try:
    from langchain.memory import ConversationBufferMemory
except ImportError:
    # 如果找不到，使用简单的列表替代
    ConversationBufferMemory = None

from .base_agent import BaseAgent
from config.settings import settings


class MemoryManager:
    """
    对话记忆管理器
    
    【前端类比】
    就像前端的本地存储管理（localStorage/sessionStorage）
    或者 Redux Persist（持久化 Redux state）
    
    作用：
    - 保存对话历史（类似保存表单数据）
    - 限制历史记录长度（类似 limit + offset 分页）
    - 提供记忆摘要（类似数据聚合）
    
    类似：
    ```javascript
    class MemoryManager {
      constructor(maxTurns = 20) {
        this.maxTurns = maxTurns;
        this.memory = [];  // 类似 localStorage
      }
      
      addMessage(user, assistant) {
        this.memory.push({ user, assistant });
        if (this.memory.length > this.maxTurns) {
          this.memory.shift();  // 删除最早的记录
        }
      }
    }
    ```
    """
    
    def __init__(self, max_turns: int = 20):
        """
        初始化记忆管理器
        
        Args:
            max_turns: 最大保留的对话轮数（类似分页的 pageSize）
        """
        self.max_turns = max_turns
        # LangChain 1.x 中 ConversationBufferMemory 可能不可用，使用简单列表
        if ConversationBufferMemory:
            self.memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        else:
            # 降级方案：使用简单列表存储
            self.memory = []
    
    def add_message(self, user_msg: str, assistant_msg: str):
        """添加对话消息"""
        if ConversationBufferMemory:
            self.memory.save_context(
                {"input": user_msg},
                {"output": assistant_msg}
            )
        else:
            # 简单列表实现
            self.memory.append({"user": user_msg, "assistant": assistant_msg})
            # 限制长度
            if len(self.memory) > self.max_turns:
                self.memory.pop(0)
    
    def get_recent_messages(self, n: int = None) -> List[Dict]:
        """获取最近的对话消息"""
        if n is None:
            n = self.max_turns
        
        # 简化实现，实际应该从 memory 中提取
        return []
    
    def clear(self):
        """清空记忆"""
        self.memory.clear()


class AdvancedAgent(BaseAgent):
    """
    高级智能体
    支持：
    - 工具调用（类似 Middleware/Plugins）
    - 长期记忆（类似 Redux Persist）
    - 多步推理（类似 Promise Chain）
    - 自定义系统提示（类似组件配置）
    
    【前端类比】
    就像一个用 Redux + Middleware + Persist 增强的 React 组件：
    ```javascript
    const AdvancedComponent = compose(
      withTools([calculator, search]),      // 中间件
      withMemory({ maxTurns: 20 }),         // 持久化
      withSystemPrompt("You are helpful")   // 配置
    )(BaseComponent);
    ```
    """
    
    def __init__(
        self,
        name: str = "高级助手",
        model: str = None,
        tools: List[Any] = None,
        system_prompt: str = None,
        temperature: float = 0.7,
        enable_memory: bool = True,
        max_memory_turns: int = 20
    ):
        super().__init__(name)
        
        # 配置模型
        self.model = model or settings.OPENAI_MODEL
        self.temperature = temperature
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL,  # 支持 DeepSeek
            max_tokens=2048,  # 增加最大输出长度
            timeout=60  # 增加超时时间
        )
        
        # 系统提示词
        self.system_prompt = system_prompt or (
            f"你是一个名为 {name} 的高级AI助手。\n"
            "你具备以下能力：\n"
            "1. 理解和分析复杂问题\n"
            "2. 使用工具获取信息和执行任务\n"
            "3. 记住对话历史并提供连贯的回答\n"
            "4. 进行多步推理和问题分解\n\n"
            "请保持专业、准确和 helpful。"
        )
        
        # 记忆管理器
        self.enable_memory = enable_memory
        if enable_memory:
            self.memory_manager = MemoryManager(max_turns=max_memory_turns)
        else:
            self.memory_manager = None
        
        # 工具列表
        self.tools = tools or []
        
        # 检查 Agent Executor 是否可用
        self.agent_executor_available = (
            create_tool_calling_agent is not None and 
            AgentExecutor is not None
        )
        
        # 创建 Agent Executor
        if self.tools and self.agent_executor_available:
            self._setup_agent_executor()
        else:
            self.agent_executor = None
            if self.tools and not self.agent_executor_available:
                print("警告: Agent Executor 不可用，将使用简单对话模式")
    
    def _setup_agent_executor(self):
        """
        设置 Agent Executor
        
        【前端类比】
        就像配置 Redux middleware 链
        """
        if not self.agent_executor_available:
            print("警告: Agent Executor 不可用，跳过工具设置")
            return
        
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 转换工具为 LangChain 格式
        langchain_tools = []
        for tool in self.tools:
            if isinstance(tool, dict):
                langchain_tools.append(Tool(
                    name=tool["name"],
                    func=tool["func"],
                    description=tool["description"]
                ))
            elif hasattr(tool, 'to_langchain_tool'):
                # MCP Tool Wrapper
                langchain_tools.append(tool.to_langchain_tool())
            else:
                langchain_tools.append(tool)
        
        try:
            # 创建工具调用 agent
            agent = create_tool_calling_agent(
                llm=self.llm,
                tools=langchain_tools,
                prompt=prompt
            )
            
            # 创建 executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=langchain_tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5
            )
        except Exception as e:
            print(f"设置 Agent Executor 失败: {e}")
            self.agent_executor = None
    
    def process(self, message: str) -> str:
        """处理用户输入"""
        try:
            # 添加用户消息到历史
            self.add_to_history("user", message)
            
            if self.agent_executor:
                # 使用 Agent Executor（支持工具调用）
                langchain_messages = self._convert_to_langchain_messages()
                
                response = self.agent_executor.invoke({
                    "messages": langchain_messages
                })
                
                assistant_message = response.get("output", "")
            else:
                # 简单对话模式
                from langchain_core.messages import HumanMessage
                
                response = self.llm.invoke([
                    ("system", self.system_prompt),
                    *self._convert_to_langchain_messages(),
                ])
                
                assistant_message = response.content
            
            # 添加 AI 响应到历史
            self.add_to_history("assistant", assistant_message)
            
            # 保存到记忆
            if self.enable_memory and self.memory_manager:
                self.memory_manager.add_message(message, assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _convert_to_langchain_messages(self) -> List:
        """将对话历史转换为 LangChain 消息格式"""
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        
        messages = []
        for msg in self.conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
        return messages
    
    def add_tool(self, tool: Any):
        """动态添加工具"""
        self.tools.append(tool)
        # 重新设置 agent executor
        if self.tools:
            self._setup_agent_executor()
    
    def remove_tool(self, tool_name: str):
        """移除工具"""
        self.tools = [t for t in self.tools if not (
            (isinstance(t, dict) and t.get("name") == tool_name) or
            (hasattr(t, 'name') and t.name == tool_name)
        )]
        
        # 重新设置 agent executor
        if self.tools:
            self._setup_agent_executor()
        else:
            self.agent_executor = None
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        if self.memory_manager:
            return f"记忆已启用，最大保留 {self.memory_manager.max_turns} 轮对话"
        return "记忆未启用"
    
    def reset(self):
        """重置对话历史和记忆"""
        super().reset()
        if self.memory_manager:
            self.memory_manager.clear()


class ReasoningAgent(AdvancedAgent):
    """
    推理智能体
    专门用于复杂问题的分步推理
    """
    
    def __init__(self, **kwargs):
        # 设置专门的系统提示
        kwargs.setdefault("system_prompt", (
            "你是一个专业的推理助手。\n"
            "面对复杂问题时，你会：\n"
            "1. 分析问题，识别关键要素\n"
            "2. 将大问题分解为小问题\n"
            "3. 逐步推理，展示思考过程\n"
            "4. 综合各部分得出最终结论\n\n"
            "请用清晰、逻辑性强的方式回答问题。"
        ))
        
        super().__init__(**kwargs)
    
    def process_with_reasoning(self, message: str) -> Dict[str, str]:
        """
        处理问题并返回推理过程
        
        Returns:
            包含推理步骤和最终答案的字典
        """
        reasoning_prompt = (
            f"{message}\n\n"
            "请按以下步骤回答：\n"
            "1. 问题分析\n"
            "2. 推理过程\n"
            "3. 最终答案\n\n"
            "请明确标注每个部分。"
        )
        
        full_response = self.process(reasoning_prompt)
        
        # 简单解析响应（实际可以更复杂）
        return {
            "full_response": full_response,
            "reasoning": full_response
        }
