# System Architecture Document

# The Lenny Growth Assistant

**Version:** 1.0
**Project Type:** Full-Stack Agentic AI Application

---

# 1. Architecture Overview

The Lenny Growth Assistant is a full-stack Agentic AI application designed to provide transcript-grounded answers, generate long-form content, and create interactive artifacts.

The system consists of the following major components:

1. Frontend Application
2. FastAPI Backend
3. Agent Router
4. Q&A Skill
5. Ship30for30 Essay Skill
6. Artifact Generation Skill
7. RAG Knowledge Base
8. LLM Configuration Layer
9. PostgreSQL Database
10. Artifact Viewer

High-level architecture:

```text
                         ┌───────────────────────┐
                         │         User          │
                         │       Browser         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       Frontend        │
                         │                       │
                         │  Chat UI              │
                         │  Session History      │
                         │  Artifact Viewer      │
                         └───────────┬───────────┘
                                     │
                                HTTP / REST
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      FastAPI API      │
                         │                       │
                         │  Session Management   │
                         │  Chat API             │
                         │  Artifact API         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     Agent Router      │
                         └───────────┬───────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ▼                    ▼                    ▼
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
        │  Q&A Skill   │     │ Essay Skill  │     │ Artifact     │
        │              │     │              │     │ Skill        │
        └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
               │                    │                    │
               ▼                    ▼                    ▼
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
        │ RAG Pipeline │     │ Transcript   │     │ HTML/CSS     │
        │              │     │ Context      │     │ Markdown     │
        └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
               │                    │                    │
               └────────────────────┼────────────────────┘
                                    │
                                    ▼
                         ┌───────────────────────┐
                         │   LLM Configuration   │
                         │                       │
                         │  Ollama / Cloud LLM   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      PostgreSQL       │
                         │                       │
                         │  Users                │
                         │  Sessions             │
                         │  Messages             │
                         └───────────────────────┘
```

---

# 2. Technology Stack

| Layer            | Technology                    |
| ---------------- | ----------------------------- |
| Frontend         | HTML, CSS, JavaScript / React |
| Backend          | FastAPI                       |
| API Server       | Uvicorn                       |
| Database         | PostgreSQL                    |
| Database Hosting | Supabase / Railway            |
| Local LLM        | Ollama                        |
| Cloud LLM        | Configurable Provider         |
| Knowledge Source | Lenny's Podcast Transcripts   |
| AI Pattern       | RAG + Agentic Routing         |
| Artifact Types   | HTML, CSS, Markdown           |
| Version Control  | Git + GitHub                  |

---

# 3. Backend Architecture

The FastAPI backend acts as the central application layer.

The backend is responsible for:

* Receiving user requests.
* Managing chat sessions.
* Loading conversation history.
* Routing requests to the appropriate skill.
* Retrieving transcript context.
* Calling the configured LLM.
* Generating artifacts.
* Saving conversations.
* Returning responses to the frontend.

The backend is organized into separate modules.

```text
backend/
│
├── main.py
│       └── FastAPI application and API routes
│
├── database.py
│       └── PostgreSQL database connection
│
├── models.py
│       └── Database models
│
├── agent.py
│       └── Agent routing logic
│
├── rag.py
│       └── Knowledge retrieval
│
├── llm.py
│       └── LLM provider configuration
│
└── prompts.py
        └── Prompt templates and skill instructions
```

This separation keeps the application modular and easier to maintain.

---

# 4. Database Architecture

The application uses PostgreSQL as the persistent database.

The database stores:

* User metadata
* Chat sessions
* Conversation messages

The database ensures that conversations remain available after restarting the application.

---

# 5. Database Schema

## 5.1 Users Table

The `users` table stores basic user information.

```text
users
────────────────────────────
id              UUID / INT
name            VARCHAR
email           VARCHAR
created_at      TIMESTAMP
```

### Fields

| Field        | Type           | Description           |
| ------------ | -------------- | --------------------- |
| `id`         | UUID / Integer | Primary key           |
| `name`       | String         | User name             |
| `email`      | String         | User email            |
| `created_at` | Timestamp      | Account creation time |

---

## 5.2 Sessions Table

The `sessions` table represents individual conversations.

```text
sessions
────────────────────────────
id              UUID
user_id         UUID
title           VARCHAR
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### Fields

| Field        | Type      | Description           |
| ------------ | --------- | --------------------- |
| `id`         | UUID      | Primary key           |
| `user_id`    | UUID      | Reference to user     |
| `title`      | String    | Chat title            |
| `created_at` | Timestamp | Session creation time |
| `updated_at` | Timestamp | Last activity time    |

---

## 5.3 Messages Table

The `messages` table stores individual conversation messages.

```text
messages
────────────────────────────
id              UUID
session_id      UUID
role            VARCHAR
content         TEXT
created_at      TIMESTAMP
```

### Fields

| Field        | Type      | Description           |
| ------------ | --------- | --------------------- |
| `id`         | UUID      | Primary key           |
| `session_id` | UUID      | Reference to session  |
| `role`       | String    | `user` or `assistant` |
| `content`    | Text      | Message content       |
| `created_at` | Timestamp | Message creation time |

---

# 6. Database Relationships

The database relationships are:

```text
Users
  │
  │ 1
  │
  │
  │ N
Sessions
  │
  │ 1
  │
  │
  │ N
Messages
```

A single user can have multiple chat sessions.

A single session can contain multiple messages.

This structure ensures that each chat session maintains its own conversation context.

---

# 7. Session Management

When a user clicks **New Chat**:

```text
User clicks New Chat
        ↓
POST /sessions
        ↓
Generate unique session ID
        ↓
Create session in PostgreSQL
        ↓
Return session ID
        ↓
Frontend opens empty conversation
```

When the user sends a message:

```text
User Message
      ↓
POST /chat
      ↓
Validate Session ID
      ↓
Load Previous Messages
      ↓
Process User Request
      ↓
Generate AI Response
      ↓
Save User Message
      ↓
Save Assistant Message
      ↓
Return Response
```

This ensures that each session has an independent context.

---

# 8. API Endpoints

The FastAPI application exposes REST endpoints.

---

## 8.1 Health Check

### Request

```text
GET /
```

### Purpose

Checks whether the backend is running.

### Response

```json
{
  "status": "ok"
}
```

---

## 8.2 Health Endpoint

### Request

```text
GET /health
```

### Purpose

Checks application and dependency health.

### Response

```json
{
  "status": "healthy"
}
```

---

## 8.3 Create New Session

### Request

```text
POST /sessions
```

### Purpose

Creates a new chat session.

### Example Response

```json
{
  "session_id": "abc123",
  "title": "New Chat"
}
```

---

## 8.4 Get Sessions

### Request

```text
GET /sessions
```

### Purpose

Returns previous chat sessions.

### Example Response

```json
[
  {
    "session_id": "abc123",
    "title": "Product Market Fit"
  },
  {
    "session_id": "xyz789",
    "title": "Growth Strategies"
  }
]
```

---

## 8.5 Get Session

### Request

```text
GET /sessions/{session_id}
```

### Purpose

Returns the details of a specific conversation.

---

## 8.6 Chat Endpoint

### Request

```text
POST /chat
```

### Request Body

```json
{
  "session_id": "abc123",
  "message": "How do successful startups achieve product-market fit?"
}
```

### Processing

```text
Request
   ↓
Validate Session
   ↓
Load Conversation
   ↓
Agent Router
   ↓
Select Skill
   ↓
Execute Skill
   ↓
Generate Response
   ↓
Save Messages
   ↓
Return Response
```

---

## 8.7 Get Messages

### Request

```text
GET /messages/{session_id}
```

### Purpose

Returns all messages belonging to a specific session.

---

## 8.8 Artifact Endpoint

### Request

```text
POST /artifact
```

### Example Request

```json
{
  "session_id": "abc123",
  "prompt": "Create a startup landing page"
}
```

### Example Response

```json
{
  "type": "html",
  "title": "Startup Landing Page",
  "content": "<html>...</html>"
}
```

The frontend sends the artifact content to the Artifact Viewer.

---

# 9. Agentic Routing Logic

The application uses an Agent Router to determine which skill should handle the user's request.

The router receives:

* User message
* Conversation history
* Optional retrieved context

The router identifies the user's intent.

```text
                         User Message
                              │
                              ▼
                       Agent Router
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
          Q&A Intent      Essay Intent    Artifact Intent
              │               │               │
              ▼               ▼               ▼
          Q&A Skill       Essay Skill     Artifact Skill
```

---

# 10. Q&A Skill

The Q&A Skill is responsible for answering product management and growth questions.

Example:

```text
How do successful startups achieve product-market fit?
```

The workflow is:

```text
User Question
      ↓
Agent Router
      ↓
Q&A Skill
      ↓
Generate Query Embedding
      ↓
Search Knowledge Base
      ↓
Retrieve Relevant Transcript Chunks
      ↓
Build Grounded Prompt
      ↓
Send to LLM
      ↓
Generate Answer
```

The LLM is instructed to use the retrieved transcript context as the primary source.

If the retrieved context does not contain enough evidence, the assistant should communicate that sufficient evidence was not found.

---

# 11. Essay Skill

The Essay Skill handles long-form content requests.

Example:

```text
Write a 1250-word essay about product-market fit.
```

Workflow:

```text
User Request
      ↓
Agent Router
      ↓
Essay Skill
      ↓
Retrieve Relevant Transcript Context
      ↓
Apply Essay Prompt
      ↓
Generate Structured Content
      ↓
Return Markdown
```

The prompt requires:

* Strong hook
* Approximately 1250 words
* Short paragraphs
* Headings
* Bullet points
* Bold key concepts
* Clear takeaway

---

# 12. Artifact Skill

The Artifact Skill generates:

* HTML
* CSS
* Markdown

Example:

```text
Create a landing page for a startup.
```

Workflow:

```text
User Request
      ↓
Agent Router
      ↓
Artifact Skill
      ↓
Generate Artifact
      ↓
Return Structured Artifact
      ↓
Frontend Artifact Viewer
      ↓
Render Preview
```

The artifact response contains metadata describing the artifact type.

Example:

```json
{
  "type": "html",
  "title": "Startup Landing Page",
  "content": "<html>...</html>"
}
```

---

# 13. Agent Routing Decision

The routing logic can use an LLM-based classification approach or deterministic intent detection.

Conceptually:

```text
if request is a knowledge question:
    use Q&A Skill

elif request asks for long-form essay:
    use Essay Skill

elif request asks for HTML/CSS/Markdown:
    use Artifact Skill

else:
    use Q&A Skill
```

A more advanced implementation can use structured LLM output:

```json
{
  "intent": "qa"
}
```

Possible intent values:

```text
qa
essay
artifact
```

The router then maps the intent to the appropriate skill.

---

# 14. LLM Configuration Architecture

The application uses an LLM abstraction layer.

Instead of directly calling Ollama from every agent, all LLM calls go through the LLM configuration module.

```text
Agent / Skill
      │
      ▼
LLM Configuration Layer
      │
      ├───────────────┐
      │               │
      ▼               ▼
   Ollama         Cloud Provider
   Local LLM
```

This allows the underlying LLM to be changed without modifying the agent logic.

---

# 15. LLM Toggle Switch

The application supports two LLM modes.

## Mode 1: Local Ollama

This is the mandatory mode for the local demo.

Example configuration:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

The application sends requests to the local Ollama server.

```text
Application
    ↓
LLM Configuration
    ↓
Provider = Ollama
    ↓
Ollama API
    ↓
Local Model
    ↓
Response
```

---

## Mode 2: Cloud LLM

The application can optionally use a cloud provider.

Example:

```env
LLM_PROVIDER=cloud
CLOUD_API_KEY=your_api_key
CLOUD_MODEL=your_model
```

The application then routes LLM requests to the configured cloud provider.

```text
Application
    ↓
LLM Configuration
    ↓
Provider = Cloud
    ↓
Cloud API
    ↓
Cloud Model
    ↓
Response
```

---

# 16. LLM Provider Selection

The provider selection is controlled through an environment variable.

```text
LLM_PROVIDER
      │
      ├── ollama
      │      ↓
      │   Local Model
      │
      └── cloud
             ↓
         Cloud Model
```

Example implementation logic:

```python
if provider == "ollama":
    llm = OllamaLLM(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL
    )

elif provider == "cloud":
    llm = CloudLLM(
        api_key=CLOUD_API_KEY,
        model=CLOUD_MODEL
    )
```

The rest of the application communicates with the selected LLM through a common interface.

This keeps the agent and skill implementations independent from the underlying model provider.

---

# 17. Runtime LLM Toggle

If the frontend provides a model/provider selector, the user can select the preferred provider.

Example:

```text
┌─────────────────────────────┐
│ LLM Provider                │
│                             │
│ ● Ollama (Local)            │
│ ○ Cloud LLM                 │
│                             │
│ Model: llama3.2             │
│                             │
│          [ Save ]           │
└─────────────────────────────┘
```

The selected configuration is sent to the backend.

The backend validates the selected provider and uses the corresponding LLM implementation.

For the required local demo, Ollama is the default configuration.

---

# 18. RAG Architecture

The RAG system uses Lenny's Podcast transcripts as the knowledge source.

```text
Lenny's Podcast Transcripts
          ↓
     Data Ingestion
          ↓
      Text Cleaning
          ↓
        Chunking
          ↓
       Embedding
          ↓
    Vector Storage
          ↓
     User Question
          ↓
     Query Embedding
          ↓
    Similarity Search
          ↓
 Relevant Transcript Chunks
          ↓
    Prompt Construction
          ↓
          LLM
          ↓
    Grounded Response
```

The RAG pipeline is primarily used by the Q&A Skill and can also provide context to the Essay Skill.

---

# 19. Artifact Viewer Architecture

The Artifact Viewer is implemented inside the frontend.

The backend generates a structured artifact response.

```text
Backend
   │
   │ Artifact JSON
   ▼
Frontend
   │
   ├── type = html
   │       ↓
   │    HTML Preview
   │
   ├── type = markdown
   │       ↓
   │    Markdown Renderer
   │
   └── type = code
           ↓
       Code Viewer
```

The Artifact Viewer contains:

* Preview tab
* Code tab
* Markdown tab where applicable

HTML artifacts should be rendered using an isolated/sandboxed environment where appropriate.

---

# 20. End-to-End Request Flow

The complete request lifecycle is:

```text
User
 │
 │ Question
 ▼
Frontend
 │
 │ POST /chat
 ▼
FastAPI
 │
 ▼
Load Session
 │
 ▼
Load Conversation History
 │
 ▼
Agent Router
 │
 ├───────────────┬────────────────┐
 │               │                │
 ▼               ▼                ▼
Q&A            Essay           Artifact
 │               │                │
 ▼               ▼                ▼
RAG           Context         Generation
 │               │                │
 └───────────────┴────────────────┘
                 │
                 ▼
        LLM Configuration Layer
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
       Ollama        Cloud LLM
          │             │
          └──────┬──────┘
                 ▼
            AI Response
                 │
                 ▼
          Save to PostgreSQL
                 │
                 ▼
         Return to Frontend
                 │
                 ▼
           Display Result
                 │
                 ▼
        Artifact Viewer if needed
```

---

# 21. Error Handling Architecture

The application handles failures at multiple levels.

## Ollama Failure

If Ollama is unavailable:

```text
Ollama Connection Failed
        ↓
Catch Exception
        ↓
Return HTTP 503
        ↓
Display User-Friendly Message
```

Example:

```text
The local AI model is unavailable.
Please make sure Ollama is running.
```

---

## Database Failure

If PostgreSQL is unavailable:

```text
Database Error
      ↓
Catch Exception
      ↓
Log Error
      ↓
Return Appropriate Response
```

---

## Invalid Session

If a session ID does not exist:

```text
Invalid Session ID
      ↓
Return HTTP 404
      ↓
Display Session Not Found
```

---

## Missing Configuration

If required environment variables are missing:

```text
Missing Environment Variable
      ↓
Configuration Validation
      ↓
Return Clear Error
```

---

# 22. Security Considerations

The application follows basic security practices.

### Environment Variables

Sensitive values are stored in `.env`.

```text
.env
```

The `.env` file is excluded from Git.

### API Keys

API keys are never hardcoded.

### Database Credentials

Database credentials are loaded through environment variables.

### Artifact Rendering

Generated HTML and JavaScript are treated as untrusted content.

Artifact rendering should use sandboxing where appropriate.

---

# 23. Deployment Architecture

The application is primarily designed for local evaluation.

The expected local architecture is:

```text
Local Machine
│
├── Frontend
│
├── FastAPI Backend
│
├── Ollama
│     └── Local LLM
│
└── Internet
      │
      ▼
   Supabase
      │
      └── PostgreSQL
```

The evaluator can run the frontend, backend, and Ollama locally while using a PostgreSQL database hosted through Supabase or Railway.

No full cloud deployment is required for the local demo unless separately configured.

---

# 24. Architecture Decisions

## Why FastAPI?

FastAPI provides:

* High-performance APIs
* Automatic API documentation
* Easy integration with Python AI libraries
* Async support
* Simple development workflow

## Why PostgreSQL?

PostgreSQL provides reliable persistent storage for:

* Sessions
* Messages
* User metadata

## Why Ollama?

Ollama allows the application to run a local LLM without depending entirely on cloud APIs.

This satisfies the local demo requirement.

## Why Agent Routing?

Agent routing separates different user intents and allows specialized skills to handle different tasks.

## Why RAG?

RAG allows the assistant to ground responses in Lenny's Podcast transcript knowledge rather than relying only on the model's general knowledge.

## Why Artifact Viewer?

The Artifact Viewer turns AI-generated code into a visual, interactive output and creates a more immersive AI workspace.

---

# 25. Future Architecture Improvements

Future versions may include:

* Dedicated vector database such as Qdrant or Pinecone.
* Redis for session caching.
* Background workers for transcript ingestion.
* Streaming LLM responses.
* Authentication.
* Multi-user access control.
* Agent execution tracing.
* Advanced tool calling.
* Automated evaluation of RAG grounding.
* Cloud deployment with containerization.
* CI/CD pipeline.

---

# 26. Summary

The Lenny Growth Assistant uses a modular architecture that combines:

```text
FastAPI
   +
Agent Router
   +
Specialized Skills
   +
RAG
   +
Ollama / Cloud LLM
   +
PostgreSQL
   +
Artifact Viewer
```

The architecture is designed to provide:

* Grounded conversational Q&A.
* Independent chat sessions.
* Agentic skill routing.
* Ship30for30-style content generation.
* HTML/CSS/Markdown artifact generation.
* Integrated artifact visualization.
* Local LLM execution.
* Configurable cloud LLM support.
* Persistent PostgreSQL storage.

The core architectural principle is:

> **Use a modular agentic layer to route user intent to specialized skills, ground knowledge-based responses using RAG, and abstract the LLM provider behind a configurable interface.**
