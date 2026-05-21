"""
基础智能体类 - 所有智能体的基类

【前端类比】
这就像 React/Vue 中的 Component 基类或 TypeScript 的 Interface
定义了所有 Agent 必须实现的基本方法和属性
类似于前端的 "组件接口规范"
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAgent(ABC):
    """
    基础智能体抽象类
    
    【前端类比】
    就像一个抽象的 React Component 基类，或者 TypeScript 的 Interface
    定义了所有子类必须实现的方法（类似 interface 中的必需方法）
    
    相当于：
    ```typescript
    interface BaseAgent {
      name: string;
      conversationHistory: Array<{role: string, content: string}>;
      process(message: string): string;  // 必须实现
      reset(): void;
      getHistory(): Array<any>;
    }
    ```
    """
    
    def __init__(self, name: str = "AI助手"):
        """
        初始化 Agent
        
        【前端类比】
        就像 React 组件的 constructor 或 Vue 的 data()
        设置组件的初始状态和属性
        
        Args:
            name: Agent 的名字，类似组件的 displayName
        """
        self.name = name  # Agent 的名称（类似组件名）
        self.conversation_history: List[Dict[str, str]] = []  # 对话历史（类似 state）
    
    @abstractmethod
    def process(self, message: str) -> str:
        """
        处理用户输入并返回响应（必须实现的抽象方法）
        
        【前端类比】
        就像 React 组件中必须实现的 render() 方法
        或者 Vue 组件中必须定义的方法
        
        相当于 TypeScript 接口中的必需方法：
        ```typescript
        process(message: string): string;  // 子类必须实现
        ```
        
        Args:
            message: 用户输入的消息
            
        Returns:
            AI 的回复消息
        """
        pass
    
    def reset(self):
        """
        重置对话历史
        
        【前端类比】
        就像清空组件的 state，或者调用 setState({})
        让组件回到初始状态
        
        类似：
        ```javascript
        this.setState({ conversationHistory: [] });
        ```
        """
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史的副本
        
        【前端类比】
        就像获取组件的 state，但返回的是副本（防止外部修改）
        类似 Redux 中的 getState() 返回不可变数据
        
        Returns:
            对话历史列表的副本
        """
        return self.conversation_history.copy()  # 返回副本，保护内部状态
    
    def add_to_history(self, role: str, content: str):
        """
        添加消息到历史记录
        
        【前端类比】
        就像更新组件的 state，往数组中添加新元素
        类似：
        ```javascript
        this.setState(prevState => ({
          conversationHistory: [...prevState.conversationHistory, {role, content}]
        }));
        ```
        
        Args:
            role: 角色类型（"user" 或 "assistant"）
            content: 消息内容
        """
        self.conversation_history.append({"role": role, "content": content})
