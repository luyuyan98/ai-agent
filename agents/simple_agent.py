"""
简单的规则-based 智能体（无需 API）
"""

import random
from datetime import datetime
from .base_agent import BaseAgent


class SimpleAgent(BaseAgent):
    """基于规则的简单智能体"""
    
    def __init__(self, name: str = "小助手"):
        super().__init__(name)
        self.commands = {
            "你好": self._greet,
            "时间": self._get_time,
            "帮助": self._help,
            "笑话": self._tell_joke,
            "日期": self._get_date,
        }
    
    def _greet(self) -> str:
        return f"你好！我是{self.name}，很高兴见到你！"
    
    def _get_time(self) -> str:
        return f"当前时间是: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _get_date(self) -> str:
        return f"今天是: {datetime.now().strftime('%Y年%m月%d日 %A')}"
    
    def _help(self) -> str:
        commands = ", ".join(self.commands.keys())
        return f"可用命令: {commands}、退出"
    
    def _tell_joke(self) -> str:
        jokes = [
            "为什么程序员喜欢黑暗？因为光有 bug。",
            "什么是程序员最害怕的东西？bug！",
            "为什么 Python 开发者很冷静？因为他们有很多 import 的库可以用。",
            "程序员的三个愿望：没有 bug、需求不变、准时下班。",
            "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25。"
        ]
        return random.choice(jokes)
    
    def process(self, message: str) -> str:
        """处理用户输入"""
        # 添加用户消息到历史
        self.add_to_history("user", message)
        
        # 查找匹配的命令
        for key, handler in self.commands.items():
            if key in message.lower():
                response = handler()
                self.add_to_history("assistant", response)
                return response
        
        # 默认响应
        response = f"抱歉，我不理解'{message}'。输入'帮助'查看可用命令。"
        self.add_to_history("assistant", response)
        return response
