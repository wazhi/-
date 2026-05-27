from dotenv import load_dotenv
import os
import streamlit as st

from src.file_parser import parse_uploaded_files
from src.core_algorithm import extract_project_features, calculate_reproduction_difficulty, rank_reproduction_risks, generate_stage_plan, build_algorithm_summary
from src.prompts import build_reproduction_prompt
from src.llm_client import generate_with_llm
from src.local_generator import generate_local_reproduction_plan
from src.render import render_metrics, render_algorithm_results, render_visualizations, render_markdown_plan, create_experiment_dataframe, export_markdown

load_dotenv()
st.set_page_config(page_title="AI科研复现方案生成器", layout="wide")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#0f1226,#1a1f46,#171530);color:#e6ecff}.block-container{padding-top:1.2rem}.stButton button{background:linear-gradient(90deg,#5b8cff,#8f6bff);color:white;border-radius:12px}.card{background:rgba(255,255,255,.04);padding:14px;border-radius:12px;border:1px solid rgba(120,140,255,.25)}</style>""", unsafe_allow_html=True)

st.title("AI4E-ResearchPilot")
st.caption("面向工程人工智能课程的 AI科研复现助手平台")
st.write("通过核心算法 + 大模型 API 生成科研复现方案")

with st.sidebar:
    st.header("大模型 API 配置")
    api_key_in = st.text_input("API Key", type="password")
    base_url = st.text_input("Base URL", value=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    model = st.text_input("Model Name", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
    api_key = api_key_in.strip() or os.getenv("OPENAI_API_KEY", "")
    mode = "大模型增强模式" if api_key else "本地演示模式"
    st.info(f"当前模式：{mode}")

    st.header("项目信息输入")
    defaults = {
        "复现项目名称":"基于深度学习的电池寿命预测模型复现","研究方向":"工程人工智能 / 电池寿命预测","论文标题":"Battery Life Prediction Based on Deep Learning",
        "复现目标":"理解论文方法，完成模型训练，并形成实验报告","已有环境":"Windows + Anaconda + Python","已有数据集":"BatteryLife 数据集",
        "期望实验结果":"得到模型预测误差、训练曲线和实验分析","当前困难":"不清楚数据预处理流程和训练入口"
    }
    project_info = {k: st.text_area(k, v, height=80) for k,v in defaults.items()}
    uploaded_files = st.file_uploader("上传材料", type=["pdf","docx","txt","md","py","zip","log","csv","xlsx"], accept_multiple_files=True)
    run = st.button("生成科研复现方案", use_container_width=True)

if run:
    parsed = parse_uploaded_files(uploaded_files)
    ext = extract_project_features(parsed, project_info)
    features = ext["features"] | {"project_type": ext["project_type"], "missing_items": ext["missing_items"], "detected_keywords": ext["detected_keywords"]}
    difficulty = calculate_reproduction_difficulty(features)
    risks = rank_reproduction_risks(features, difficulty)
    stage_plan = generate_stage_plan(features, risks)
    algorithm_summary = build_algorithm_summary(features, difficulty, risks, stage_plan)

    render_metrics(parsed, features, difficulty)
    render_algorithm_results(features, difficulty, risks, stage_plan)
    render_visualizations(difficulty, risks, stage_plan)

    extracted_text = "\n\n".join(parsed.get("texts", []))
    code_summary = parsed.get("zip_tree", "") + "\n" + "\n".join(parsed.get("code_files", []))
    prompt = build_reproduction_prompt(project_info, extracted_text, code_summary, algorithm_summary)
    plan_text = ""
    if api_key:
        llm_text = generate_with_llm(prompt, api_key, base_url, model, temperature)
        if llm_text.startswith("[LLM调用失败]"):
            st.error(llm_text + "，已自动回退到本地演示模式。")
            plan_text = generate_local_reproduction_plan(project_info, extracted_text, code_summary, {"difficulty":difficulty,"risks":risks,"stage_plan":stage_plan})
        else:
            plan_text = llm_text
    else:
        plan_text = generate_local_reproduction_plan(project_info, extracted_text, code_summary, {"difficulty":difficulty,"risks":risks,"stage_plan":stage_plan})

    render_markdown_plan(plan_text)
    st.subheader("实验计划表")
    st.dataframe(create_experiment_dataframe(stage_plan), use_container_width=True)
    st.download_button("导出 Markdown 报告素材", data=export_markdown(plan_text, project_info, difficulty, risks), file_name="AI4E_reproduction_plan.md", mime="text/markdown")
