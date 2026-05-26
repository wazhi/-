# AI4E-Learn（Python版）

## 项目简介
AI4E-Learn 是面向“工程人工智能”课程大作业展示的个性化学习路径规划平台。主语言为 **Python**，采用 **FastAPI + Jinja2** 构建可本地运行的教学辅助 Web 系统。

## 功能模块
- `/` 首页 Dashboard
- `/students` 学生画像
- `/knowledge-graph` 课程知识图谱
- `/diagnosis` 学习诊断
- `/recommendation` 个性化路径推荐（7天）
- `/resources` 学习资源推荐
- `/analytics` 数据报表与可视化
- `/ai-modules` AI 功能说明

## 核心算法
见 `py_ai4e/algorithms.py`：
- `calculate_mastery`
- `mastery_level`
- `diagnose`
- `diagnosis_text`
- `learning_path`
- `recommend_resources`
- `risk_level`

## 运行方式
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
访问 `http://127.0.0.1:8000`。

## 项目亮点
- 全部基于本地 mock 数据，易演示、易答辩。
- 推荐结果动态计算，不是静态写死。
- 诊断、路径、资源推荐均带可解释文本。

## 后续优化
- 引入 SQLite 持久化
- 使用 scikit-learn 建立风险预测模型
- 前后端分离并增加教师管理端
