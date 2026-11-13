"""
Day 10：项目 1 收官——网页版聊天机器人
=====================================
把 Day 7 的命令行机器人升级成网页版。用 Streamlit：Python 库，
几行代码就能出聊天界面，不用学前端。

前置：
    1. pip install streamlit python-dotenv requests
    2. .env 里有 DEEPSEEK_API_KEY（练习/ 目录下那份会被自动往上找到）

运行：
    streamlit run app.py
浏览器会自动打开 http://localhost:8501

已包含的加分改造：
    - 侧边栏温度滑杆（Day 9 的温度）
    - 侧边栏实时 token 用量（Day 7 的 usage 记账）
    - 清空对话按钮
"""

import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()

st.set_page_config(page_title="我的聊天机器人", page_icon="🤖")
st.title("🤖 我的第一个聊天机器人")

if not API_KEY:
    st.error("没找到 DEEPSEEK_API_KEY！请在本文件夹或上级目录建 .env 文件。")
    st.stop()


def 请求(messages: list, temperature: float = 0.7) -> tuple[str, dict]:
    """发请求，返回 (回答文本, usage)。出错时返回友好提示而不是崩溃。"""
    resp = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat", "messages": messages, "temperature": temperature},
        timeout=120,
    )
    if resp.status_code != 200:
        return f"（出错了：{resp.text[:100]}）", {}
    data = resp.json()
    return data["choices"][0]["message"]["content"], data.get("usage", {})


# st.session_state 是 Streamlit 的「全局内存」：页面每次刷新都会重跑脚本，
# 但存进 session_state 的东西会保留。聊天记录就存在这里。
if "消息" not in st.session_state:
    st.session_state.消息 = [{"role": "system", "content": "你是小徐的助手，回答简洁直接。"}]

if "用量" not in st.session_state:
    st.session_state.用量 = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

# ---------- 侧边栏：温度 + token 花费 + 清空对话 ----------
温度 = st.sidebar.slider("温度", 0.0, 1.5, 0.7, 0.1)

st.sidebar.subheader("Token 用量")
st.sidebar.metric("合计", st.session_state.用量["total_tokens"])
st.sidebar.caption(
    f"输入 {st.session_state.用量['prompt_tokens']} / "
    f"输出 {st.session_state.用量['completion_tokens']}"
)

if st.sidebar.button("清空对话"):
    st.session_state.消息 = [st.session_state.消息[0]]   # 只留 system
    st.session_state.用量 = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    st.rerun()

# 把历史消息渲染出来（第一次进来是空的）
for m in st.session_state.消息:
    if m["role"] != "system":                     # 系统提示词不显示给用户看
        with st.chat_message(m["role"]):          # user=右侧，assistant=左侧
            st.markdown(m["content"])

# 输入框：用户发消息
用户输入 = st.chat_input("说点什么…")

if 用户输入:
    with st.chat_message("user"):
        st.markdown(用户输入)
    st.session_state.消息.append({"role": "user", "content": 用户输入})

    with st.chat_message("assistant"):
        with st.spinner("思考中…"):
            回答, 用量 = 请求(st.session_state.消息, 温度)
        st.markdown(回答)
    st.session_state.消息.append({"role": "assistant", "content": 回答})

    # usage 累加（请求出错时 用量 是 {}，.get 兜底为 0）
    for 键 in st.session_state.用量:
        st.session_state.用量[键] += 用量.get(键, 0)
