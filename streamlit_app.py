import streamlit as st
import random
import json
import re

# ---------- 页面配置 ----------
st.set_page_config(
    page_title="灵枢智械 · 医疗百科",
    page_icon="🏥",
    layout="wide"
)

# ---------- 自定义CSS（医疗蓝主题 + 适老化） ----------
st.markdown("""
<style>
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #f0f7fc 0%, #e8f0f8 100%);
    }
    /* 标题样式 */
    h1 {
        color: #1a5276 !important;
        font-size: 48px !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
    }
    /* 卡片样式 - 操作步骤 */
    .step-card {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 10px 0;
        box-shadow: 0 2px 12px rgba(26, 82, 118, 0.10);
        border-left: 5px solid #2e86c1;
        transition: transform 0.2s;
    }
    .step-card:hover {
        transform: translateX(6px);
    }
    .step-card .step-icon {
        font-size: 28px;
        margin-right: 10px;
    }
    .step-card .step-action {
        font-size: 20px;
        font-weight: 600;
        color: #1a5276;
    }
    .step-card .step-detail {
        font-size: 17px;
        color: #2c3e50;
        margin: 6px 0 4px 0;
        line-height: 1.6;
    }
    .step-card .step-tip {
        color: #2e86c1;
        font-size: 15px;
        padding-left: 8px;
        background: #eaf4fa;
        border-radius: 8px;
        padding: 6px 14px;
        display: inline-block;
        margin-top: 4px;
    }
    /* 搜索框放大（适老化） */
    .stTextInput input {
        font-size: 22px !important;
        padding: 16px 20px !important;
        border-radius: 30px !important;
        border: 2px solid #2e86c1 !important;
        background: white !important;
    }
    .stTextInput input:focus {
        box-shadow: 0 0 0 3px rgba(46, 134, 193, 0.3) !important;
    }
    /* 大按钮 */
    .stButton button {
        background: linear-gradient(135deg, #1a5276, #2e86c1) !important;
        color: white !important;
        font-size: 22px !important;
        padding: 14px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(26, 82, 118, 0.3) !important;
        transition: all 0.3s !important;
        width: 100% !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(26, 82, 118, 0.4) !important;
    }
    /* 栏目标题 */
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #1a5276;
        border-bottom: 3px solid #2e86c1;
        padding-bottom: 10px;
        margin-bottom: 18px;
    }
    /* 健康小贴士画报 */
    .health-poster {
        background: linear-gradient(135deg, #eaf4fa, #d4e6f1);
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #aed6f1;
        margin-top: 20px;
    }
    .health-poster h4 {
        color: #1a5276;
        font-size: 24px;
        margin-bottom: 8px;
    }
    .health-poster p {
        font-size: 20px;
        color: #2c3e50;
    }
    /* FAQ折叠样式 */
    .stExpander {
        border-radius: 12px !important;
        border: 1px solid #d4e6f1 !important;
        margin: 6px 0 !important;
    }
    .stExpander summary {
        font-size: 17px !important;
        font-weight: 500 !important;
        color: #1a5276 !important;
    }
    /* 错误提示美化 */
    .stAlert {
        border-radius: 16px !important;
        font-size: 18px !important;
        padding: 16px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- 标题 ----------
st.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <h1>🏥 灵枢智械 · 医疗百科</h1>
    <p style="font-size: 20px; color: #2c3e50; margin-top: -10px;">
        输入设备名称 · 一键获取操作步骤 + 安抚语 + 常见问题
    </p >
    <p style="font-size: 16px; color: #5d6d7e;">
        👴 专为长辈设计的健康助手 · 让冰冷参数变温暖关怀
    </p >
</div>
""", unsafe_allow_html=True)

# ---------- 安抚语词库（扩充） ----------
comfort_messages = [
    "💙 别紧张，设备是您的帮手，不是对手。慢慢来，一定能学会！",
    "🌼 您做得很好！每一步都正确，健康自然来。",
    "✨ 真棒！这个设备马上就是您的好朋友了。",
    "🍀 灵枢守护，愿您操作顺利，身体安康。",
    "💪 您学得很快！多试几次就熟练了。",
    "🌟 每一步都很清晰，您已经掌握了要点！",
    "❤️ 别急，机器冷冰冰，但灵枢智械在陪着您。",
    "🌺 您比想象中更厉害！操作很简单对不对？"
]

# ---------- 同义词映射（提升搜索命中率） ----------
synonyms = {
    "血压计": ["量血压", "测血压", "血压", "高压", "低压"],
    "血糖仪": ["测血糖", "量血糖", "血糖", "扎手指", "采血"],
    "制氧机": ["吸氧", "氧气", "氧疗"],
    "体温计": ["测温", "量体温", "发烧", "耳温枪"],
    "血氧仪": ["血氧", "夹手指", "脉搏", "氧饱和度"],
    "雾化器": ["雾化", "咳嗽", "哮喘", "化痰"],
    "轮椅": ["代步", "老人车", "行动不便"],
    "助听器": ["听力", "耳背", "老人听力"],
    "艾灸仪": ["艾灸", "温灸", "灸"],
    "理疗仪": ["理疗", "低频", "按摩", "颈椎", "腰椎"]
}


# ---------- 加载设备数据 ----------
@st.cache_data
def load_devices():
    try:
        with open("devices.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["devices"]
    except FileNotFoundError:
        st.error("❌ 设备数据文件 devices.json 未找到，请检查文件是否存在。")
        return []
    except json.JSONDecodeError:
        st.error("❌ devices.json 格式错误，请检查JSON语法是否正确。")
        return []


devices = load_devices()


# ---------- 搜索函数（优化版：同义词+模糊匹配） ----------
def search_device(query):
    if not query or not query.strip():
        return None, None

    query_lower = query.strip().lower()

    # 1. 精确匹配设备名称或ID
    for device in devices:
        if device["name"].lower() == query_lower or device["id"].lower() == query_lower:
            return device, "exact"

    # 2. 关键词匹配（设备自带关键词）
    for device in devices:
        for kw in device["keywords"]:
            if kw in query_lower:
                return device, "keyword"

    # 3. 同义词匹配（扩展搜索范围）
    for device in devices:
        device_name_lower = device["name"].lower()
        for category, syn_list in synonyms.items():
            # 检查用户输入是否包含同义词
            for syn in syn_list:
                if syn in query_lower:
                    # 检查该设备是否属于这个分类
                    if category in device_name_lower or category in device.get("category", ""):
                        return device, "synonym"

    # 4. 设备名包含匹配（更宽松）
    for device in devices:
        device_name_lower = device["name"].lower()
        # 提取用户输入中的核心词
        core_words = ["血压", "血糖", "制氧", "体温", "血氧", "雾化", "轮椅", "助听", "艾灸", "理疗", "按摩", "低频"]
        for word in core_words:
            if word in query_lower and word in device_name_lower:
                return device, "fuzzy"

    # 5. 完全没匹配到 → 推荐相似设备
    return None, None


def get_recommendation(query):
    """获取推荐设备列表"""
    query_lower = query.strip().lower()
    recommendations = []
    for device in devices:
        name = device["name"].lower()
        # 计算简单匹配度
        score = 0
        for char in query_lower:
            if char in name:
                score += 1
        if score >= 2:  # 至少有2个字符匹配
            recommendations.append(device["name"])
    return recommendations[:3]  # 最多推荐3个


# ---------- 界面布局 ----------
col_search, col_btn = st.columns([4, 1])
with col_search:
    query = st.text_input(
        "",
        placeholder="🔍 输入设备名称，例如：血压计、血糖仪、助听器...",
        label_visibility="collapsed"
    )
with col_btn:
    search_clicked = st.button("🔍 搜索", use_container_width=True)

# ---------- 处理搜索 ----------
if search_clicked or query:
    if not query.strip():
        st.warning("📝 请先输入设备名称哦！")
    else:
        device, match_type = search_device(query)

        if device is None:
            # 推荐相似设备
            recs = get_recommendation(query)
            if recs:
                st.error(f"😅 小助手暂未收录「{query}」，您是不是想找：{'、'.join(recs)}？")
            else:
                all_names = "、".join([d["name"].split()[0] for d in devices])
                st.error(f"😅 小助手暂未收录这款设备，试试搜索：{all_names}")
        else:
            # ---------- 显示搜索结果 ----------
            # 匹配类型标签
            match_labels = {
                "exact": "✅ 精确匹配",
                "keyword": "📌 关键词匹配",
                "synonym": "🔗 同义词匹配",
                "fuzzy": "🔄 相关推荐"
            }
            st.caption(match_labels.get(match_type, ""))

            # ---------- 三栏布局 ----------
            col1, col2, col3 = st.columns(3)

            # 左栏：操作步骤
            with col1:
                st.markdown('<p class="section-title">📋 操作步骤</p >', unsafe_allow_html=True)
                for step in device["steps"]:
                    st.markdown(f"""
                    <div class="step-card">
                        <span class="step-icon">{step['icon']}</span>
                        <span class="step-action">{step['step']}. {step['action']}</span>
                        <div class="step-detail">{step['detail']}</div>
                        <div class="step-tip">💙 {step['tip']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # 随机安抚语
                st.markdown(f"""
                <div style="background: #eaf4fa; padding: 16px; border-radius: 14px; margin-top: 16px; text-align: center; font-size: 18px;">
                    {random.choice(comfort_messages)}
                </div>
                """, unsafe_allow_html=True)

            # 中栏：PDF说明书
            with col2:
                st.markdown('<p class="section-title">📄 设备说明书</p >', unsafe_allow_html=True)
                pdf_url = device.get("pdf_url", "")
                if pdf_url and pdf_url.strip():
                    try:
                        st.pdf(pdf_url, height=450)
                    except Exception:
                        st.warning("⚠️ 说明书加载失败，请稍后再试或点击下方下载。")
                        st.link_button("📥 点击下载说明书", pdf_url)
                else:
                    st.info("📌 说明书PDF即将上线，敬请期待。\n\n如需帮助，请咨询客服或查看设备包装内的纸质说明书。")

            # 右栏：图文解释 + FAQ
            with col3:
                st.markdown('<p class="section-title">🧠 图文解释</p >', unsafe_allow_html=True)
                image_url = device.get("image_url", "")
                if image_url and image_url.strip():
                    try:
                        st.image(image_url, caption=f"{device['name']} 操作示意图")
                    except Exception:
                        st.warning("⚠️ 图片加载失败，请稍后再试。")
                else:
                    st.info("📌 图解说明即将上线，敬请期待。\n\n操作步骤已用文字清晰描述，请参考左侧步骤。")

                # FAQ
                st.markdown('<p class="section-title" style="margin-top: 20px;">❓ 常见问题</p >',
                            unsafe_allow_html=True)
                for faq in device.get("faq", []):
                    with st.expander(f"Q: {faq['q']}"):
                        st.write(f"A: {faq['a']}")

            # ---------- 底部健康小贴士画报 ----------
            st.divider()
            st.markdown(f"""
            <div class="health-poster">
                <h4>🌿 健康小贴士</h4>
                <p>{random.choice(comfort_messages)}</p >
                <p style="font-size: 16px; color: #5d6d7e; margin-top: 8px;">
                    —— 灵枢智械 · 让健康更简单 ——
                </p >
                <p style="font-size: 14px; color: #7f8c8d; margin-top: 4px;">
                    💡 记住：健康是1，其他都是后面的0
                </p >
            </div>
            """, unsafe_allow_html=True)

# ---------- 底部提示 ----------
st.divider()
st.caption("🏥 灵枢智械 · 支持10种家用医疗设备 · 持续更新中")
