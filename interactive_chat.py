"""
交互式 AI 对话程序
你可以实时输入问题与 AI 对话
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

from agents import ChatAgent, LangChainAgent, AdvancedAgent


def chat_with_agent():
    """与 Agent 进行交互式对话"""
    
    print("=" * 60)
    print("🤖 AI 智能对话助手")
    print("=" * 60)
    print()
    
    # 选择 Agent 类型
    print("请选择 Agent 类型：")
    print("1. ChatAgent - 基础对话（快速）")
    print("2. LangChainAgent - LangChain 增强（推荐）")
    print("3. AdvancedAgent - 高级功能（带记忆）")
    print()
    
    choice = input("请输入选项 (1/2/3，默认 2): ").strip()
    
    # 创建 Agent
    if choice == "1":
        agent = ChatAgent(name="AI助手")
        print("\n✅ 已选择: ChatAgent（基础对话）")
    elif choice == "3":
        agent = AdvancedAgent(name="AI助手", enable_memory=True)
        print("\n✅ 已选择: AdvancedAgent（高级功能，带记忆）")
    else:
        agent = LangChainAgent(name="AI助手", temperature=0.7)
        print("\n✅ 已选择: LangChainAgent（LangChain 增强）")
    
    print()
    print("-" * 60)
    print("💡 提示:")
    print("  - 直接输入问题开始对话")
    print("  - 输入 'quit' 或 'exit' 退出")
    print("  - 输入 'clear' 清空对话历史")
    print("  - 输入 'help' 查看帮助")
    print("-" * 60)
    print()
    
    # 开始对话循环
    while True:
        try:
            # 获取用户输入
            user_input = input("👤 你: ").strip()
            
            # 处理特殊命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！感谢使用！")
                break
            
            elif user_input.lower() == 'clear':
                agent.reset()
                print("✅ 对话历史已清空\n")
                continue
            
            elif user_input.lower() == 'help':
                print("\n📖 帮助信息:")
                print("  quit/exit/q - 退出对话")
                print("  clear       - 清空对话历史")
                print("  help        - 显示此帮助信息")
                print("  history     - 查看对话历史")
                print()
                continue
            
            elif user_input.lower() == 'history':
                history = agent.get_history()
                if history:
                    print(f"\n📜 对话历史（共 {len(history)} 条）:")
                    for i, msg in enumerate(history[-5:], 1):  # 只显示最近5条
                        role = "👤 你" if msg["role"] == "user" else "🤖 AI"
                        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                        print(f"  {i}. {role}: {content}")
                else:
                    print("\n📜 暂无对话历史")
                print()
                continue
            
            # 检查是否为空输入
            if not user_input:
                print("⚠️  请输入问题\n")
                continue
            
            # 处理用户问题
            print("🤖 AI: ", end="", flush=True)
            
            try:
                response = agent.process(user_input)
                print(response)
                print()
                
            except Exception as e:
                print(f"\n❌ 错误: {e}\n")
                print("💡 提示: 请检查 API Key 和网络连接\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 检测到中断，再见！")
            break
        
        except EOFError:
            print("\n\n👋 输入结束，再见！")
            break


def main():
    """主函数"""
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 未设置 OPENAI_API_KEY")
        print("\n请在 .env 文件中配置你的 API Key")
        print("参考: .env.example 文件")
        return
    
    try:
        chat_with_agent()
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n💡 建议:")
        print("  1. 检查 .env 文件配置是否正确")
        print("  2. 确认 API Key 有效")
        print("  3. 检查网络连接")


if __name__ == "__main__":
    main()
