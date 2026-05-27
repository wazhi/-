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
