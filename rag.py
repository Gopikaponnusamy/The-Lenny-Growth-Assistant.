import json
import os
import math
import re


# ==========================================
# VECTOR STORE LOCATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

VECTOR_STORE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vector_store.json"
)


# ==========================================
# LOAD VECTOR STORE
# ==========================================

def load_vector_store():

    if not os.path.exists(
        VECTOR_STORE_PATH
    ):

        print(
            "ERROR: Vector store not found:"
        )

        print(
            VECTOR_STORE_PATH
        )

        return []


    try:

        with open(
            VECTOR_STORE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        # Handle different JSON formats

        if isinstance(
            data,
            list
        ):

            return data


        if isinstance(
            data,
            dict
        ):

            # Common formats

            if "chunks" in data:

                return data["chunks"]


            if "documents" in data:

                return data["documents"]


            if "data" in data:

                return data["data"]


        return []


    except Exception as e:

        print(
            "Error loading vector store:",
            e
        )

        return []


# ==========================================
# SIMPLE TEXT TOKENIZER
# ==========================================

def tokenize(text):

    if not text:

        return []


    text = text.lower()


    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text
    )


# ==========================================
# TEXT SIMILARITY
# ==========================================

def calculate_similarity(
    query,
    text
):

    query_words = set(
        tokenize(query)
    )

    text_words = set(
        tokenize(text)
    )


    if not query_words:

        return 0.0


    if not text_words:

        return 0.0


    # Word overlap

    intersection = (

        query_words
        &
        text_words

    )


    score = (

        len(intersection)

        /

        len(query_words)

    )


    return score


# ==========================================
# SEARCH TRANSCRIPTS
# ==========================================

def search_transcripts(

    query,

    top_k=5

):

    print(
        "Loading vector store..."
    )


    documents = load_vector_store()


    print(
        f"Loaded {len(documents)} vector chunks."
    )


    if not documents:

        print(
            "WARNING: No documents found."
        )

        return []


    results = []


    # ======================================
    # SEARCH EACH CHUNK
    # ======================================

    for document in documents:

        # ----------------------------------
        # GET TEXT
        # ----------------------------------

        if isinstance(
            document,
            dict
        ):

            text = (

                document.get(
                    "text",
                    ""
                )

                or

                document.get(
                    "content",
                    ""
                )

                or

                document.get(
                    "chunk",
                    ""
                )

            )


        elif isinstance(
            document,
            str
        ):

            text = document


        else:

            continue


        if not text:

            continue


        # ----------------------------------
        # CALCULATE SCORE
        # ----------------------------------

        score = calculate_similarity(

            query,

            text

        )


        results.append({

            "text":
                text,

            "score":
                score

        })


    # ======================================
    # SORT RESULTS
    # ======================================

    results.sort(

        key=lambda x:
            x["score"],

        reverse=True

    )


    # ======================================
    # GET TOP RESULTS
    # ======================================

    top_results = results[
        :top_k
    ]


    print(
        "\nTop transcript results:"
    )


    for result in top_results:

        print(

            "- Score:",

            round(
                result["score"],
                4
            )

        )


    return top_results