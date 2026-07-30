import json

from app.llm import ollama_chat


def semantic_check(
    student_answer: str, answer_key: str, max_score: float = 10.0
) -> dict:
    system_prompt = (
        "You are a grading assistant. Compare the student's answer to the expected answer key. "
        "Evaluate only for semantic equivalence — does the answer contain the required concepts and "
        "logical steps? Do not penalize wording differences. "
        f"Max score: {max_score}."
    )
    user_prompt = (
        f"Answer key (required concepts): {answer_key}\n\n"
        f"Student answer: {student_answer}\n\n"
        "Return a JSON object with keys: 'score' (float), 'feedback' (string), "
        "'concepts_present' (list of strings), 'concepts_missing' (list of strings)."
    )
    raw = ollama_chat(system_prompt, user_prompt, timeout=60)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"score": 0.0, "feedback": raw, "concepts_present": [], "concepts_missing": []}
    return result
