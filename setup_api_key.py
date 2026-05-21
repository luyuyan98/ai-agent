"""
API Key 配置助手
帮助快速设置 OpenAI API Key
"""

import os


def setup_api_key():
    """交互式设置 API Key"""
    
    print("=" * 60)
    print("OpenAI API Key 配置助手")
    print("=" * 60)
    print()
    
    print("📝 如何获取 API Key:")
    print("1. 访问: https://platform.openai.com/api-keys")
    print("2. 登录/注册账号")
    print("3. 点击 'Create new secret key'")
    print("4. 复制生成的 Key")
    print()
    
    print("⚠️  安全提示:")
    print("- API Key 只会显示一次，请立即保存")
    print("- 不要分享给他人")
    print("- .env 文件不会上传到 Git")
    print()
    
    # 获取用户输入
    api_key = input("请粘贴你的 API Key (以 sk- 开头): ").strip()
    
    # 验证格式
    if not api_key.startswith("sk-"):
        print()
        print("❌ 错误: API Key 应该以 'sk-' 开头")
        print("   请检查是否复制完整")
        return False
    
    if len(api_key) < 20:
        print()
        print("❌ 错误: API Key 长度不正确")
        print("   请检查是否复制完整")
        return False
    
    # 写入 .env 文件
    env_content = f"""# OpenAI API 配置
OPENAI_API_KEY={api_key}

# 模型配置（可选）
OPENAI_MODEL=gpt-3.5-turbo

# 日志级别（可选）
LOG_LEVEL=INFO
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print()
        print("✅ API Key 已成功保存到 .env 文件")
        print()
        print("🎉 配置完成！")
        print()
        print("现在可以运行:")
        print("  python run.py")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ 保存失败: {e}")
        return False


def verify_api_key():
    """验证 API Key 是否已配置"""
    
    print("=" * 60)
    print("验证 API Key 配置")
    print("=" * 60)
    print()
    
    # 检查 .env 文件
    if not os.path.exists(".env"):
        print("❌ .env 文件不存在")
        print()
        print("请运行配置助手:")
        print("  python setup_api_key.py")
        return False
    
    # 读取并检查
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "OPENAI_API_KEY=" in content:
        # 提取 key（部分隐藏）
        for line in content.split("\n"):
            if line.startswith("OPENAI_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key and key != "sk-your-api-key-here":
                    hidden_key = key[:8] + "..." + key[-4:]
                    print(f"✅ 检测到 API Key: {hidden_key}")
                    print()
                    print("配置正确！可以运行:")
                    print("  python run.py")
                    return True
                else:
                    print("⚠️  API Key 未配置或使用占位符")
                    print()
                    print("请重新配置:")
                    print("  python setup_api_key.py")
                    return False
    
    print("❌ 未在 .env 文件中找到 OPENAI_API_KEY")
    print()
    print("请运行配置助手:")
    print("  python setup_api_key.py")
    return False


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--verify":
            verify_api_key()
        else:
            print("用法:")
            print("  python setup_api_key.py          # 配置 API Key")
            print("  python setup_api_key.py --verify # 验证配置")
    else:
        setup_api_key()


if __name__ == "__main__":
    main()
