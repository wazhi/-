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
