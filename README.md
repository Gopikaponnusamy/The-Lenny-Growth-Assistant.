# 🚀 The Lenny Growth Assistant

An AI-powered conversational assistant that uses insights from **Lenny's Podcast transcripts** to answer product management and growth questions, generate long-form essays in a Ship30for30-inspired format, and create renderable Markdown and HTML/CSS artifacts.

The application is built as a full-stack system with a **FastAPI backend**, **PostgreSQL database**, **RAG-based knowledge retrieval**, and configurable **Local/Cloud LLM support**.

---

## 📌 Features

### 1. Conversational Q&A

Users can ask product management, startup, and growth-related questions.

The assistant retrieves relevant information from Lenny's Podcast transcripts and generates answers grounded in the available knowledge base.

The system is designed to avoid answering questions using unsupported external knowledge when transcript evidence is unavailable.

---

### 2. New Chat Sessions

Users can create multiple independent conversations.

Each chat session has:

* A unique session ID
* Its own conversation history
* User messages
* Assistant responses
* Timestamps

Starting a new chat creates a new session without mixing context from previous conversations.

---

### 3. Lenny's Podcast Knowledge Base

The application uses transcripts from the following public repository:

https://github.com/ChatPRD/lennys-podcast-transcripts

The transcripts are processed and converted into searchable knowledge chunks.

The RAG pipeline retrieves relevant transcript content based on the user's question.

---

### 4. RAG-Based Question Answering

The Q&A pipeline works as follows:

```text
User Question
      ↓
FastAPI Backend
      ↓
Query Processing
      ↓
Knowledge Base Retrieval
      ↓
Relevant Transcript Chunks
      ↓
LLM Prompt with Retrieved Context
      ↓
Grounded Answer
      ↓
Save Conversation
      ↓
Display in Frontend
```

The assistant uses retrieved transcript content as the primary source for answering questions.

If sufficient evidence is not available in the knowledge base, the assistant should clearly indicate that there is insufficient evidence instead of inventing an answer.

---

### 5. Ship30for30 Content Generation Skill

The application includes a dedicated content-generation skill.

When the user requests an essay or long-form content, the agent routes the request to the content generation skill.

The generated content is structured with:

* A strong opening hook
* Clear sections
* Short paragraphs
* Bullet points
* Bold text for important ideas
* Practical insights
* Clear takeaway

The target output is approximately **1250 words** and is inspired by the requested Ship30for30-style writing format.

---

### 6. Artifact Generation

The assistant can generate artifacts based on the conversation context.

Supported artifact types include:

* Markdown documents
* HTML
* CSS
* Combined HTML/CSS snippets

Examples of user requests:

```text
Create a landing page for a startup.
```

```text
Create a Markdown document summarizing the key growth lessons.
```

```text
Generate an HTML dashboard based on this conversation.
```

---

### 7. Artifact Viewer

Generated artifacts are displayed inside the application using an Artifact Viewer.

Instead of showing only raw code, the frontend can display:

```text
┌──────────────────────┬─────────────────────────┐
│                      │                         │
│      Chat            │     Artifact Viewer     │
│                      │                         │
│  User: Create a      │   ┌─────────────────┐   │
│  landing page        │   │                 │   │
│                      │   │  Rendered HTML  │   │
│  AI: Here is your    │   │  / Markdown     │   │
│  artifact...         │   │                 │   │
│                      │   └─────────────────┘   │
│                      │                         │
└──────────────────────┴─────────────────────────┘
```

HTML artifacts are rendered within the application.

Markdown artifacts are converted into a readable, styled document view.

---

# 🏗️ System Architecture

The application follows a modular full-stack architecture.

```text
                    ┌─────────────────────────┐
                    │       User / Browser    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Frontend Application │
                    │    Chat + Artifact UI   │
                    └────────────┬────────────┘
                                 │ HTTP / REST
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend    │
                    │                         │
                    │  Session Management     │
                    │  Agent Router           │
                    │  API Endpoints          │
                    └──────┬─────────┬────────┘
                           │         │
              ┌────────────┘         └─────────────┐
              ▼                                    ▼
    ┌───────────────────┐                ┌─────────────────┐
    │    Agent Router   │                │   PostgreSQL    │
    │                   │                │                 │
    │  Q&A Skill        │                │ Sessions        │
    │  Essay Skill      │                │ Messages        │
    │  Artifact Skill   │                │ User Metadata   │
    └─────────┬─────────┘                └─────────────────┘
              │
              ▼
    ┌───────────────────┐
    │   RAG Pipeline    │
    │                   │
    │ Query Embedding   │
    │ Retrieval         │
    │ Context Building  │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────────────────┐
    │       LLM Configuration       │
    │                               │
    │  Local: Ollama                │
    │  Cloud: Configurable Provider │
    └───────────────────────────────┘
```

---

# 🤖 Agentic Architecture

The application uses an agent routing approach.

The main agent determines the type of request and selects the appropriate skill.

```text
                    User Request
                         │
                         ▼
                  ┌─────────────┐
                  │ Agent Router│
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Q&A Skill      Essay Skill   Artifact Skill
          │              │              │
          ▼              ▼              ▼
        RAG         Ship30for30     HTML/CSS
      Retrieval       Format        Markdown
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                       LLM
                         │
                         ▼
                    Final Output
```

### Q&A Skill

Used for questions about:

* Product management
* Startup growth
* Product-market fit
* User research
* Growth strategies
* Leadership
* Hiring
* Product development

The Q&A skill retrieves relevant transcript context before generating an answer.

---

### Essay Skill

Used when the user requests:

* An essay
* Long-form content
* A detailed article
* Ship30for30-style content

The skill takes the retrieved knowledge and transforms it into a structured long-form essay.

---

### Artifact Skill

Used when the user asks for:

* HTML
* CSS
* Markdown
* UI components
* Web pages
* Documents

The generated artifact is returned to the frontend and displayed in the Artifact Viewer.

---

# 🧠 RAG Pipeline

The Retrieval-Augmented Generation pipeline is responsible for grounding answers in Lenny's Podcast transcripts.

### Step 1: Transcript Collection

Podcast transcripts are collected from the provided public dataset.

### Step 2: Document Processing

The raw transcript files are cleaned and processed.

### Step 3: Chunking

Long transcripts are divided into smaller chunks to improve retrieval accuracy.

### Step 4: Embedding

The transcript chunks are converted into vector representations.

### Step 5: Retrieval

When a user asks a question, the system searches for the most relevant transcript chunks.

### Step 6: Context Injection

The retrieved transcript content is added to the LLM prompt.

### Step 7: Response Generation

The LLM generates a response using the retrieved context.

```text
Transcript Files
      ↓
Text Cleaning
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Search
      ↓
Relevant Context
      ↓
LLM
      ↓
Grounded Response
```

---

# 🗄️ Database Architecture

The application uses PostgreSQL for persistent storage.

The database stores:

* User information
* Chat sessions
* Conversation messages
* Session metadata
* Timestamps

A simplified database structure is:

```text
Users
│
├── id
├── name
├── email
└── created_at

Sessions
│
├── id
├── user_id
├── title
└── created_at

Messages
│
├── id
├── session_id
├── role
├── content
└── created_at
```

Relationship:

```text
User
  │
  └──> Multiple Sessions
              │
              └──> Multiple Messages
```

Each session maintains independent conversation context.

---

# 🔌 API Endpoints

The FastAPI backend exposes REST API endpoints.

| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| `GET`  | `/`                      | Health check              |
| `POST` | `/sessions`              | Create a new chat session |
| `GET`  | `/sessions`              | Get user sessions         |
| `GET`  | `/sessions/{session_id}` | Get session details       |
| `POST` | `/chat`                  | Send a message            |
| `GET`  | `/messages/{session_id}` | Get conversation history  |
| `POST` | `/artifact`              | Generate an artifact      |
| `GET`  | `/health`                | Check backend health      |

The exact endpoints may vary depending on the final implementation.

---

# 🔄 LLM Configuration

The application supports switching between a local LLM and a cloud LLM through environment configuration.

### Local LLM

For the required local demo, the application uses **Ollama**.

Example:

```text
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

### Cloud LLM

A cloud provider can be configured using environment variables.

Example:

```text
LLM_PROVIDER=cloud
CLOUD_API_KEY=your_api_key
CLOUD_MODEL=your_model
```

The application reads the configuration and selects the appropriate LLM provider.

```text
             LLM_PROVIDER
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
      Ollama              Cloud
        │                   │
        ▼                   ▼
   Local Model         Cloud Model
```

API keys are never hardcoded in the source code.

---

# 💻 Local Installation

## Prerequisites

Install the following before running the application:

* Python 3.10+
* Node.js 18+ (if required by the frontend)
* Git
* PostgreSQL / Supabase PostgreSQL database
* Ollama

---

# 1. Clone the Repository

```bash

cd lenny-growth-assistant
```

---

# 2. Create a Python Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Install and Run Ollama

Install Ollama from:

https://ollama.com/

After installation, download a supported local model.

Example:

```bash
ollama pull llama3.2
```

Start Ollama:

```bash
ollama serve
```

The default Ollama API runs at:

```text
http://localhost:11434
```

Keep Ollama running while using the application.

---

# 5. Configure PostgreSQL

Create a PostgreSQL database using either:

* Supabase
* Railway
* Local PostgreSQL

Copy the PostgreSQL connection string.

Example:

```text
postgresql://username:password@host:5432/database
```

---

# 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_postgresql_connection_string

LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

CLOUD_API_KEY=
CLOUD_MODEL=
```

If using a cloud LLM:

```env
LLM_PROVIDER=cloud
CLOUD_API_KEY=your_api_key
CLOUD_MODEL=your_model
```

### Important

Never commit `.env` to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

A `.env.example` file is included in the repository to show the required environment variables without exposing secret keys.

---

# 7. Prepare the Transcript Knowledge Base

Download or clone the Lenny's Podcast transcript dataset:

```bash
git clone https://github.com/ChatPRD/lennys-podcast-transcripts.git
```

Place the transcript files in the configured data directory.

Example:

```text
data/
└── transcripts/
    ├── transcript1.md
    ├── transcript2.md
    └── transcript3.md
```

Run the ingestion script:

```bash
python scripts/ingest.py
```

This processes the transcripts and prepares them for retrieval.

---

# 8. Start the FastAPI Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 9. Start the Frontend

If the frontend uses Node.js:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend URL shown in the terminal.

For example:

```text
http://localhost:5173
```

If the frontend is a simple HTML/CSS/JavaScript application, it can be opened using a local development server.

---

# 🧪 Testing the Application

After starting the backend, frontend, Ollama, and database, test the following workflows.

### Test 1: Create a New Chat

1. Open the application.
2. Click **New Chat**.
3. Send a message.
4. Verify that a new session is created.
5. Send another message.
6. Refresh the page.
7. Verify that the conversation remains available.

---

### Test 2: Transcript Q&A

Example:

```text
How do successful startups achieve product-market fit?
```

The assistant should retrieve relevant transcript context and provide a grounded answer.

---

### Test 3: Insufficient Evidence

Ask a question that is unrelated to the transcript knowledge base.

The assistant should avoid hallucinating and respond that sufficient evidence was not found in the available transcript context.

---

### Test 4: Ship30for30 Essay

Example:

```text
Write a 1250-word essay about product-market fit based on Lenny's Podcast insights.
```

The application should generate a structured essay with:

* Strong hook
* Headings
* Bullet points
* Bold key ideas
* Practical insights
* Clear takeaway

---

### Test 5: Artifact Generation

Example:

```text
Create a landing page for a startup using HTML and CSS.
```

The application should:

1. Generate HTML/CSS.
2. Display the artifact in the Artifact Viewer.
3. Render the actual HTML UI inside the application.

---

# 🛡️ Error Handling

The application handles common runtime errors.

### Missing Environment Variables

The backend should display a clear configuration error if required environment variables are missing.

### Ollama Not Running

If Ollama is unavailable, the application should return an understandable error instead of crashing.

Example:

```text
Unable to connect to Ollama.
Please make sure Ollama is running and the selected model is installed.
```

### Database Connection Failure

If the PostgreSQL database is unavailable, the application should return an appropriate error message.

### Empty User Input

The API validates empty messages before sending them to the agent.

### Invalid Session

If a user sends a message to a non-existent session, the API returns an appropriate error response.

---

# 📁 Project Structure

```text
lenny-growth-assistant/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── agent.py
│   ├── rag.py
│   ├── llm.py
│   └── prompts.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── data/
│   └── transcripts/
│
├── scripts/
│   └── ingest.py
│
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   ├── design.md
│   └── agent-transcripts/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔐 Security

The project follows basic security practices:

* API keys are stored in environment variables.
* `.env` is excluded from Git.
* No secret credentials are committed to the repository.
* Database credentials are not hardcoded.
* User sessions are isolated.
* User-generated HTML artifacts should be rendered safely using appropriate sandboxing where applicable.

---

# 🚀 Future Improvements

Possible future improvements include:

* Streaming responses
* User authentication
* Advanced vector databases
* Better transcript citation and source display
* Conversation title generation
* Multi-agent workflows
* Improved artifact editing
* Cloud deployment
* Automated testing and CI/CD
* Conversation export
* File upload support

---

# 📹 Demo


The demo covers:

1. Starting a new chat
2. Asking a transcript-based Q&A question
3. Generating Ship30for30-style content
4. Generating an artifact
5. Viewing the rendered artifact
6. Switching/configuring the LLM
7. Demonstrating the application workflow

---

# 📚 Knowledge Source

The application uses the following transcript dataset:

Lenny's Podcast Transcripts:

https://github.com/ChatPRD/lennys-podcast-transcripts

---

# 👩‍💻 Author

**Gopika P.**

M.Sc. Data Science
Coimbatore Institute of Technology

Built as part of the **Agentic AI Engineer Intern Take-Home Assignment**.
