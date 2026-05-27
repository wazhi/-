from src.prompts import build_reproduction_prompt

def test_prompt_contains_algorithm_words():
    p=build_reproduction_prompt({"x":"y"},"a","b","核心算法分析结果:xx")
    assert "核心算法分析结果" in p
