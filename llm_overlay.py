import os
import openai


def llm_reply(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Return a reply from the specified OpenAI model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY environment variable not set."

    client = openai.OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content.strip()
    except Exception as exc:
        return f"LLM error: {exc}"
