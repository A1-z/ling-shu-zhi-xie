import streamlit as st
import random

# 安抚语词库
comfort = [
    "💙 别急，机器冷冰冰，但灵枢智械在陪着您。",
    "🌼 慢慢来，您做得很好。",
    "✨ 已为您找到相关信息。",
    "🍀 灵枢守护，祝您顺利！"
]

st.set_page_config(page_title="灵枢智械", layout="centered")
st.title("🏥 灵枢智械 · 医疗设备助手")
st.caption("让冰冷参数变温暖关怀")

file = st.file_uploader("📎 上传医疗设备PDF说明书", type=["pdf"])
question = st.text_input("💬 输入您的问题", placeholder="例如：怎么开机？")

if st.button("🔍 提交问题"):
    if file is None:
        st.error("请先上传PDF文件")
    elif not question:
        st.error("请输入问题")
    else:
        reply = f"✅ 收到《{file.name}》的问题：{question}\n\n📖 灵枢正在检索..."
        st.success(reply + "\n\n" + random.choice(comfort))
