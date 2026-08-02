from backend.rag import search_transcripts
from backend.llm import generate_response


# ==========================================
# PROCESS USER MESSAGE
# ==========================================

def process_message(question):

    print("\n======================================")
    print("LENNY GROWTH ASSISTANT")
    print("======================================")

    print("Question:", question)

    # ======================================
    # SEARCH TRANSCRIPTS
    # ======================================

    print("\nSearching Lenny transcripts...")

    try:

        results = search_transcripts(
            question,
            top_k=5
        )

    except Exception as e:

        print(
            "RAG search error:",
            e
        )

        results = []


    print(
        "Search results:",
        len(results)
    )


    # ======================================
    # BUILD CONTEXT
    # ======================================

    context_parts = []


    for result in results:

        if isinstance(
            result,
            dict
        ):

            text = (

                result.get(
                    "text",
                    ""
                )

                or

                result.get(
                    "content",
                    ""
                )

            )


            if text:

                context_parts.append(
                    text
                )


        elif isinstance(
            result,
            str
        ):

            context_parts.append(
                result
            )


    context = "\n\n".join(
        context_parts
    )


    print(
        "Context length:",
        len(context)
    )


    # ======================================
    # CREATE PROMPT
    # ======================================

    prompt = f"""
You are Lenny Growth Assistant.

You are an expert product and growth advisor.

Answer the user's question clearly and practically.

Use the Lenny Podcast transcript context below
when it is relevant.

If the transcript context does not contain enough
information, you can still provide a useful answer
based on your general knowledge.

Do NOT say:
"There is insufficient evidence"
or
"I could not generate an answer"

Instead, give the best helpful answer possible.

------------------------------------------
USER QUESTION
------------------------------------------

{question}

------------------------------------------
LENNY PODCAST TRANSCRIPT CONTEXT
------------------------------------------

{context}

------------------------------------------
YOUR ANSWER
------------------------------------------

Answer the user's question now.
"""


    print(
        "\nSending prompt to Ollama..."
    )


    # ======================================
    # CALL OLLAMA
    # ======================================

    try:

        answer = generate_response(
            prompt
        )


    except Exception as e:

        print(
            "LLM ERROR:",
            e
        )

        answer = (

            "Sorry, I could not generate "
            "an answer from the AI model."

        )


    # ======================================
    # CHECK ANSWER
    # ======================================

    if not answer:

        answer = (

            "Sorry, I could not generate "
            "an answer."

        )


    print(
        "\nAnswer received:"
    )

    print(
        answer
    )


    # ======================================
    # RETURN TO MAIN.PY
    # ======================================

    return {

        "content":
            answer,

        "skill":
            "qa",

        "sources":
            [],

        "artifact":
            None

    }