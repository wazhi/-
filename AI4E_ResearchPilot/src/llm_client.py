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
