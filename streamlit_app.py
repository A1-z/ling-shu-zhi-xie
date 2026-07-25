import gradio as gr
import random

# ---------- 暖心安抚语词库（科艺融合亮点）----------
comfort_messages = [
    "💙 别急，机器冷冰冰，但灵枢智械在陪着您。",
    "🌼 慢慢来，操作设备不熟悉很正常，您做得很好。",
    "✨ 已为您找到相关信息，请放心操作。",
    "🍀 灵枢守护，祝您一切顺利！"
]


# ---------- 核心查询函数（现在是模拟版，明天改）----------
def query_pdf(file, question):
    # 如果用户没上传文件，提醒他
    if file is None:
        return "⚠️ 请先上传一份医疗设备PDF说明书哦！"

    # 如果用户没打字，提醒他
    if not question or question.strip() == "":
        return "📝 请在对话框中输入您的问题，例如：怎么开机？"

    # ---------- 模拟回复（今晚先把界面跑通）----------
    # 注意：这里没写真正读取PDF的逻辑，先返回占位回复，
    # 目的就是让你的网页立刻亮起来，不卡在复杂代码上！
    reply = f"✅ 已收到您关于《{file.name}》的问题：\n“{question}”\n\n📖 灵枢正在检索手册内容...(此处明天将接入真实PDF读取功能)"

    # 随机加上一句安抚语
    comfort = random.choice(comfort_messages)
    return reply + "\n\n" + comfort


# ---------- 制作漂亮的蓝白医疗风界面 ----------
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="sky"),
               title="灵枢智械 · 医疗设备智能助手") as demo:
    gr.Markdown("""
    # 🏥 灵枢智械
    ### 医疗设备智能说明书助手 · 让冰冷参数变温暖关怀
    """)

    # 文件上传区域
    file_input = gr.File(label="📎 上传医疗设备说明书 (PDF格式)", file_types=[".pdf"])

    # 问题输入框
    question_input = gr.Textbox(label="💬 输入您的问题", placeholder="例如：这个血压计的袖带怎么绑？", lines=2)

    # 回答输出框
    answer_output = gr.Textbox(label="🧠 AI 智能回复", lines=6, interactive=False)

    # 按钮区域（并列排放）
    with gr.Row():
        submit_btn = gr.Button("🔍 提交问题", variant="primary")
        clear_btn = gr.Button("🗑️ 清空记录", variant="secondary")

    # 设置按钮点击事件
    submit_btn.click(fn=query_pdf, inputs=[file_input, question_input], outputs=answer_output)
    clear_btn.click(fn=lambda: ("", "", None), inputs=[], outputs=[question_input, answer_output, file_input])

# ---------- 启动应用 ----------
if __name__ == "__main__":
    demo.launch()
    