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
