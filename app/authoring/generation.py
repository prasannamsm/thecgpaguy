from app.llm import ollama_chat


def generate_definition(concept_title: str, textbook_passage: str) -> str:
    system_prompt = (
        "You are an academic content generator for engineering curricula. "
        "Generate a concise, rigorous definition grounded in the provided textbook passage. "
        "Include a citation reference."
    )
    user_prompt = f"Concept: {concept_title}\n\nTextbook passage:\n{textbook_passage}\n\nGenerate: definition with source citation."
    return ollama_chat(system_prompt, user_prompt)


def generate_analogy(concept_title: str, definition: str) -> str:
    system_prompt = (
        "You are a pedagogical assistant. Generate a simple, memorable analogy "
        "for the given concept that a first-year engineering student would understand."
    )
    user_prompt = f"Concept: {concept_title}\nDefinition: {definition}\n\nGenerate: a relatable analogy."
    return ollama_chat(system_prompt, user_prompt)


def generate_assessment_question(
    concept_title: str,
    definition: str,
    question_type: str = "SHORT_ANSWER",
) -> dict:
    system_prompt = (
        "You are an assessment generator for engineering exams. "
        "Create a question and structured answer key."
    )
    user_prompt = (
        f"Concept: {concept_title}\nDefinition: {definition}\n"
        f"Question type: {question_type}\n\n"
        f"Generate: a challenging question and its structured answer key."
    )
    result = ollama_chat(system_prompt, user_prompt)
    return {
        "question_text": result,
        "question_type": question_type,
        "answer_key": result,
    }


def generate_multi_correct_pool(
    concept_title: str, num_options: int = 15
) -> dict:
    system_prompt = (
        "You are an assessment generator. Create a multi-correct MCQ pool "
        "where 3-6 options out of 10-30 are correct. Return JSON with "
        "options array (each with text and is_correct boolean)."
    )
    user_prompt = (
        f"Concept: {concept_title}\n"
        f"Generate {num_options} options for a multi-correct matrix question. "
        f"Ensure 3-6 are correct."
    )
    result = ollama_chat(system_prompt, user_prompt)
    return {"options": result}
