# AI4E-ResearchPilot 文本归档

该文档用于在不支持二进制文件传输的环境中，以纯文本/Markdown方式共享项目源码。

## `.env.example`

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## `README.md`

```text
# AI4E-ResearchPilot：AI科研复现助手平台

## 项目简介
聚焦“AI科研复现方案生成器”：上传论文/说明/代码包/日志后，系统执行**难度评估+风险排序+阶段规划**，再结合大模型生成可执行复现方案。

## 项目背景与系统需求分析
面向工程类研究生、课程大作业学生、指导教师，解决论文理解难、训练入口不清、环境依赖复杂、排错无路径、报告难整理等问题。

## 核心功能
1. 材料上传与解析（PDF/DOCX/TXT/MD/PY/ZIP/LOG/CSV/XLSX）
2. 科研复现难度评估与任务规划算法
3. OpenAI-compatible 大模型增强生成
4. 本地演示模式回退
5. Plotly 可视化 + Markdown 导出

## 技术栈
Python、Streamlit、pandas、plotly、pypdf、python-docx、openai、python-dotenv、pytest。

## 大模型 API 配置
- 侧边栏输入：API Key / Base URL / Model / Temperature
- `.env` 兜底：OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL
- 有 Key：大模型增强模式；无 Key：本地演示模式

## 安装运行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 使用流程
上传材料 -> 文件解析 -> 特征提取 -> 难度评估 -> 风险排序 -> 阶段规划 -> 大模型/本地生成 -> 可视化与导出。

## 核心算法说明
DifficultyScore =
0.25 * ModelComplexity +
0.20 * DataComplexity +
0.20 * CodeCompletenessRisk +
0.15 * EnvironmentRisk +
0.10 * ExperimentComplexity +
0.10 * ReportComplexity

## 大模型功能说明
基于算法总结构造 Prompt，要求结构化中文 Markdown 输出，直接可用于实验报告。

## 可视化说明
包含难度维度柱状图、风险等级分布图、阶段优先级图、复现流程漏斗图。

## 系统亮点
- 不是聊天机器人，也不是普通RAG
- 核心算法结果直接影响最终方案
- 支持课程答辩所需可视化与报告素材导出

## 测试方式
```bash
python -m py_compile app.py src/*.py tests/*.py
pytest -q
```

## 后续优化方向
自动日志解析增强、项目结构图谱、实验版本追踪、模型对比模板、Agent协同排错。
```

## `app.py`

```text
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
```

## `data/sample_project_info.json`

```text
{
  "复现项目名称": "基于深度学习的电池寿命预测模型复现",
  "研究方向": "工程人工智能 / 电池寿命预测",
  "论文标题": "Battery Life Prediction Based on Deep Learning",
  "复现目标": "理解论文方法，完成模型训练，并形成实验报告",
  "已有环境": "Windows + Anaconda + Python",
  "已有数据集": "BatteryLife 数据集",
  "期望实验结果": "得到模型预测误差、训练曲线和实验分析",
  "当前困难": "不清楚数据预处理流程和训练入口"
}
```

## `docs/report_outline.md`

```text
# 实验报告大纲
1. 项目背景与需求分析：说明工程AI课程场景和复现痛点。
2. 调研对象与痛点分析：研究生、课程学生、教师三类用户。
3. 系统总体设计：单页平台与模块协同关系。
4. 系统核心功能设计：上传解析、算法分析、方案生成。
5. 科研复现难度评估算法设计：特征、评分、风险、阶段规划。
6. 大模型辅助科研复现模块设计：Prompt与回退机制。
7. 系统实现过程：关键代码实现与工程组织。
8. 应用成果展示：示例项目分析与输出结果。
9. 数据可视化设计：难度、风险、优先级、流程漏斗。
10. 系统测试：单元测试与运行验证。
11. 总结与优化展望：可扩展能力与未来路线。
```

## `docs/system_design.md`

```text
# 系统设计文档
## 1. 系统需求分析
围绕“科研复现方案生成”单核心能力，提供解析-评估-规划-生成闭环。
## 2. 用户角色
研究生、课程学生、教师。
## 3. 业务流程
上传材料 -> 解析 -> 特征提取 -> 难度评分 -> 风险排序 -> 阶段规划 -> LLM生成 -> 导出。
## 4. 功能架构
app.py(编排) + src/file_parser.py + src/core_algorithm.py + src/prompts.py + src/llm_client.py + src/local_generator.py + src/render.py。
## 5. 核心算法模块设计
- 算法输入：parsed_files, project_info
- 算法输出：features/difficulty/risks/stage_plan/summary
- 特征提取逻辑：关键文件、关键词、日志、指标、环境等布尔与计数特征
- 评分公式：DifficultyScore = 0.25*ModelComplexity + 0.20*DataComplexity + 0.20*CodeCompletenessRisk + 0.15*EnvironmentRisk + 0.10*ExperimentComplexity + 0.10*ReportComplexity
- 风险排序逻辑：按风险分数降序映射低中高
- 阶段任务规划逻辑：8阶段，依据缺失项/风险动态改写操作建议
- LLM利用算法结果：将算法摘要注入Prompt，约束输出结构与优先级
## 6. AI模块技术路线
OpenAI-compatible Chat Completions + 失败回退本地生成。
## 7. 数据流设计
UI输入与文件流进入解析器，结构化结果进入算法，算法结果传渲染器与生成器。
## 8. 大模型调用流程
读取页面/API环境变量 -> 构造Prompt -> 调用模型 -> 失败回退。
## 9. 可视化设计
Plotly：柱状图、饼图、优先级图、漏斗图。
## 10. 安全与隐私考虑
本地运行、无登录、无数据库；仅在用户提供API Key时发起外部调用。
## 11. 可扩展方向
多模型对比、自动参数搜索、报告模板扩展、日志异常检测。
```

## `requirements.txt`

```text
streamlit>=1.36.0
pandas>=2.2.0
plotly>=5.22.0
pypdf>=4.2.0
python-docx>=1.1.2
openai>=1.40.0
python-dotenv>=1.0.1
pytest>=8.2.0
openpyxl>=3.1.5
```

## `sample_docs/sample_paper_summary.txt`

```text
This paper studies battery capacity degradation across cycle trajectories and predicts SOH/RUL with an LSTM model. We use capacity and cycle features, optimize MAE and RMSE, and report robust performance under domain shift.
```

## `sample_docs/sample_readme.md`

```text
# Sample Project
- train.py: 模型训练入口
- dataset.py: 数据加载与切分
- model.py: 模型结构定义
- requirements.txt: 环境依赖
```

## `sample_docs/sample_training_log.log`

```text
epoch=1 loss=0.221 val_loss=0.245 MAE=0.082 RMSE=0.114
epoch=2 loss=0.180 val_loss=0.210 MAE=0.075 RMSE=0.105
epoch=3 loss=0.151 val_loss=0.195 MAE=0.071 RMSE=0.099
```

## `scripts/export_text_bundle.py`

```text
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "project_text_bundle.md"

INCLUDE_SUFFIX = {".py", ".md", ".txt", ".log", ".json", ".example", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".csv"}
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}
EXCLUDE_FILES = {"project_text_bundle.md"}


def should_include(path: Path) -> bool:
    if any(p in EXCLUDE_DIRS for p in path.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in INCLUDE_SUFFIX:
        return True
    if path.name in {"requirements.txt", ".env.example"}:
        return True
    return False


def build_bundle() -> str:
    lines = [
        "# AI4E-ResearchPilot 文本归档",
        "",
        "该文档用于在不支持二进制文件传输的环境中，以纯文本/Markdown方式共享项目源码。",
        "",
    ]

    files = [p for p in ROOT.rglob("*") if p.is_file() and should_include(p)]
    files.sort(key=lambda x: x.as_posix())

    for fp in files:
        rel = fp.relative_to(ROOT).as_posix()
        try:
            content = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = fp.read_text(encoding="latin-1", errors="replace")

        lines.extend([
            f"## `{rel}`",
            "",
            "```text",
            content.rstrip("\n"),
            "```",
            "",
        ])

    return "\n".join(lines)


if __name__ == "__main__":
    OUT.write_text(build_bundle(), encoding="utf-8")
    print(f"written: {OUT}")
```

## `src/__init__.py`

```text

```

## `src/core_algorithm.py`

```text
from __future__ import annotations

from typing import Any


def _contains(text: str, words: list[str]) -> bool:
    t = text.lower()
    return any(w.lower() in t for w in words)


def extract_project_features(parsed_files, project_info) -> dict[str, Any]:
    texts = "\n".join(parsed_files.get("texts", [])) + "\n" + "\n".join(str(v) for v in project_info.values())
    code_files = [c.lower() for c in parsed_files.get("code_files", [])]
    zip_tree = parsed_files.get("zip_tree", "").lower()

    def has_file(n):
        return any(n in c for c in code_files) or n in zip_tree

    features = {
        "has_paper_text": parsed_files.get("has_pdf", False) or _contains(texts, ["abstract", "论文", "introduction"]),
        "has_docx": parsed_files.get("has_docx", False),
        "has_zip": parsed_files.get("has_zip", False),
        "has_requirements": has_file("requirements.txt"),
        "has_train_py": has_file("train.py"),
        "has_main_py": has_file("main.py"),
        "has_config_py": has_file("config.py"),
        "has_model_py": has_file("model.py"),
        "has_dataset_py": has_file("dataset.py") or has_file("data.py"),
        "has_eval_py": has_file("evaluate.py") or has_file("test.py"),
        "has_training_log": parsed_files.get("has_log", False) or _contains(texts, ["epoch", "val_loss", "loss"]),
        "python_file_count": parsed_files.get("python_file_count", 0),
        "total_chars": parsed_files.get("total_chars", 0),
        "mention_deep_learning": _contains(texts, ["deep learning", "深度学习", "pytorch", "tensorflow"]),
        "mention_ml": _contains(texts, ["machine learning", "机器学习", "randomforest", "svm", "xgboost"]),
        "mention_cnn": _contains(texts, ["cnn", "卷积神经网络"]),
        "mention_rnn": _contains(texts, ["rnn", "循环神经网络"]),
        "mention_lstm": _contains(texts, ["lstm"]),
        "mention_transformer": _contains(texts, ["transformer"]),
        "mention_tree_models": _contains(texts, ["randomforest", "svm", "xgboost"]),
        "mention_gpu": _contains(texts, ["gpu"]),
        "mention_cuda": _contains(texts, ["cuda"]),
        "has_dataset_desc": _contains(texts, ["dataset", "数据集", "样本", "capacity", "cycle"]),
        "has_metrics_desc": _contains(texts, ["metric", "评价指标", "mae", "rmse", "f1", "auc", "accuracy"]),
        "has_training_metrics": _contains(texts, ["loss", "accuracy", "mae", "rmse", "f1", "auc"]),
        "has_env_desc": _contains(texts, ["requirements", "python", "cuda", "pytorch", "tensorflow", "anaconda"]),
        "has_result_desc": _contains(texts, ["result", "实验结果", "ablation", "对比实验"]),
        "has_report_material": _contains(texts, ["report", "实验报告", "结论", "分析"]),
    }
    kws=[k for k,v in features.items() if isinstance(v,bool) and v]
    missing=[k for k,v in features.items() if isinstance(v,bool) and not v and k.startswith("has_")]

    if _contains(texts,["battery","电池","soh","rul","capacity","cycle"]): pt="电池寿命预测"
    elif _contains(texts,["lane","车道线","segmentation"]): pt="车道线检测"
    elif _contains(texts,["image classification","图像分类"]): pt="图像分类"
    elif _contains(texts,["time series","时间序列"]): pt="时间序列预测"
    elif _contains(texts,["nlp","自然语言处理","bert"]): pt="自然语言处理"
    elif features["mention_ml"]: pt="通用机器学习"
    elif features["mention_deep_learning"]: pt="通用深度学习"
    else: pt="未知工程AI项目"

    return {"features":features,"detected_keywords":kws,"missing_items":missing,"project_type":pt}


def calculate_reproduction_difficulty(features):
    model = 30 + 15*features.get("mention_deep_learning",False)+20*features.get("mention_transformer",False)+10*features.get("mention_lstm",False)+8*features.get("mention_cnn",False)
    data = 45 + 15*(not features.get("has_dataset_desc",False)) + 10*(not features.get("has_dataset_py",False)) + 8*features.get("has_training_log",False)
    missing_count = sum(not features.get(k, False) for k in ["has_train_py","has_main_py","has_requirements","has_config_py","has_model_py","has_dataset_py"])
    code = min(100, 25 + missing_count * 12)
    env = 35 + 20*features.get("mention_cuda",False)+10*features.get("mention_gpu",False)+20*(not features.get("has_requirements",False))
    exp = 40 + 15*features.get("mention_deep_learning",False)+10*features.get("has_training_metrics",False)+10*features.get("has_metrics_desc",False)
    report = 35 + 20*(not features.get("has_result_desc",False))+15*(not features.get("has_report_material",False))+10*(not features.get("has_metrics_desc",False))
    dims = {"模型复杂度":min(100,model),"数据复杂度":min(100,data),"代码完整性风险":min(100,code),"环境配置风险":min(100,env),"实验复杂度":min(100,exp),"报告整理复杂度":min(100,report)}
    total = round(0.25*dims["模型复杂度"]+0.20*dims["数据复杂度"]+0.20*dims["代码完整性风险"]+0.15*dims["环境配置风险"]+0.10*dims["实验复杂度"]+0.10*dims["报告整理复杂度"],1)
    level = "低难度" if total <40 else "中等难度" if total <70 else "高难度"
    reasons=[]
    if features.get("mention_transformer") or features.get("mention_deep_learning"): reasons.append("检测到 Transformer 或深度学习关键词，模型复杂度较高")
    if not features.get("has_requirements"): reasons.append("缺少 requirements.txt，环境复现风险较高")
    if not features.get("has_train_py") and not features.get("has_main_py"): reasons.append("训练入口不明确，代码理解成本较高")
    return {"total_score":total,"level":level,"dimension_scores":dims,"reasons":reasons}


def rank_reproduction_risks(features, difficulty_result):
    risks=[]
    def add(name,score,reason,advice):
        lvl="低" if score<40 else "中" if score<70 else "高"
        risks.append({"风险名称":name,"风险等级":lvl,"风险分数":int(score),"风险原因":reason,"解决建议":advice})
    add("环境依赖风险", 85 if (features.get("mention_cuda") and not features.get("has_requirements")) else 60 if not features.get("has_requirements") else 35,
        "项目涉及 CUDA，但依赖说明不足" if features.get("mention_cuda") else "依赖清单完整性一般", "整理 Python/框架/CUDA 版本并冻结依赖。")
    add("数据缺失风险", 80 if not features.get("has_dataset_desc") else 45, "缺少清晰的数据集说明" if not features.get("has_dataset_desc") else "数据集说明较完整", "确认下载链接、字段定义、划分策略与预处理规范。")
    add("代码入口不清晰风险", 82 if (not features.get("has_train_py") and not features.get("has_main_py")) else 35, "未识别 train.py/main.py" if (not features.get("has_train_py") and not features.get("has_main_py")) else "入口文件可识别", "梳理调用栈并补充README中的运行命令。")
    add("模型复杂度风险", difficulty_result["dimension_scores"]["模型复杂度"], "深度模型参数较多" if features.get("mention_deep_learning") else "模型复杂度中等", "先做小规模实验，再逐步调参。")
    add("训练资源不足风险", 75 if (features.get("mention_gpu") or features.get("mention_cuda")) else 40, "可能需要GPU资源" if (features.get("mention_gpu") or features.get("mention_cuda")) else "CPU可运行", "设置小batch、减少epoch并开启断点续训。")
    add("结果复现偏差风险", 72 if not features.get("has_training_log") else 50, "缺少历史训练日志对照" if not features.get("has_training_log") else "可参考现有训练日志", "固定随机种子并记录关键超参数。")
    add("报告撰写风险", 70 if not features.get("has_report_material") else 45, "报告素材不足" if not features.get("has_report_material") else "已有部分报告素材", "按实验模板记录过程、结果图和结论。")
    return sorted(risks, key=lambda x: x["风险分数"], reverse=True)


def generate_stage_plan(features, risks):
    top = risks[0]["风险名称"] if risks else "环境依赖风险"
    env_step = "创建虚拟环境并安装 requirements.txt，校验 GPU/CUDA 可用性。" if features.get("has_requirements") else "手动整理依赖（Python/框架/CUDA版本）并生成 requirements.txt。"
    code_step = "定位 train.py/main.py 作为训练入口并梳理调用关系。" if (features.get("has_train_py") or features.get("has_main_py")) else "通过 README、model.py、dataset.py 反向定位训练入口。"
    data_step = "核对数据格式、划分与标注规则。" if features.get("has_dataset_desc") else "先补充数据集来源、字段含义、样本数量与划分规则。"
    analysis_step = "结合日志分析 loss/accuracy/MAE/RMSE 变化并解释异常。" if features.get("has_training_log") else "建立实验记录模板，补充训练曲线与指标表格。"
    names=[("环境配置","搭建可运行环境",env_step,"可运行环境与依赖清单","环境依赖风险"),
    ("数据准备","明确数据资产",data_step,"可用数据集与数据说明","数据缺失风险"),
    ("代码结构理解","明确代码执行路径",code_step,"训练入口与模块关系图","代码入口不清晰风险"),
    ("数据预处理","完成可复用预处理流水线","实现清洗、标准化、切分并固化脚本。","预处理脚本与样本检查报告","数据缺失风险"),
    ("模型训练","获得可复现实验结果","设置超参数并启动训练，记录配置。","训练日志与checkpoint","训练资源不足风险"),
    ("模型测试","完成验证与泛化评估","运行 evaluate/test 并输出核心指标。","测试指标与误差分析","结果复现偏差风险"),
    ("结果分析","解释模型表现",analysis_step,"结论与改进建议","结果复现偏差风险"),
    ("实验报告整理","沉淀可提交材料","整理方法、实验、图表和结论。","可提交课程实验报告","报告撰写风险")]
    return [{"阶段名称":n,"任务目标":g,"具体操作":o,"预期产出":p,"关联风险":r,"建议优先级":i+1} for i,(n,g,o,p,r) in enumerate(names)]


def build_algorithm_summary(features, difficulty_result, risks, stage_plan):
    top_risks = "\n".join([f"- {r['风险名称']}({r['风险等级']},{r['风险分数']}): {r['风险原因']}" for r in risks[:5]])
    stages = "\n".join([f"{s['建议优先级']}. {s['阶段名称']} -> {s['具体操作']}" for s in stage_plan])
    return f"""【核心算法分析结果】
项目类型：{features.get('project_type','未知')}
关键特征：{', '.join(features.get('detected_keywords', []))}
缺失项：{', '.join(features.get('missing_items', [])) or '无'}
复现难度总分：{difficulty_result['total_score']}（{difficulty_result['level']}）
维度评分：{difficulty_result['dimension_scores']}
主要风险排序：\n{top_risks}
阶段任务规划：\n{stages}
生成约束：请严格依据上述评分、风险与阶段优先级输出可执行方案，避免空泛建议，需包含可量化指标与排错路径。"""
```

## `src/file_parser.py`

```text
from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile
from typing import Any

import pandas as pd
from docx import Document
from pypdf import PdfReader

MAX_TEXT_CHARS = 12000
MAX_TABLE_ROWS = 8
KEY_FILES = {
    "readme.md",
    "requirements.txt",
    "train.py",
    "main.py",
    "config.py",
    "model.py",
    "dataset.py",
    "data.py",
    "evaluate.py",
    "test.py",
}


def _safe_decode(raw: bytes) -> str:
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return ""


def _clip(text: str, limit: int = MAX_TEXT_CHARS) -> str:
    return text[:limit]


def parse_uploaded_files(uploaded_files) -> dict[str, Any]:
    result = {
        "texts": [],
        "file_summaries": [],
        "code_files": [],
        "zip_tree": "",
        "total_chars": 0,
        "python_file_count": 0,
        "has_pdf": False,
        "has_docx": False,
        "has_zip": False,
        "has_log": False,
        "uploaded_count": len(uploaded_files or []),
    }
    if not uploaded_files:
        return result

    for f in uploaded_files:
        name = f.name.lower()
        raw = f.getvalue()
        suffix = name.rsplit(".", 1)[-1] if "." in name else ""

        if suffix == "pdf":
            result["has_pdf"] = True
            reader = PdfReader(BytesIO(raw))
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
            text = _clip(text)
            result["texts"].append(text)
            result["file_summaries"].append(f"PDF:{f.name} 字符数={len(text)}")
        elif suffix == "docx":
            result["has_docx"] = True
            doc = Document(BytesIO(raw))
            text = _clip("\n".join(p.text for p in doc.paragraphs if p.text.strip()))
            result["texts"].append(text)
            result["file_summaries"].append(f"DOCX:{f.name} 段落字符数={len(text)}")
        elif suffix in {"txt", "md", "log", "py"}:
            text = _clip(_safe_decode(raw))
            if suffix == "log":
                result["has_log"] = True
            if suffix == "py":
                result["python_file_count"] += 1
                result["code_files"].append(f.name)
            result["texts"].append(text)
            result["file_summaries"].append(f"文本:{f.name} 字符数={len(text)}")
        elif suffix == "csv":
            df = pd.read_csv(BytesIO(raw), nrows=MAX_TABLE_ROWS)
            snippet = f"CSV:{f.name} 列={list(df.columns)}\n{df.head(MAX_TABLE_ROWS).to_markdown(index=False)}"
            result["texts"].append(_clip(snippet))
            result["file_summaries"].append(f"CSV:{f.name} 行预览={len(df)}")
        elif suffix == "xlsx":
            df = pd.read_excel(BytesIO(raw), nrows=MAX_TABLE_ROWS)
            snippet = f"XLSX:{f.name} 列={list(df.columns)}\n{df.head(MAX_TABLE_ROWS).to_markdown(index=False)}"
            result["texts"].append(_clip(snippet))
            result["file_summaries"].append(f"XLSX:{f.name} 行预览={len(df)}")
        elif suffix == "zip":
            result["has_zip"] = True
            with ZipFile(BytesIO(raw)) as zf:
                names = sorted([n for n in zf.namelist() if not n.endswith("/")])
                result["zip_tree"] = "\n".join(names[:200])
                result["python_file_count"] += sum(1 for n in names if n.endswith(".py"))
                for n in names:
                    lower = n.lower().split("/")[-1]
                    if n.endswith(".py"):
                        result["code_files"].append(n)
                    if lower in KEY_FILES:
                        content = _clip(_safe_decode(zf.read(n)))
                        result["texts"].append(f"[{n}]\n{content}")
                        result["file_summaries"].append(f"ZIP关键文件:{n}")
        else:
            result["file_summaries"].append(f"暂不解析:{f.name}")

    result["total_chars"] = sum(len(t) for t in result["texts"])
    return result
```

## `src/llm_client.py`

```text
from openai import OpenAI


def generate_with_llm(prompt: str, api_key: str, base_url: str, model: str, temperature: float) -> str:
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是工程人工智能课程中的科研复现指导专家，擅长将论文、代码和实验日志转化为可执行的科研复现方案。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        return f"[LLM调用失败] {exc}"
```

## `src/local_generator.py`

```text
def generate_local_reproduction_plan(project_info, extracted_text, code_summary, algorithm_result) -> str:
    text=(str(project_info)+"\n"+extracted_text+"\n"+code_summary).lower()
    if any(k in text for k in ["battery","电池","soh","rul","capacity","cycle"]):
        domain_tip="重点分析容量退化曲线、循环次数与 SOH/RUL 预测误差（MAE/RMSE）。"
    elif any(k in text for k in ["lane","车道线","detection"]):
        domain_tip="重点关注图像预处理、分割/检测指标及可视化。"
    elif any(k in text for k in ["randomforest","svm","xgboost"]):
        domain_tip="重点执行特征工程、交叉验证与模型对比。"
    else:
        domain_tip="重点完成数据、代码、环境三线并行复现。"

    d=algorithm_result["difficulty"]
    risks=algorithm_result["risks"]
    stages=algorithm_result["stage_plan"]
    risk_md="\n".join([f"- **{r['风险名称']}**（{r['风险等级']}:{r['风险分数']}）: {r['解决建议']}" for r in risks])
    stage_md="\n".join([f"### {s['建议优先级']}. {s['阶段名称']}\n- 目标：{s['任务目标']}\n- 操作：{s['具体操作']}\n- 输出：{s['预期产出']}" for s in stages])
    return f"""# 一、研究背景理解
本项目面向工程人工智能课程复现任务，目标是将论文与代码转化为可执行实验流程。{domain_tip}

# 二、方法与模型理解
请结合上传材料梳理模型输入输出、训练目标、损失函数与评价指标。

# 三、核心算法分析结果解读
- 复现难度：**{d['total_score']} / {d['level']}**
- 维度评分：{d['dimension_scores']}
- 评分原因：{'；'.join(d['reasons'])}

# 四、复现任务拆解
{stage_md}

# 五、代码复现指导
优先定位 train.py/main.py、config.py、model.py、dataset.py，并建立“配置->数据->训练->评估”执行链路。

# 六、实验计划表
|实验编号|实验目的|数据集|模型/方法|关键参数|评价指标|预期结果|记录内容|
|---|---|---|---|---|---|---|---|
|E1|基线复现|原始数据|基线模型|默认参数|MAE/RMSE|得到可运行基线|日志与配置|
|E2|调参优化|同上|目标模型|学习率/batch|MAE/RMSE/F1|性能提升|曲线与对比表|

# 七、风险提示与排错建议
{risk_md}

# 八、实验报告素材
- 实验目的：验证论文方法在目标数据上的可复现性。
- 实验原理：遵循论文方法并对关键模块进行对齐验证。
- 实验环境：记录 OS/Python/框架/CUDA 与依赖版本。
- 实验步骤：按阶段执行并记录证据链。
- 实验分析思路：从数据质量、模型结构、超参数和资源约束四维分析。

# 九、后续优化方向
从数据增强、模型压缩、自动化实验管理、可解释性分析和LLM代理协同五个方向迭代。"""
```

## `src/prompts.py`

```text
def build_reproduction_prompt(project_info, extracted_text, code_summary, algorithm_summary) -> str:
    info = "\n".join([f"- {k}: {v}" for k, v in project_info.items()])
    return f"""你是一名工程人工智能课程的科研复现指导专家。
请根据以下项目材料、代码结构和核心算法分析结果，为学生生成科研复现方案。

## 项目信息
{info}

## 上传材料摘要
{extracted_text[:5000]}

## 代码结构摘要
{code_summary[:3000]}

## 核心算法分析结果
{algorithm_summary}

请严格按照以下结构输出：
# 一、研究背景理解
# 二、方法与模型理解
# 三、核心算法分析结果解读
# 四、复现任务拆解
# 五、代码复现指导
# 六、实验计划表
# 七、风险提示与排错建议
# 八、实验报告素材
# 九、后续优化方向

要求：
1) 输出中文、Markdown格式；2) 结合上传材料与核心算法分析结果；
3) 不要空泛回答；4) 内容可直接用于课程实验报告。"""
```

## `src/render.py`

```text
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
```

## `src/utils.py`

```text

```

## `tests/conftest.py`

```text
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

## `tests/test_core_algorithm.py`

```text
from src.core_algorithm import extract_project_features, calculate_reproduction_difficulty, rank_reproduction_risks, generate_stage_plan

def test_core_algo_pipeline():
    parsed={"texts":["battery LSTM MAE RMSE CUDA loss"],"code_files":["train.py","dataset.py","model.py"],"zip_tree":"requirements.txt\nmain.py","has_pdf":True,"has_docx":False,"has_zip":True,"has_log":True,"python_file_count":5,"total_chars":200}
    info={"复现项目名称":"x"}
    ext=extract_project_features(parsed,info)
    assert ext["features"]["mention_lstm"]
    diff=calculate_reproduction_difficulty(ext["features"])
    assert "total_score" in diff and "level" in diff
    risks=rank_reproduction_risks(ext["features"],diff)
    assert risks[0]["风险分数"] >= risks[-1]["风险分数"]
    plan=generate_stage_plan(ext["features"],risks)
    assert len(plan)==8
```

## `tests/test_file_parser.py`

```text
from io import BytesIO
from src.file_parser import parse_uploaded_files

class UF:
    def __init__(self,name,data): self.name=name; self._data=data
    def getvalue(self): return self._data

def test_parse_txt_file():
    r = parse_uploaded_files([UF("a.txt", b"hello battery")])
    assert r["total_chars"] > 0
    assert any("hello" in t for t in r["texts"])
```

## `tests/test_local_generator.py`

```text
from src.local_generator import generate_local_reproduction_plan

def test_local_plan_markdown():
    md=generate_local_reproduction_plan({"a":"battery"},"LSTM MAE RMSE","train.py",{"difficulty":{"total_score":70,"level":"高难度","dimension_scores":{},"reasons":[]},"risks":[],"stage_plan":[]})
    assert "# 一、研究背景理解" in md and "# 九、后续优化方向" in md
```

## `tests/test_prompts.py`

```text
from src.prompts import build_reproduction_prompt

def test_prompt_contains_algorithm_words():
    p=build_reproduction_prompt({"x":"y"},"a","b","核心算法分析结果:xx")
    assert "核心算法分析结果" in p
```
