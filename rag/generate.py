"""
Generation stage of the RAG pipeline - now using Google's Gemini API
(free tier), instead of Claude, so you can build/test without cost.

Takes the sections found by retrieve.py and asks the LLM to explain them
in plain language for the user's specific situation. The key design
choice: the prompt forces the model to ONLY use the retrieved text,
never make up a section number or law that wasn't actually retrieved.

Setup:
1. Get a free API key: https://aistudio.google.com/apikey
2. Set it as an environment variable:
    export GEMINI_API_KEY=your-key-here   (Mac/Linux)
    set GEMINI_API_KEY=your-key-here      (Windows cmd)
3. pip install google-genai
"""

import os
from google import genai
from google.genai import types

client = None  # created lazily, only once an API key is actually needed

# If this model name ever stops working (Google renames/deprecates models
# fairly often), check https://ai.google.dev/gemini-api/docs/models for
# the current free-tier Flash model name and swap it in below.
MODEL_NAME = "gemini-2.5-flash"


def get_client():
    global client
    if client is None:
        client = genai.Client()  # reads GEMINI_API_KEY from environment
    return client


def build_context(retrieved_sections):
    """Turn the retrieved sections into plain text the model can read."""
    blocks = []
    for section, score in retrieved_sections:
        block = (
            f"Act: {section['act']}\n"
            f"Section: {section['section']}\n"
            f"Title: {section['title']}\n"
            f"Summary: {section['summary']}\n"
            f"What to do: {section['what_to_do']}\n"
        )
        if section.get("punishment"):
            block += f"Punishment/Remedy: {section['punishment']}\n"
        blocks.append(block)
    return "\n---\n".join(blocks)


SYSTEM_PROMPT = """You are a legal information assistant for Indian law. You help \
users understand which law sections may apply to their situation.

STRICT RULES - follow these exactly:
1. Only reference sections, acts, and section numbers that appear in the \
CONTEXT provided below. Never invent, guess, or recall a section number \
from your own general knowledge, even if you believe it exists.
2. If the CONTEXT doesn't contain a good match for the user's situation, \
say so clearly instead of forcing an answer.
3. Explain the applicable section(s) in plain, simple language.
4. Always tell the user what practical next step to take.
5. End every answer with: "This is general legal information, not legal \
advice for your specific case. Please consult a licensed advocate before \
taking action."
"""


def generate_answer(user_query, retrieved_sections):
    if not retrieved_sections:
        return (
            "I couldn't find a section in the current database that clearly "
            "matches your situation. This may be outside what's covered so far, "
            "or you may want to rephrase. Please consult a licensed advocate for "
            "guidance on your specific case."
        )

    context = build_context(retrieved_sections)

    user_prompt = (
        f"CONTEXT (retrieved law sections):\n{context}\n\n"
        f"USER'S SITUATION:\n{user_query}\n\n"
        "Explain which section(s) apply and what the user should do."
    )

    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=600,
        ),
    )
    return response.text


if __name__ == "__main__":
    from retrieve import LawRetriever

    retriever = LawRetriever()
    query = "my neighbour keeps threatening to hurt me"
    results = retriever.retrieve(query)

    if not os.environ.get("GEMINI_API_KEY"):
        print("Set GEMINI_API_KEY environment variable to test generation.")
        print("Retrieved sections that would be sent to the LLM:")
        for section, score in results:
            print(f"  [{score:.2f}] {section['act']} Sec {section['section']}")
    else:
        answer = generate_answer(query, results)
        print(answer)