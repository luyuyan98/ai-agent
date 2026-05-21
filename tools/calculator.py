"""
计算工具
"""


def calculate(expression: str) -> str:
    """
    执行数学计算
    
    Args:
        expression: 数学表达式字符串，如 "2 + 3 * 4"
    
    Returns:
        计算结果字符串
    """
    try:
        # 只允许安全的数学运算
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含非法字符"
        
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"


def add(a: float, b: float) -> float:
    """加法"""
    return a + b


def subtract(a: float, b: float) -> float:
    """减法"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法"""
    return a * b


def divide(a: float, b: float) -> float:
    """除法"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
