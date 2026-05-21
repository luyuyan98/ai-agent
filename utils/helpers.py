"""
辅助工具函数
"""

import json
from datetime import datetime
from typing import Any


def format_response(success: bool, data: Any = None, message: str = "") -> dict:
    """
    格式化响应数据
    
    Args:
        success: 是否成功
        data: 响应数据
        message: 响应消息
    
    Returns:
        格式化的响应字典
    """
    return {
        "success": success,
        "data": data,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }


def save_conversation(history: list, filename: str = "conversation.json"):
    """
    保存对话历史到文件
    
    Args:
        history: 对话历史列表
        filename: 文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"对话已保存到 {filename}")


def load_conversation(filename: str = "conversation.json") -> list:
    """
    从文件加载对话历史
    
    Args:
        filename: 文件名
    
    Returns:
        对话历史列表
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def clear_screen():
    """清屏"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome(agent_name: str):
    """打印欢迎信息"""
    print("=" * 50)
    print(f"欢迎使用 {agent_name}！")
    print("输入 '退出' 或 'quit' 结束对话")
    print("输入 '帮助' 查看可用命令")
    print("=" * 50)
