"""
基于 OpenAI API 的对话智能体
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .base_agent import BaseAgent


class ChatAgent(BaseAgent):
    """基于 OpenAI 的对话智能体"""
    
    def __init__(self, name: str = "AI助手", model: str = None, api_key: Optional[str] = None):
        super().__init__(name)
        
        # 加载环境变量
        load_dotenv()
        
        # 获取模型名称（优先使用参数，其次使用环境变量）
        self.model = model or os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        
        # 获取 API Key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数")
        
        if OpenAI is None:
            raise ImportError("请安装 openai 库: pip install openai")
        
        # 配置客户端，支持 SiliconFlow/DeepSeek 等兼容 API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
        )
    
    def process(self, message: str) -> str:
        """处理用户输入并返回 AI 响应"""
        try:
            # 添加用户消息到历史
            self.add_to_history("user", message)
            
            # 调用 OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=2048,  # 增加最大输出长度
                timeout=60  # 增加超时时间
            )
            
            # 获取 AI 响应
            assistant_message = response.choices[0].message.content
            
            # 添加 AI 响应到历史
            self.add_to_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(error_msg)
            return error_msg
