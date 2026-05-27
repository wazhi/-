import json
import pandas as pd
import plotly.express as px
import streamlit as st


def render_metrics(parsed_info, features, difficulty_result):
    high_risk = 0
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("上传文件数", parsed_info.get("uploaded_count",0))
    c2.metric("解析文本长度", parsed_info.get("total_chars",0))
    c3.metric("Python文件数", parsed_info.get("python_file_count",0))
    c4.metric("关键文件命中", sum(1 for k,v in features.items() if k.startswith("has_") and v))
    c5.metric("复现难度评分", difficulty_result["total_score"])
    c6.metric("高风险项数量", high_risk)


def render_algorithm_results(features, difficulty_result, risks, stage_plan):
    st.subheader("核心算法分析结果")
    st.write(f"**项目类型识别**：{features.get('project_type','未知')}")
    st.write("**缺失项**：", ", ".join(features.get("missing_items",[])) or "无")
    st.json(difficulty_result)
    st.dataframe(pd.DataFrame(risks), use_container_width=True)
    st.dataframe(pd.DataFrame(stage_plan), use_container_width=True)


def render_visualizations(difficulty_result, risks, stage_plan):
    dims = pd.DataFrame({"维度": list(difficulty_result["dimension_scores"].keys()), "分数": list(difficulty_result["dimension_scores"].values())})
    st.plotly_chart(px.bar(dims, x="维度", y="分数", color="分数", title="复现难度维度柱状图"), use_container_width=True)
    risk_df = pd.DataFrame(risks)
    dist = risk_df["风险等级"].value_counts().rename_axis("风险等级").reset_index(name="数量")
    st.plotly_chart(px.pie(dist, names="风险等级", values="数量", title="风险等级分布图"), use_container_width=True)
    stage_df = pd.DataFrame(stage_plan)
    st.plotly_chart(px.bar(stage_df, x="阶段名称", y="建议优先级", title="复现阶段优先级图"), use_container_width=True)
    funnel = pd.DataFrame({"阶段":["文件解析","特征提取","难度评估","风险排序","任务规划","大模型生成","报告导出"],"完成度":[100,95,90,85,80,70,60]})
    st.plotly_chart(px.funnel(funnel, x="完成度", y="阶段", title="复现流程漏斗图"), use_container_width=True)


def render_markdown_plan(plan_text):
    st.subheader("科研复现方案")
    st.markdown(plan_text)


def create_experiment_dataframe(stage_plan):
    return pd.DataFrame(stage_plan)


def export_markdown(plan_text, project_info, difficulty_result, risks):
    payload = "# AI4E-ResearchPilot 导出报告\n\n" + plan_text + "\n\n## 元信息\n```json\n" + json.dumps({"project_info":project_info,"difficulty":difficulty_result,"risks":risks}, ensure_ascii=False, indent=2) + "\n```"
    return payload.encode("utf-8")
