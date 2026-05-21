# 🚀 DeepSeek API 配置指南

## ✅ 已配置完成

你的项目已经配置为使用 **DeepSeek API**！

### 当前配置

```env
OPENAI_API_KEY=sk-fa624a075a2f4b8db4015e1d9c53285b
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

---

## 📝 DeepSeek 简介

**DeepSeek** 是一个强大的中文 AI 模型提供商，优势：

✅ **中文理解能力强** - 对中文支持更好  
✅ **价格实惠** - 比 OpenAI 便宜很多  
✅ **国内访问快** - 不需要科学上网  
✅ **API 兼容** - 与 OpenAI API 格式兼容  

---

## 🎯 可用模型

| 模型 | 说明 | 适用场景 |
|------|------|---------|
| `deepseek-chat` | 对话模型（默认） | 通用对话、问答 |
| `deepseek-coder` | 代码专用模型 | 编程、代码生成 |
| `deepseek-reasoner` | 推理模型 | 复杂推理、数学 |

---

## 💰 DeepSeek 定价

### deepseek-chat

- **输入**: ¥0.001 / 1K tokens
- **输出**: ¥0.002 / 1K tokens
- **约**: $0.00014 / 1K tokens（非常便宜！）

### 对比 OpenAI

| 服务商 | 模型 | 价格（每百万 tokens） |
|--------|------|---------------------|
| DeepSeek | deepseek-chat | ¥1-2 |
| OpenAI | gpt-3.5-turbo | $0.5-1.5 |
| OpenAI | gpt-4 | $10-30 |

**DeepSeek 便宜 10-100 倍！** 🎉

---

## 🔑 获取 DeepSeek API Key

1. **访问官网**
   ```
   https://platform.deepseek.com/
   ```

2. **注册/登录**
   - 支持手机号注册
   - 微信扫码登录

3. **创建 API Key**
   - 进入 "API Keys" 页面
   - 点击 "创建新密钥"
   - 复制 Key（格式：`sk-xxxxx`）

4. **充值（可选）**
   - 新用户有免费额度
   - 后续可按需充值

---

## ✅ 验证配置

运行测试：

```bash
python run.py
```

应该能看到正常的 AI 回复，不再出现超时错误。

---

## 🎓 DeepSeek 特点

### 优势

1. **中文优化**
   - 更好的中文理解
   - 更符合中文表达习惯

2. **速度快**
   - 国内服务器
   - 延迟低

3. **成本低**
   - 价格只有 OpenAI 的 1/10
   - 适合大量使用

4. **易用性**
   - API 完全兼容 OpenAI
   - 无需修改代码

### 注意事项

1. **英文能力**
   - 英文也不错，但略逊于 GPT-4
   - 日常使用完全够用

2. **最新知识**
   - 训练数据截止到 2024 年
   - 最新事件可能不知道

---

## 🔧 切换模型

如果想使用其他 DeepSeek 模型，修改 `.env` 文件：

### 使用代码模型
```env
OPENAI_MODEL=deepseek-coder
```

### 使用推理模型
```env
OPENAI_MODEL=deepseek-reasoner
```

---

## 📊 使用建议

### 推荐场景

✅ **中文对话** - 客服、问答  
✅ **代码生成** - 使用 deepseek-coder  
✅ **内容创作** - 文章、文案  
✅ **学习实验** - 成本低，随便用  

### 不太适合

❌ **需要最新信息** - 训练数据有截止  
❌ **极高精度要求** - GPT-4 略强  
❌ **纯英文专业场景** - OpenAI 更优  

---

## 🚀 开始使用

配置已完成，直接运行：

```bash
python run.py
```

享受快速、便宜的 AI 服务吧！🎉

---

## 📚 相关资源

- [DeepSeek 官网](https://platform.deepseek.com/)
- [API 文档](https://platform.deepseek.com/docs)
- [ pricing](https://platform.deepseek.com/pricing)

---

**祝你使用愉快！** 😊
