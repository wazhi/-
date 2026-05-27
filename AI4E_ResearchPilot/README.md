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

## 无二进制交付（文本/Markdown）
在不支持二进制文件的平台，可运行：
```bash
python scripts/export_text_bundle.py
```
生成 `docs/project_text_bundle.md`，其中包含项目源码文本快照，便于粘贴/审阅/创建PR。
