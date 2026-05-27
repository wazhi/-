from src.local_generator import generate_local_reproduction_plan

def test_local_plan_markdown():
    md=generate_local_reproduction_plan({"a":"battery"},"LSTM MAE RMSE","train.py",{"difficulty":{"total_score":70,"level":"高难度","dimension_scores":{},"reasons":[]},"risks":[],"stage_plan":[]})
    assert "# 一、研究背景理解" in md and "# 九、后续优化方向" in md
