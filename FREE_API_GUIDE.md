# 🆓 免费 AI API 选择指南

## 💡 当前问题

你的 DeepSeek 账户余额不足（`Insufficient Balance`），需要：
- 充值，或
- 使用其他提供免费额度的服务

---

## 🎯 推荐的免费/低成本方案

### 方案 1: SiliconFlow（硅基流动）⭐ 推荐

**特点**：
- ✅ **免费额度多** - 新用户赠送较多额度
- ✅ **国内访问快** - 不需要代理
- ✅ **模型丰富** - 支持 Qwen、ChatGLM 等
- ✅ **价格便宜** - 比 DeepSeek 还便宜

**注册**：
```
https://siliconflow.cn/
```

**配置**：
```env
OPENAI_API_KEY=sk-your-siliconflow-key
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

---

### 方案 2: Moonshot（月之暗面/Kimi）

**特点**：
- ✅ Kimi 聊天机器人同款 API
- ✅ 中文能力强
- ✅ 有免费额度
- ✅ 长文本支持好

**注册**：
```
https://platform.moonshot.cn/
```

**配置**：
```env
OPENAI_API_KEY=sk-your-moonshot-key
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=moonshot-v1-8k
```

---

### 方案 3: 百度文心一言

**特点**：
- ✅ 百度大厂背书
- ✅ 有免费调用次数
- ✅ 中文优化

**注册**：
```
https://cloud.baidu.com/product/wenxinworkshop
```

**注意**：百度 API 格式略有不同，需要额外适配

---

### 方案 4: 继续用 DeepSeek（充值）

**优点**：
- ✅ 已经配置好
- ✅ 价格便宜（¥0.001-0.002 / 1K tokens）
- ✅ 中文能力强

**充值**：
- 最少 ¥10-50
- ¥10 可以进行数千次对话

---

## 📊 对比表格

| 服务商 | 免费额度 | 价格 | 中文能力 | 速度 | 推荐度 |
|--------|---------|------|---------|------|--------|
| **SiliconFlow** | ⭐⭐⭐⭐⭐ | 很便宜 | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Moonshot** | ⭐⭐⭐⭐ | 便宜 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| **DeepSeek** | ⭐⭐ | 便宜 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| **百度文心** | ⭐⭐⭐ | 中等 | ⭐⭐⭐⭐ | ⚡⚡⚡ | ⭐⭐⭐ |
| **OpenAI** | ⭐ | 贵 | ⭐⭐⭐ | ⚡⚡（需代理） | ⭐⭐ |

---

## 🚀 快速切换到 SiliconFlow

### 第 1 步：注册账号

访问 https://siliconflow.cn/ 并注册

### 第 2 步：获取 API Key

1. 登录后进入 "API Keys" 页面
2. 创建新的 API Key
3. 复制 Key（格式：`sk-xxxxx`）

### 第 3 步：修改 .env 文件

打开 `.env` 文件，改为：

```env
OPENAI_API_KEY=sk-你的siliconflow-key
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

### 第 4 步：测试

```bash
python run.py
```

---

## 💰 各平台价格参考

### SiliconFlow
- Qwen2.5-7B: ¥0.0005 / 1K tokens（超便宜！）
- 免费额度：新用户赠送较多

### Moonshot
- moonshot-v1-8k: ¥0.012 / 1K tokens
- 免费额度：有一定免费调用次数

### DeepSeek
- deepseek-chat: ¥0.001-0.002 / 1K tokens
- 免费额度：较少或已过期

---

## 🎓 建议

### 如果你是学生/学习者

**推荐 SiliconFlow**：
- 免费额度多
- 价格超低
- 足够学习使用

### 如果你需要高质量中文

**推荐 Moonshot 或 DeepSeek（充值）**：
- 中文能力最强
- 适合正式项目

### 如果只是想体验

**先用 SiliconFlow 免费额度**：
- 不用花钱
- 体验完整功能
- 满意后再考虑充值

---

## 🔧 切换 API 的步骤

无论选择哪个平台，步骤都一样：

1. **注册账号**
2. **获取 API Key**
3. **修改 `.env` 文件**
   ```env
   OPENAI_API_KEY=你的key
   OPENAI_BASE_URL=API地址
   OPENAI_MODEL=模型名称
   ```
4. **运行测试**
   ```bash
   python run.py
   ```

代码会自动适配，无需修改！

---

## ❓ 常见问题

### Q: 哪个平台的免费额度最多？

**A:** SiliconFlow 通常给的免费额度最多，适合学习使用。

### Q: 可以同时使用多个平台吗？

**A:** 可以！只需修改 `.env` 文件切换即可。

### Q: 免费额度用完后怎么办？

**A:** 
1. 注册新账号（用不同手机号/邮箱）
2. 或者充值继续使用
3. 或者切换到其他平台

### Q: API 格式都兼容吗？

**A:** 是的！这些平台都兼容 OpenAI API 格式，代码无需修改。

---

## 🎯 我的建议

**立即行动**：

1. **注册 SiliconFlow**（5分钟）
   ```
   https://siliconflow.cn/
   ```

2. **获取 API Key**

3. **修改 `.env` 文件**

4. **运行测试**
   ```bash
   python run.py
   ```

5. **开始免费使用！** 🎉

---

**SiliconFlow 是目前最推荐的免费/低成本方案！** 😊
