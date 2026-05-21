"""
AI 智能体主程序
演示如何使用不同类型的智能体
"""

import sys
from agents.simple_agent import SimpleAgent
from utils.helpers import print_welcome, save_conversation


def run_simple_agent():
    """运行简单规则智能体（无需 API）"""
    print("\n=== 启动简单智能体 ===")
    agent = SimpleAgent(name="小助手")
    print_welcome(agent.name)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 检查退出命令
            if user_input.lower() in ["退出", "quit", "exit", "q"]:
                print("再见！")
                # 保存对话历史
                save_conversation(agent.get_history())
                break
            
            # 处理用户输入
            response = agent.process(user_input)
            print(f"{agent.name}: {response}")
            
        except KeyboardInterrupt:
            print("\n\n检测到中断，再见！")
            save_conversation(agent.get_history())
            break
        except Exception as e:
            print(f"发生错误: {e}")


def run_chat_agent():
    """运行 OpenAI 对话智能体（需要 API Key）"""
    print("\n=== 启动 OpenAI 智能体 ===")
    
    try:
        from agents.chat_agent import ChatAgent
        
        # 创建智能体
        agent = ChatAgent(name="AI助手", model="gpt-3.5-turbo")
        print_welcome(agent.name)
        
        while True:
            try:
                user_input = input("\n你: ").strip()
                
                if not user_input:
                    continue
                
                # 检查退出命令
                if user_input.lower() in ["退出", "quit", "exit", "q"]:
                    print("再见！")
                    save_conversation(agent.get_history())
                    break
                
                # 处理用户输入
                print(f"{agent.name}: 思考中...")
                response = agent.process(user_input)
                print(f"{agent.name}: {response}")
                
            except KeyboardInterrupt:
                print("\n\n检测到中断，再见！")
                save_conversation(agent.get_history())
                break
            except Exception as e:
                print(f"发生错误: {e}")
                
    except ImportError:
        print("错误: 未安装 openai 库")
        print("请运行: pip install openai python-dotenv")
    except ValueError as e:
        print(f"错误: {e}")
        print("请在 .env 文件中设置 OPENAI_API_KEY")


def main():
    """主函数"""
    print("=" * 50)
    print("AI 智能体演示程序")
    print("=" * 50)
    print("\n请选择智能体类型:")
    print("1. 简单智能体（无需 API，基于规则）")
    print("2. OpenAI 智能体（需要 API Key）")
    print("0. 退出")
    
    choice = input("\n请输入选择 (0-2): ").strip()
    
    if choice == "1":
        run_simple_agent()
    elif choice == "2":
        run_chat_agent()
    elif choice == "0":
        print("再见！")
    else:
        print("无效选择")


if __name__ == '__main__':
    main()
