"""
启动脚本 - 自动设置 Python 路径
解决 ModuleNotFoundError 问题
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"项目根目录: {project_root}")
print(f"Python 路径: {sys.path[:3]}")
print("-" * 60)

# 导入并运行主程序
from examples.full_stack_demo import main

if __name__ == "__main__":
    main()
