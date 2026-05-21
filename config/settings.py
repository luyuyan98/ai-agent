"""
项目配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings:
    """应用配置"""
    
    # OpenAI/DeepSeek API 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
    
    # 应用配置
    APP_NAME = "AI智能体"
    VERSION = "1.0.0"
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
