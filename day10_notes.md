# Day 10：项目 1 收官——网页版聊天机器人

> 把 Day 7 的命令行机器人升级成网页版，用 Streamlit（Python 库，不用学前端）。
> 这是计划里「项目 1」的完成节点：**命令行 + 网页版** 都有了。

## 安装依赖（第一次）

```bash
pip install streamlit python-dotenv requests
```

## 运行

```bash
cd C:\Users\xjl\Desktop\AI学习\练习\day10
streamlit run app.py
```

浏览器自动打开 http://localhost:8501 。前提：本文件夹有 `.env`（复制 day7 的过来）。

## 今天要搞懂的三件事

1. **`st.session_state` 是什么**：Streamlit 页面每操作一次就「重跑整个脚本」，变量会被清空；
   存进 `st.session_state` 的才会保留。聊天记录就是靠它「记住」的。这是 Streamlit 的核心概念。
2. **多轮对话搬到网页**：和 Day 7 命令行完全一样的逻辑（messages 历史 + 每次整体重发），
   只是把 `input()` 换成了 `st.chat_input()`，把 `print()` 换成了 `st.markdown()`。
3. **改人设**：改 `st.session_state.消息` 初始化的那条 system 提示词，机器人性格就变了——试试。

## 加分改造（选做）

- 加 `temperature=0.7` 到 请求() 里（Day 9 学过的温度）
- 把 `usage` 显示到 `st.sidebar`（侧边栏），实时看 token 花费（Day 7 学过的）
- 加一个「清空对话」按钮：
  ```python
  if st.button("清空对话"):
      st.session_state.消息 = [st.session_state.消息[0]]  # 只留 system
      st.rerun()
  ```

## 里程碑达成标准

- [ ] `streamlit run app.py` 能打开网页，聊几轮能记住上下文
- [ ] 能说出 `st.session_state` 为什么存在
- [ ] 把整个 day10 文件夹推到 GitHub（git add . → commit → push）
- [ ] README 写上：这是什么、怎么运行、截图
