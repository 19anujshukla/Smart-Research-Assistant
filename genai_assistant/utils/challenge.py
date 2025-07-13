import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# ✅ Generate 3 logic-based, clean questions from document
def generate_questions(document_text):
    prompt = f"""You are an exam paper setter. From the following document, create 3 logic-based, comprehension-focused questions that test a student's understanding.

Document:
{document_text[:3000]}
Questions:"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=300,
        temperature=0.5
    )

    raw_lines = response.generations[0].text.strip().split("\n")

    # ✅ Advanced filtering logic
    questions = []
    for line in raw_lines:
        cleaned = line.strip("•-–0123456789. ").strip()

        # Skip introductory or empty lines
        if not cleaned:
            continue
        if cleaned.lower().startswith("here are") or cleaned.lower().startswith("these"):
            continue

        # Accept if looks like a real question
        if "?" in cleaned or any(word in cleaned.lower() for word in ["explain", "describe", "define", "compare", "summarize"]):
            questions.append(cleaned)

        if len(questions) == 3:
            break

    # ✅ Fallback: if fewer than 3 good questions, fill with dummy
    while len(questions) < 3:
        questions.append("⚠️ [Question could not be generated. Try again or re-upload a clearer document.]")

    return questions

# ✅ Evaluate user answer using Cohere LLM
def evaluate_answer(question, user_answer, document_text):
    prompt = f"""Evaluate the user's answer to a question based on the following document. Give a score out of 5 and explain the reasoning.

Question: {question}
User's Answer: {user_answer}
Document: {document_text[:3000]}

Your evaluation (include score and reasoning):"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=300,
        temperature=0.3
    )
    return response.generations[0].text.strip()
