# Product Requirements Document (PRD)

# The Lenny Growth Assistant

**Version:** 1.0
**Status:** Final
**Project Type:** Full-Stack Agentic AI Application
**Target:** Agentic AI Engineer Intern Take-Home Assignment

---

# 1. Product Overview

## 1.1 Product Name

**The Lenny Growth Assistant**

## 1.2 Product Description

The Lenny Growth Assistant is a full-stack, AI-powered conversational application that allows users to interact with knowledge extracted from Lenny's Podcast transcripts.

The application provides a ChatGPT-like conversational experience where users can:

* Ask product management and startup growth questions.
* Receive answers grounded in Lenny's Podcast transcript knowledge.
* Generate long-form essays in a Ship30for30-inspired format.
* Generate Markdown documents.
* Generate HTML/CSS artifacts.
* Preview generated artifacts directly inside the application.
* Create and manage multiple independent chat sessions.
* Switch between a local Ollama LLM and a configurable cloud LLM.

The product combines **RAG, agentic routing, specialized skills, FastAPI, PostgreSQL, Ollama, and an interactive frontend** into a single AI workspace.

---

# 2. Problem Statement

Product managers, startup founders, and students often consume large amounts of podcast and written content to learn about product development and growth.

However, finding specific insights from long-form podcast transcripts is difficult.

Users currently need to:

1. Search through large transcript collections.
2. Read multiple episodes.
3. Identify relevant insights.
4. Compare ideas across different conversations.
5. Convert insights into useful written content.
6. Create separate documents or UI artifacts manually.

This process is time-consuming and fragmented.

The Lenny Growth Assistant solves this problem by creating a conversational interface over the transcript knowledge base.

Instead of manually searching through transcripts, users can ask:

> "How do successful startups achieve product-market fit?"

The system retrieves relevant transcript context and generates a grounded response.

Users can then continue by asking:

> "Turn this into a 1250-word essay."

or:

> "Create a landing page based on these ideas."

This creates a continuous workflow:

```text
Research
   ↓
Ask
   ↓
Understand
   ↓
Generate Content
   ↓
Create Artifact
   ↓
Preview
```

---

# 3. Product Vision

The vision is to build an AI-powered knowledge workspace that transforms Lenny's Podcast content from a static transcript collection into an interactive product and growth knowledge assistant.

The application should feel like:

> **ChatGPT + RAG + Agent Skills + Claude Artifacts**

The user should be able to move from a question to a useful output without leaving the application.

---

# 4. Goals

## Primary Goals

### Goal 1: Transcript-Grounded Q&A

Enable users to ask product management and startup growth questions and receive answers grounded strictly in the available Lenny's Podcast transcript knowledge.

---

### Goal 2: Agentic Skill Routing

Build an agentic system that identifies the user's intent and selects the appropriate skill.

The initial skills are:

* Q&A Skill
* Ship30for30 Essay Skill
* Artifact Generation Skill

---

### Goal 3: Persistent Conversations

Allow users to create multiple independent chat sessions.

Each session should maintain its own conversation history.

---

### Goal 4: Artifact Generation

Allow users to generate:

* Markdown
* HTML
* CSS
* HTML/CSS web components

The artifacts should be displayed in an integrated Artifact Viewer.

---

### Goal 5: Local LLM Support

The application must run locally using Ollama.

This allows evaluators to test the application without depending on a paid cloud LLM.

---

### Goal 6: Configurable LLM Architecture

The application should support switching between:

* Local Ollama models
* Cloud LLM providers

The LLM provider should be configurable through environment variables.

---

### Goal 7: Professional User Experience

Build a modern, responsive, ChatGPT-like interface with:

* Chat history
* New Chat functionality
* Markdown rendering
* Code rendering
* Artifact Viewer
* Loading states
* Error states

---

# 5. Non-Goals

The following features are outside the initial scope.

* Full user authentication and OAuth.
* Mobile native applications.
* Real-time multi-user collaboration.
* Voice input.
* Voice output.
* Training a custom foundation model.
* Building a new vector database from scratch.
* Automatic podcast transcription.
* Full cloud production deployment.
* Enterprise-level identity management.

These may be considered future improvements.

---

# 6. Target Users

## Primary Users

### Product Managers

Users who want to quickly find product management insights from Lenny's Podcast.

### Startup Founders

Users looking for advice related to:

* Product-market fit
* Growth
* User acquisition
* Hiring
* Product strategy

### Students

Students learning product management, startups, and growth.

### AI/Product Researchers

Users interested in exploring product and growth knowledge through conversational AI.

---

# 7. User Stories

## User Story 1: Ask a Question

As a user,

I want to ask a product or growth question,

so that I can quickly understand relevant insights from Lenny's Podcast.

### Example

```text
How do successful startups achieve product-market fit?
```

### Expected Result

The system retrieves relevant transcript context and provides a grounded answer.

---

## User Story 2: Start a New Chat

As a user,

I want to start a new chat,

so that I can begin a fresh conversation without previous context.

### Expected Result

A new session is created with a unique session ID.

---

## User Story 3: Continue a Conversation

As a user,

I want to ask follow-up questions,

so that the AI understands the context of my current conversation.

### Expected Result

The system uses the current session's conversation history.

---

## User Story 4: Generate an Essay

As a user,

I want to convert insights into a long-form essay,

so that I can consume or reuse the information in a structured format.

### Example

```text
Write a 1250-word essay about product-market fit.
```

### Expected Result

The Ship30for30 Skill generates a structured essay with:

* Strong hook
* Headings
* Bullet points
* Bold text
* Practical insights
* Clear takeaway

---

## User Story 5: Generate an Artifact

As a user,

I want to ask the AI to create a webpage,

so that I can see the generated result immediately.

### Example

```text
Create a landing page for a startup.
```

### Expected Result

The AI generates HTML/CSS and the Artifact Viewer displays the rendered page.

---

## User Story 6: Use Local AI

As an evaluator,

I want to run the application using Ollama,

so that I can test the application locally without requiring a cloud LLM.

---

# 8. Functional Requirements

## FR-01: Chat Sessions

The system must allow users to:

* Create a new chat.
* View previous chats.
* Open an existing chat.
* Continue a conversation.
* Maintain independent session contexts.

---

## FR-02: Conversation Persistence

The system must store:

* Session ID
* User metadata
* User messages
* Assistant messages
* Timestamps

The data must persist in PostgreSQL.

---

## FR-03: Transcript Knowledge Base

The system must ingest transcripts from:

```text
https://github.com/ChatPRD/lennys-podcast-transcripts
```

The ingestion pipeline should:

1. Load transcript files.
2. Clean text.
3. Split text into chunks.
4. Generate embeddings.
5. Store searchable representations.

---

## FR-04: RAG Question Answering

When a user asks a question:

1. Receive the user query.
2. Identify it as a Q&A request.
3. Search the knowledge base.
4. Retrieve relevant transcript chunks.
5. Build an LLM prompt.
6. Generate an answer.
7. Return the answer to the user.
8. Save the conversation.

The system should not invent information when sufficient transcript evidence is unavailable.

---

## FR-05: Agent Routing

The agent router should classify user requests.

Example:

```text
User Request
      │
      ▼
Agent Router
      │
      ├── Q&A
      │
      ├── Essay
      │
      └── Artifact
```

The routing decision can be based on:

* User intent
* Request keywords
* LLM classification
* Structured tool/skill selection

---

## FR-06: Ship30for30 Skill

The application must provide a dedicated skill for long-form content generation.

The skill should:

* Use relevant transcript context.
* Generate approximately 1250 words.
* Start with a strong hook.
* Use headings.
* Use bullet points.
* Use bold text for important concepts.
* End with a clear takeaway.

---

## FR-07: Artifact Skill

The artifact skill should support:

* Markdown generation.
* HTML generation.
* CSS generation.
* HTML/CSS combinations.

The artifact should be returned in a structured format.

Example:

```json
{
  "type": "html",
  "title": "Startup Landing Page",
  "content": "<html>...</html>"
}
```

---

## FR-08: Artifact Viewer

The frontend must display generated artifacts within the application.

The viewer should support:

* HTML Preview
* Markdown Preview
* Code View

The user should not need to open an external application.

---

## FR-09: LLM Configuration

The system must support:

```text
Local LLM
   ↓
Ollama
```

and optionally:

```text
Cloud LLM
   ↓
Cloud Provider
```

The provider should be selected through configuration.

---

## FR-10: Error Handling

The system must handle:

* Missing API keys.
* Ollama unavailable.
* Invalid model.
* Database connection failure.
* Invalid session ID.
* Empty user message.
* Knowledge base retrieval failure.

Errors should be displayed in user-friendly language.

---

# 9. Non-Functional Requirements

## Performance

The application should provide responses within a reasonable time depending on the selected LLM.

## Reliability

The application should not crash when external dependencies fail.

## Security

API keys must not be committed to GitHub.

Sensitive configuration must be stored in `.env`.

## Maintainability

The backend should separate:

* API routes
* Database logic
* Agent logic
* RAG logic
* LLM configuration
* Prompt templates

## Scalability

The architecture should allow additional skills and LLM providers to be added later.

---

# 10. Agentic Architecture

The system uses a central agent router.

```text
                         User
                          │
                          ▼
                    FastAPI API
                          │
                          ▼
                   Agent Router
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
          Q&A Skill   Essay Skill  Artifact Skill
             │            │            │
             ▼            ▼            ▼
            RAG       Transcript    HTML/CSS/
          Retrieval     Context      Markdown
             │            │            │
             └────────────┼────────────┘
                          ▼
                         LLM
                          │
                          ▼
                    Final Response
```

---

# 11. Technical Architecture

## Frontend

The frontend provides:

* Chat interface
* Session sidebar
* New Chat functionality
* Artifact Viewer
* Settings

## Backend

FastAPI handles:

* API requests
* Session management
* Agent routing
* LLM interaction
* RAG retrieval
* Artifact generation

## Database

PostgreSQL stores:

* Users
* Sessions
* Messages

## Knowledge Base

The knowledge base contains processed Lenny's Podcast transcripts.

## LLM

The application supports:

* Ollama for local execution
* Configurable cloud provider

---

# 12. Database Requirements

The database contains three primary entities.

## Users

```text
id
name
email
created_at
```

## Sessions

```text
id
user_id
title
created_at
updated_at
```

## Messages

```text
id
session_id
role
content
created_at
```

Relationship:

```text
User
 │
 └── Sessions
       │
       └── Messages
```

---

# 13. API Requirements

The backend should expose endpoints similar to:

```text
GET    /
GET    /health

POST   /sessions
GET    /sessions
GET    /sessions/{session_id}

POST   /chat
GET    /messages/{session_id}

POST   /artifact
```

The exact endpoint implementation may vary.

---

# 14. User Experience Requirements

The application should feel similar to modern AI assistants.

The primary layout should contain:

```text
┌────────────┬───────────────────────┬────────────────┐
│ Chat       │ Conversation          │ Artifact       │
│ History    │                       │ Viewer         │
│            │                       │                │
│ New Chat   │ User Message          │ Preview        │
│            │ AI Response           │                │
│ Chat 1     │                       │ Code           │
│ Chat 2     │                       │ Markdown       │
│ Chat 3     │                       │                │
│            │ Input                 │                │
└────────────┴───────────────────────┴────────────────┘
```

The Artifact Viewer should be optional and appear when an artifact is generated.

---

# 15. Success Metrics

The project will be considered successful when:

### Knowledge Grounding

The assistant answers questions using relevant transcript context.

### Session Management

Users can create and continue independent conversations.

### Agent Routing

The correct skill is selected for Q&A, essay, and artifact requests.

### Content Quality

Generated essays follow the required structure and approximate length.

### Artifact Quality

Generated HTML/CSS renders correctly inside the Artifact Viewer.

### Local Execution

The entire application can be run locally using Ollama.

### Documentation

An evaluator can understand and run the application using the README.

---

# 16. Development Plan

The application will be developed in incremental stages.

## Phase 1: Project Setup

* Create repository.
* Set up FastAPI.
* Set up frontend.
* Configure environment variables.
* Set up PostgreSQL.

---

## Phase 2: Database

* Create database models.
* Create sessions table.
* Create messages table.
* Implement database connection.

---

## Phase 3: Knowledge Base

* Download transcripts.
* Process transcripts.
* Implement chunking.
* Implement embeddings.
* Implement retrieval.

---

## Phase 4: Q&A Skill

* Create Q&A prompts.
* Connect RAG retrieval.
* Connect LLM.
* Implement grounded responses.

---

## Phase 5: Agent Router

* Implement request classification.
* Add Q&A skill.
* Add Essay skill.
* Add Artifact skill.

---

## Phase 6: Essay Skill

* Implement Ship30for30-style prompt.
* Add formatting requirements.
* Test long-form generation.

---

## Phase 7: Artifact Generation

* Implement artifact output format.
* Add HTML/CSS generation.
* Add Markdown generation.

---

## Phase 8: Artifact Viewer

* Build preview panel.
* Add HTML rendering.
* Add Markdown rendering.
* Add code view.

---

## Phase 9: LLM Toggle

* Configure Ollama.
* Add cloud LLM configuration.
* Test provider switching.

---

## Phase 10: Testing

Test:

* New chat.
* Chat persistence.
* Q&A.
* RAG grounding.
* Essay generation.
* Artifact generation.
* Artifact rendering.
* Ollama.
* Error handling.

---

## Phase 11: Documentation

Complete:

* README.md
* design.md
* Architecture documentation
* Agent transcripts/logs

---

## Phase 12: Demo

Record a 2–3 minute demo showing:

1. New Chat
2. Q&A
3. Follow-up question
4. Essay generation
5. Artifact generation
6. Artifact Viewer
7. Local Ollama workflow

---

# 17. Definition of Done

The project is considered complete when:

* [ ] FastAPI backend is working.
* [ ] Frontend chat interface is working.
* [ ] New Chat functionality works.
* [ ] PostgreSQL persistence works.
* [ ] Lenny's Podcast transcripts are ingested.
* [ ] RAG retrieval works.
* [ ] Q&A skill works.
* [ ] Essay skill works.
* [ ] Artifact skill works.
* [ ] Artifact Viewer works.
* [ ] HTML/CSS artifacts render correctly.
* [ ] Markdown artifacts render correctly.
* [ ] Ollama local LLM works.
* [ ] Cloud LLM configuration is available.
* [ ] Environment variables are documented.
* [ ] API errors are handled.
* [ ] README.md is complete.
* [ ] design.md is complete.
* [ ] Agent transcripts are included.
* [ ] Public GitHub repository is ready.
* [ ] Demo video is recorded.
* [ ] Final application is tested locally.

---

# 18. Risks and Mitigations

| Risk                        | Mitigation                           |
| --------------------------- | ------------------------------------ |
| Ollama response is slow     | Use a lightweight model              |
| Poor RAG retrieval          | Improve chunking and retrieval       |
| LLM hallucination           | Require transcript-grounded context  |
| Database connection failure | Add error handling and retries       |
| Invalid generated HTML      | Validate and safely render artifacts |
| Large transcript dataset    | Process transcripts incrementally    |
| Missing API keys            | Validate environment configuration   |
| Context window limitations  | Retrieve only relevant chunks        |

---

# 19. Future Improvements

Future versions may include:

* Authentication
* Multi-user support
* Streaming responses
* Advanced vector database
* Source citations
* Transcript episode metadata
* Episode-level search
* Conversation export
* Artifact editing
* Artifact version history
* Voice interaction
* Cloud deployment
* Automated evaluation of RAG grounding

---

# 20. Final Product Vision

The final product should allow a user to complete the following workflow in one application:

```text
Ask a Question
      ↓
Retrieve Lenny's Podcast Insights
      ↓
Get a Grounded Answer
      ↓
Ask Follow-up Questions
      ↓
Generate a Long-Form Essay
      ↓
Create an HTML/CSS Artifact
      ↓
Preview the Artifact
```

The core product principle is:

> **Turn a large knowledge base into an interactive, agentic workspace that helps users move from learning to creating.**

The Lenny Growth Assistant is successful when users can explore product and growth insights, transform those insights into useful content, and create visual artifacts without leaving the application.
