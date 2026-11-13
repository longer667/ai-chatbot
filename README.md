# AI 网页聊天机器人（Day 10 · 项目 1）

## 这是什么

一个跑在浏览器里的 AI 聊天机器人。基于 DeepSeek API，支持多轮对话——它能记住你前面说过的话，
而不是每句都从零开始。

这是我的 AI 应用开发学习计划里**第 1 个项目**：先把 DeepSeek API 用裸代码调通（Day 6-9），
再用 Streamlit 把它变成能给人用的网页（Day 10）。

## 功能

- **多轮对话**：完整保留对话历史，模型能接上文
- **温度调节**：侧边栏滑杆实时调整 `temperature`（0 = 稳定，1.5 = 发散）
- **Token 用量**：侧边栏实时累计输入/输出 token，用量心里有数
- **清空对话**：一键重置聊天记录和用量统计
- **错误兜底**：API 出错时显示友好提示，页面不会崩

## 技术栈

- **Python 3** + **Streamlit**（界面，不用写前端）
- **DeepSeek API**（`deepseek-chat` 模型）
- **requests**（HTTP 调用）+ **python-dotenv**（密钥管理）

## 怎么运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥：在本目录或上级目录建 .env，写入
#    DEEPSEEK_API_KEY=你的key
#    （key 在 https://platform.deepseek.com 申请）

# 3. 启动
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501 。

> `.env` 已在 `.gitignore` 里，密钥不会进仓库。

## 关键实现

### `st.session_state`：Streamlit 的"内存"

Streamlit 的运行模型和普通脚本相反——**用户每次操作，整个脚本从头重跑一遍**，
所以普通变量会被清空：

```python
消息 = []                      # 下次交互就丢了
st.session_state.消息 = []     # 会保留
```

聊天记录、token 累计、温度设置这些需要跨交互存活的东西，全部放在 `st.session_state` 里。
这是 Streamlit 最核心、也最容易踩的概念。

### 对话历史

和命令行版逻辑完全一样：维护一个 `messages` 列表，每轮把 user 和 assistant 各追加一条，
请求时**整体重发**。模型本身没有记忆，"记住"全靠这个列表。

## 目录结构

```
day10/
├── app.py             # Streamlit 主程序
├── requirements.txt   # 依赖
├── README.md          # 本文件
├── .gitignore         # 挡住 .env 和缓存
└── day10_notes.md     # 学习笔记（要搞懂的三件事 + 验收标准）
```

## 踩坑记录

1. **模型选错导致每次回复等 20 秒**：一开始用 `deepseek-v4-flash`，它是推理模型，
   每次请求会先生成约 9700 字隐藏推理，单次耗时 20 秒，聊天场景下页面像卡死。
   换成 `deepseek-chat` 后降到 1~2 秒。
   > 经验：**Prompt 工程 / 聊天这类需要即时反馈的场景用非推理模型**；
   > 需要复杂推理的任务再用推理模型。

2. **`.env` 放哪**：`load_dotenv()` 会从脚本所在目录往上逐级查找，所以放在上级目录也能读到。
   但推到 GitHub 时 `.env` 必须被 `.gitignore` 挡住。

## 后续计划

- [ ] 流式输出（打字机效果）
- [ ] 部署到 Hugging Face Spaces，拿到公网链接（Day 24）
- [ ] 换成 RAG 知识库问答（项目 2）
