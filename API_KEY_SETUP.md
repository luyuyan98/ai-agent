# 🔑 OpenAI API Key 配置指南

## 📝 当前状态

✅ 程序已经成功运行  
✅ 所有模块导入正常  
✅ MCP 工具集成成功  
⏳ 只需要配置 API Key 即可启用完整功能

---

## 🚀 快速配置步骤

### 第 1 步：获取 OpenAI API Key

1. **访问 OpenAI 平台**
   ```
   https://platform.openai.com/
   ```

2. **注册/登录账号**
   - 如果没有账号，先注册
   - 已有账号直接登录

3. **进入 API Keys 页面**
   - 点击右上角头像
   - 选择 "API keys"
   - 或直接访问：https://platform.openai.com/api-keys

4. **创建新的 API Key**
   - 点击 "Create new secret key"
   - 给 key 起个名字（如：My AI Agent）
   - 点击 "Create secret key"

5. **复制 API Key**
   - ⚠️ **重要**: Key 只会显示一次！
   - 立即复制到安全的地方
   - 格式类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### 第 2 步：配置到项目

我已经为你创建了 `.env` 文件，现在需要填入真实的 API Key。

**方法 1: 直接编辑文件**

打开项目根目录的 `.env` 文件，将：
```env
OPENAI_API_KEY=sk-your-api-key-here
```

改为：
```env
OPENAI_API_KEY=sk-你的真实API-Key-在这里
```

**方法 2: 使用 PowerShell 命令**

```powershell
# 替换为你的真实 API Key
$apiKey = "sk-你的真实API-Key-在这里"
Set-Content -Path ".env" -Value "OPENAI_API_KEY=$apiKey"
```

---

### 第 3 步：验证配置

运行测试脚本：

```bash
python simple_test.py
```

应该看到所有模块都显示 ✅

然后运行完整示例：

```bash
python run.py
```

现在应该能看到完整的 AI 对话功能了！

---

## 💰 费用说明

### OpenAI API 定价

| 模型 | 输入价格 | 输出价格 |
|------|---------|---------|
| gpt-3.5-turbo | $0.0005/1K tokens | $0.0015/1K tokens |
| gpt-4 | $0.03/1K tokens | $0.06/1K tokens |

### 免费额度

- 新注册用户有 **$5 免费额度**
- 有效期：3 个月
- 足够学习和测试使用

### 估算成本

对于本项目示例：
- 每次对话约 100-500 tokens
- $5 免费额度可以进行 **数千次对话**
- 完全够用！

---

## 🔒 安全提示

### ⚠️ 重要安全规则

1. **永远不要公开 API Key**
   - ❌ 不要上传到 GitHub
   - ❌ 不要分享给他人
   - ❌ 不要在公共场合展示

2. **.env 文件已加入 .gitignore**
   - ✅ 不会被提交到 Git
   - ✅ 本地保存，安全

3. **定期轮换 Key**
   - 建议每 3-6 个月更换一次
   - 在 OpenAI 平台可以撤销旧 Key

4. **监控使用情况**
   - 定期检查用量
   - 设置使用限额

---

## ❓ 常见问题

### Q1: 没有信用卡能注册吗？

**A:** 是的！OpenAI 提供 $5 免费额度，不需要信用卡。

### Q2: API Key 泄露了怎么办？

**A:** 
1. 立即在 OpenAI 平台撤销该 Key
2. 创建新的 Key
3. 更新 `.env` 文件

### Q3: 可以使用其他模型吗？

**A:** 可以！修改 `.env` 文件：
```env
OPENAI_MODEL=gpt-4
```

可用模型：
- `gpt-3.5-turbo` (推荐，便宜)
- `gpt-4` (更强大，较贵)
- `gpt-4-turbo` (最新)

### Q4: 如何查看用量？

**A:** 
1. 访问 https://platform.openai.com/usage
2. 查看当前周期用量
3. 监控花费

### Q5: 不想用 OpenAI 可以吗？

**A:** 可以！项目支持其他 LLM：
- Anthropic Claude
- Google Gemini
- 本地模型（Ollama）

需要修改代码中的 LLM 初始化部分。

---

## 🎯 配置完成后的测试

### 测试 1: 简单对话

```bash
python run.py
```

应该看到：
- ✅ 示例 1-5: AI 正常回复
- ✅ 示例 6: MCP 工具展示
- ✅ 示例 7-8: Agent 协作演示

### 测试 2: 交互式对话

创建一个简单的测试文件 `test_chat.py`:

```python
from agents import ChatAgent

agent = ChatAgent(name="助手")

print("开始对话（输入 'quit' 退出）\n")

while True:
    user_input = input("你: ")
    if user_input.lower() == 'quit':
        break
    
    response = agent.process(user_input)
    print(f"AI: {response}\n")
```

运行：
```bash
python test_chat.py
```

---

## 📚 下一步

配置好 API Key 后：

1. **阅读文档**
   - [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) - 前端开发者指南
   - [QUICKSTART.md](QUICKSTART.md) - 快速开始

2. **运行示例**
   ```bash
   python run.py
   ```

3. **开始开发**
   - 修改示例代码
   - 创建自己的 Agent
   - 添加自定义工具

4. **探索 MCP 工具**
   - GitHub 集成
   - 网页抓取
   - 浏览器自动化

---

## 💡 小贴士

### 节省 API 费用

1. **使用 gpt-3.5-turbo**
   - 比 GPT-4 便宜 10-60 倍
   - 对大多数任务足够好

2. **优化 Prompt**
   - 简洁明了
   - 避免冗余信息

3. **缓存结果**
   - 相同问题不重复调用
   - 保存常用回答

4. **设置限额**
   - 在 OpenAI 平台设置月度限额
   - 防止意外高额费用

---

## 🆘 需要帮助？

如果遇到问题：

1. **检查 API Key 格式**
   - 应该以 `sk-` 开头
   - 长度约 50 字符

2. **检查网络连接**
   - 确保能访问 openai.com
   - 可能需要科学上网

3. **查看错误信息**
   - 仔细阅读错误提示
   - 通常是配置问题

4. **查阅文档**
   - [OpenAI 官方文档](https://platform.openai.com/docs)
   - 项目文档

---

**配置完成后，你就可以体验完整的 AI Agent 功能了！** 🎉
