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
