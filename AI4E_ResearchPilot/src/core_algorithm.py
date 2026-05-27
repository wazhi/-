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
