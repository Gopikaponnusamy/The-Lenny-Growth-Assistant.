import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from backend.database import Base


# ==========================================
# CHAT SESSION
# ==========================================

class ChatSession(Base):

    __tablename__ = "chat_sessions"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    title = Column(
        String,
        default="New Chat"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    messages = relationship(

        "ChatMessage",

        back_populates="session",

        cascade="all, delete-orphan"

    )


# ==========================================
# CHAT MESSAGE
# ==========================================

class ChatMessage(Base):

    __tablename__ = "chat_messages"


    id = Column(

        String,

        primary_key=True,

        default=lambda: str(uuid.uuid4())

    )


    session_id = Column(

        String,

        ForeignKey(
            "chat_sessions.id"
        ),

        nullable=False

    )


    role = Column(

        String,

        nullable=False

    )


    content = Column(

        Text,

        nullable=False

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    session = relationship(

        "ChatSession",

        back_populates="messages"

    )


# ==========================================
# ARTIFACT
# ==========================================

class Artifact(Base):

    __tablename__ = "artifacts"


    id = Column(

        String,

        primary_key=True,

        default=lambda: str(uuid.uuid4())

    )


    session_id = Column(

        String,

        nullable=True

    )


    title = Column(

        String,

        default="Generated Artifact"

    )


    type = Column(

        String,

        default="markdown"

    )


    content = Column(

        Text,

        nullable=False

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )