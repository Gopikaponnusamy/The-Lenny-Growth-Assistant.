from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

from backend.agent import process_message


# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="Lenny Growth OS API",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# SIMPLE IN-MEMORY DATABASE
# ==========================================

sessions = {}


# ==========================================
# REQUEST MODELS
# ==========================================

class SessionCreate(BaseModel):

    title: str = "New Chat"


class MessageCreate(BaseModel):

    content: str


# ==========================================
# HEALTH
# ==========================================

@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "service": "lenny-growth-os"
    }


# ==========================================
# LIST SESSIONS
# ==========================================

@app.get("/api/sessions")
def list_sessions():

    result = []

    for session_id, session in sessions.items():

        result.append({

            "id": session_id,

            "title":
                session["title"]

        })

    return result


# ==========================================
# CREATE SESSION
# ==========================================

@app.post("/api/sessions")
def create_session(
    data: SessionCreate
):

    session_id = str(
        uuid4()
    )

    sessions[session_id] = {

        "id":
            session_id,

        "title":
            data.title,

        "messages":
            []

    }

    print(
        "Created session:",
        session_id
    )

    return {

        "id":
            session_id,

        "title":
            data.title

    }


# ==========================================
# GET SESSION
# ==========================================

@app.get(
    "/api/sessions/{session_id}"
)
def get_session(
    session_id: str
):

    if session_id not in sessions:

        raise HTTPException(

            status_code=404,

            detail="Session not found"

        )


    return sessions[
        session_id
    ]


# ==========================================
# DELETE SESSION
# ==========================================

@app.delete(
    "/api/sessions/{session_id}"
)
def delete_session(
    session_id: str
):

    if session_id not in sessions:

        raise HTTPException(

            status_code=404,

            detail="Session not found"

        )


    del sessions[
        session_id
    ]


    return {

        "message":
            "Session deleted"

    }


# ==========================================
# SEND MESSAGE
# ==========================================

@app.post(
    "/api/sessions/{session_id}/messages"
)
def send_message(

    session_id: str,

    data: MessageCreate

):

    # --------------------------------------
    # CHECK SESSION
    # --------------------------------------

    if session_id not in sessions:

        raise HTTPException(

            status_code=404,

            detail="Session not found"

        )


    question = data.content.strip()


    if not question:

        raise HTTPException(

            status_code=400,

            detail="Message cannot be empty"

        )


    print(
        "\n======================================"
    )

    print(
        "USER QUESTION:",
        question
    )

    print(
        "======================================"
    )


    # --------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------

    user_message_id = str(
        uuid4()
    )


    sessions[
        session_id
    ]["messages"].append({

        "id":
            user_message_id,

        "role":
            "user",

        "content":
            question

    })


    # --------------------------------------
    # CALL LENNY AGENT
    # --------------------------------------

    try:

        result = process_message(
            question
        )


        print(
            "\nAGENT RESULT:"
        )

        print(
            result
        )


    except Exception as e:

        print(
            "\nAGENT ERROR:",
            str(e)
        )


        raise HTTPException(

            status_code=500,

            detail=
                f"Agent error: {str(e)}"

        )


    # --------------------------------------
    # GET ANSWER
    # --------------------------------------

    if isinstance(
        result,
        dict
    ):

        answer = (

            result.get(
                "content"
            )

            or

            result.get(
                "answer"
            )

            or

            result.get(
                "response"
            )

            or

            result.get(
                "message"
            )

        )


        skill = result.get(

            "skill",

            "qa"

        )


        sources = result.get(

            "sources",

            []

        )


        artifact = result.get(

            "artifact",

            None

        )


    else:

        answer = str(
            result
        )

        skill = "qa"

        sources = []

        artifact = None


    # --------------------------------------
    # EMPTY ANSWER CHECK
    # --------------------------------------

    if not answer:

        answer = (

            "Sorry, I could not generate "
            "an answer. Please try again."

        )


    # --------------------------------------
    # SAVE ASSISTANT MESSAGE
    # --------------------------------------

    assistant_message_id = str(
        uuid4()
    )


    sessions[
        session_id
    ]["messages"].append({

        "id":
            assistant_message_id,

        "role":
            "assistant",

        "content":
            answer

    })


    # --------------------------------------
    # UPDATE CHAT TITLE
    # --------------------------------------

    if (

        sessions[
            session_id
        ]["title"]

        ==

        "New Chat"

    ):

        sessions[
            session_id
        ]["title"] = (

            question[:50]

            +

            (
                "..."

                if len(question) > 50

                else ""

            )

        )


    # --------------------------------------
    # RETURN RESPONSE
    # --------------------------------------

    print(
        "\nFINAL ANSWER:"
    )

    print(
        answer
    )

    print(
        "======================================\n"
    )


    return {

        "message_id":
            assistant_message_id,

        "content":
            answer,

        "skill":
            skill,

        "sources":
            sources,

        "artifact":
            artifact

    }