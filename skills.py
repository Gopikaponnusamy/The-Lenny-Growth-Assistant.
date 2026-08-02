from backend.llm import ask_ollama
from backend.prompts import (
    SYSTEM_PROMPT,
    SHIP30_PROMPT,
    ARTIFACT_PROMPT
)


# ==========================================
# Q&A SKILL
# ==========================================

def qa_skill(
    question: str,
    context: str
):
    """
    Answer a user's question using
    Lenny's Podcast transcript context.
    """

    prompt = SYSTEM_PROMPT.format(

        context=context,

        question=question

    )


    answer = ask_ollama(

        prompt

    )


    return {

        "type": "answer",

        "content": answer

    }


# ==========================================
# SHIP30 ESSAY SKILL
# ==========================================

def essay_skill(
    question: str,
    context: str
):
    """
    Generate a long-form essay based on
    Lenny's Podcast transcript insights.
    """

    prompt = SHIP30_PROMPT.format(

        context=context,

        question=question

    )


    answer = ask_ollama(

        prompt

    )


    return {

        "type": "essay",

        "content": answer

    }


# ==========================================
# ARTIFACT SKILL
# ==========================================

def artifact_skill(
    question: str,
    context: str
):
    """
    Generate a Markdown or HTML artifact.
    """

    prompt = ARTIFACT_PROMPT.format(

        context=context,

        question=question

    )


    answer = ask_ollama(

        prompt

    )


    return parse_artifact(

        answer

    )


# ==========================================
# PARSE ARTIFACT
# ==========================================

def parse_artifact(
    response: str
):
    """
    Convert the LLM artifact response
    into a structured object.
    """

    artifact_type = "markdown"

    title = "Generated Artifact"

    content = response


    # Find TYPE
    if "TYPE:" in response:

        try:

            type_part = response.split(
                "TYPE:",
                1
            )[1].split(
                "\n",
                1
            )[0].strip().lower()


            if type_part in [

                "html",

                "markdown"

            ]:

                artifact_type = type_part

        except Exception:

            pass


    # Find TITLE
    if "TITLE:" in response:

        try:

            title = response.split(

                "TITLE:",

                1

            )[1].split(

                "\n",

                1

            )[0].strip()

        except Exception:

            pass


    # Find CONTENT
    if "CONTENT:" in response:

        try:

            content = response.split(

                "CONTENT:",

                1

            )[1].strip()

        except Exception:

            pass


    # Remove Markdown code fences
    if content.startswith(
        "```"
    ):

        lines = content.splitlines()


        if len(lines) > 2:

            content = "\n".join(

                lines[1:-1]

            )


    return {

        "type":
            "artifact",

        "artifact_type":
            artifact_type,

        "title":
            title,

        "content":
            content

    }


# ==========================================
# SKILL ROUTER
# ==========================================

def detect_skill(
    question: str
):
    """
    Decide which skill should be used.
    """

    text = question.lower()


    # ======================================
    # ARTIFACT REQUEST
    # ======================================

    artifact_words = [

        "artifact",

        "html",

        "css",

        "website",

        "webpage",

        "landing page",

        "dashboard",

        "component",

        "code",

        "markdown file",

        "create a page"

    ]


    for word in artifact_words:

        if word in text:

            return "artifact"


    # ======================================
    # ESSAY REQUEST
    # ======================================

    essay_words = [

        "essay",

        "write an article",

        "write a post",

        "ship30",

        "ship 30",

        "long form",

        "long-form",

        "detailed article",

        "newsletter"

    ]


    for word in essay_words:

        if word in text:

            return "essay"


    # ======================================
    # DEFAULT = Q&A
    # ======================================

    return "qa"


# ==========================================
# RUN SKILL
# ==========================================

def run_skill(

    question: str,

    context: str

):
    """
    Detect the correct skill and execute it.
    """

    skill = detect_skill(

        question

    )


    if skill == "essay":

        return essay_skill(

            question,

            context

        )


    if skill == "artifact":

        return artifact_skill(

            question,

            context

        )


    return qa_skill(

        question,

        context

    )