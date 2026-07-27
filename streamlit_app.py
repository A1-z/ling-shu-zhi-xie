import streamlit as st
import random
import json
import re

# ---------- 页面配置 ----------
st.set_page_config(page_title="灵枢智械 · 医疗百科", layout="wide")
st.title("🏥 灵枢智械 · 医疗设备百科全览")
st.caption("输入设备名称，一键获取操作步骤 + 说明书 + 图解说明")

# ---------- 安抚语词库 ----------
comfort_messages = [
    "💙 别紧张，设备是您的帮手，不是对手。",
    "🌼 慢慢来，每一步都做对，健康自然来。",
    "✨ 您学得很快，这个设备马上就是您的好朋友了。",
    "🍀 灵枢守护，愿您操作顺利，身体安康。"
]

# ---------- 加载设备数据 ----------
@st.cache_data
def load_devices():
    with open("devices.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["devices"]

devices = load_devices()

# ---------- 搜索函数 ----------
def search_device(query):
    query_lower = query.strip().lower()
    # 精确匹配
    for device in devices:
        if device["name"].lower() == query_lower or device["id"].lower() == query_lower:
            return device
    # 模糊匹配（关键词）
    for device in devices:
        for kw in device["keywords"]:
            if kw in query_lower:
                return device
    return None

# ---------- UI ----------
col_search, col_btn = st.columns([4, 1])
with col_search:
    query = st.text_input("", placeholder="例如：鱼跃血压计YE660A", label_visibility="collapsed")
with col_btn:
    search_clicked = st.button("🔍 搜索", use_container_width=True)

if search_clicked or query:
    if not query.strip():
        st.warning("📝 请先输入设备名称哦！")
    else:
        device = search_device(query)
        if device is None:
            st.error("😅 小助手暂未收录这款设备，试试搜索：血压计、血糖仪、制氧机、体温计、血氧仪、雾化器、轮椅、助听器、艾灸仪、理疗仪")
        else:
            # 三栏布局
            col1, col2, col3 = st.columns(3)
            
            # 左栏：操作步骤
            with col1:
                st.subheader("📋 操作步骤")
                for step in device["steps"]:
                    st.markdown(f"**{step['step']}. {step['icon']} {step['action']}**")
                    st.write(step["detail"])
                    st.caption(f"💙 {step['tip']}")
                    st.divider()
                st.info(f"✨ {random.choice(comfort_messages)}")
            
            # 中栏：PDF（占位）
            with col2:
                st.subheader("📄 设备说明书")
                if device.get("pdf_url"):
                    st.markdown(f'<iframe src="{device["pdf_url"]}" width="100%" height="400" style="border:none;"></iframe>', unsafe_allow_html=True)
                    st.download_button("⬇️ 下载说明书", data=None, file_name="说明书.pdf", disabled=True)
                else:
                    st.info("📌 说明书PDF即将上线，敬请期待。")
            
            # 右栏：图文解释 + FAQ
            with col3:
                st.subheader("🧠 图文解释")
                if device.get("image_url"):
                    st.image(device["image_url"], caption="操作示意图")
                else:
                    st.info("📌 图解说明即将上线，敬请期待。")
                st.subheader("❓ 常见问题")
                for faq in device.get("faq", []):
                    with st.expander(f"Q: {faq['q']}"):
                        st.write(f"A: {faq['a']}")
            
            # 底部健康小贴士
            st.divider()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f4f8, #d1ecf1); padding: 20px; border-radius: 15px; text-align: center;">
                <h4 style="color: #1a3a5c;">🌿 健康小贴士</h4>
                <p style="font-size: 18px;">{random.choice(comfort_messages)}</p >
                <p style="font-size: 14px; color: #5a6c7d;">—— 灵枢智械 · 让健康更简单</p >
            </div>
            """, unsafe_allow_html=True)
