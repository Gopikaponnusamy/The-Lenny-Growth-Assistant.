# UI/UX Design Document

# The Lenny Growth Assistant

## 1. Design Overview

The Lenny Growth Assistant is designed as a modern, AI-first conversational workspace inspired by products such as ChatGPT and Claude.

The primary goal of the interface is to make it easy for users to:

* Ask questions about product management and startup growth.
* Continue conversations within independent chat sessions.
* Generate long-form essays.
* Generate Markdown, HTML, and CSS artifacts.
* View generated artifacts directly inside the application.
* Switch between different LLM configurations.
* Understand how the AI arrived at its response through relevant transcript context.

The design focuses on **simplicity, clarity, speed, and usability**.

The interface should feel like a professional AI productivity tool rather than a traditional chatbot.

---

# 2. Design Principles

The application follows the following core design principles.

## 2.1 Simple

The user should be able to open the application and immediately understand how to start.

The main action should be:

> Ask a question.

The interface should avoid unnecessary buttons, menus, and configuration options.

---

## 2.2 Conversational

The chat is the primary interaction model.

Users communicate naturally with the AI instead of navigating through complicated forms.

Example:

```text
User:
How do successful startups achieve product-market fit?

AI:
Based on insights from Lenny's Podcast transcripts...
```

---

## 2.3 Context-Aware

Each conversation belongs to a specific chat session.

When users create a new chat, the previous conversation context should not be mixed with the new conversation.

This creates a familiar experience similar to ChatGPT.

---

## 2.4 Artifact-First Experience

When the AI generates an artifact, the application should not simply display raw code.

The generated artifact should be displayed in a dedicated Artifact Viewer.

For example:

```text
┌──────────────────────────────────────────────────────┐
│                    Lenny Growth Assistant            │
├──────────────────┬───────────────────────────────────┤
│                  │                                   │
│  Chat            │       Artifact Viewer             │
│                  │                                   │
│  User:           │   ┌───────────────────────────┐   │
│  Create a        │   │                           │   │
│  startup         │   │     Rendered Website      │   │
│  landing page.   │   │                           │   │
│                  │   │     [Get Started]          │   │
│  AI:             │   │                           │   │
│  I created the   │   └───────────────────────────┘   │
│  landing page.   │                                   │
│                  │                                   │
└──────────────────┴───────────────────────────────────┘
```

This allows users to interact with the generated output immediately.

---

# 3. Target Users

The primary users of the application are:

* Product managers
* Startup founders
* Growth professionals
* Students
* AI and product enthusiasts
* Researchers interested in product management and growth

The interface should support both technical and non-technical users.

---

# 4. Information Architecture

The application is organized into five primary areas.

```text
Application
│
├── Sidebar
│   ├── New Chat
│   ├── Chat History
│   └── Settings
│
├── Main Chat Area
│   ├── User Messages
│   ├── AI Responses
│   ├── Markdown Content
│   └── Code Blocks
│
├── Input Area
│   ├── Message Input
│   ├── Send Button
│   └── Artifact Generation
│
├── Artifact Viewer
│   ├── Preview
│   ├── Markdown View
│   └── Code View
│
└── Settings
    ├── LLM Provider
    └── Model Configuration
```

---

# 5. Main Application Layout

The primary desktop layout uses a three-section structure.

```text
┌──────────────────────────────────────────────────────────────┐
│                    Lenny Growth Assistant                    │
├──────────────┬──────────────────────────┬────────────────────┤
│              │                          │                    │
│   Sidebar    │       Chat Area          │  Artifact Viewer   │
│              │                          │                    │
│ + New Chat   │                          │                    │
│              │      Messages            │                    │
│ Chat 1       │                          │    Preview         │
│ Chat 2       │                          │                    │
│ Chat 3       │                          │                    │
│              │                          │                    │
│              │                          │                    │
│              ├──────────────────────────┤                    │
│              │      Message Input       │                    │
│              │  [ Ask anything... ]     │                    │
│              └──────────────────────────┘                    │
└──────────────┴──────────────────────────┴────────────────────┘
```

The Artifact Viewer can be opened or closed depending on whether an artifact is available.

When no artifact exists, the chat area can use the available screen width.

---

# 6. Sidebar Design

The sidebar provides navigation and session management.

## Components

### New Chat Button

The most prominent action in the sidebar.

Example:

```text
+ New Chat
```

When clicked:

1. A new session is created.
2. A unique session ID is generated.
3. The conversation context is reset.
4. The new session is added to chat history.

---

### Chat History

Previous conversations are displayed in chronological order.

Example:

```text
Recent Chats

Product-Market Fit
Growth Strategies
Startup Ideas
User Research
```

Clicking a previous chat loads its conversation history.

---

### Active Session

The current chat should be visually distinguishable from inactive sessions.

The active session should have:

* Clear visual highlighting
* Stronger text contrast
* Optional active indicator

---

# 7. Chat Interface

The chat interface is the core of the application.

Messages are displayed in a clean conversational format.

Example:

```text
┌─────────────────────────────────────────────┐
│ You                                         │
│ How do startups achieve product-market fit? │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Lenny Growth Assistant                      │
│                                             │
│ Based on insights from Lenny's Podcast,     │
│ successful startups often focus on...       │
│                                             │
│ Sources: Transcript Context                 │
└─────────────────────────────────────────────┘
```

AI responses should support:

* Markdown
* Headings
* Bold text
* Bullet points
* Numbered lists
* Code blocks
* Links where appropriate

Long answers should be visually structured for easy scanning.

---

# 8. Message Input

The input area should remain easily accessible.

Example:

```text
┌───────────────────────────────────────────────┐
│ Ask about product, growth, or create an       │
│ artifact...                                   │
│                                               │
│                                  [ Send ]      │
└───────────────────────────────────────────────┘
```

The input should:

* Support multi-line text.
* Submit using the Send button.
* Support Enter to send.
* Support Shift + Enter for a new line.
* Disable sending while an empty message is entered.
* Show a loading state while the AI is responding.

---

# 9. Loading and Streaming States

The interface should clearly communicate that the AI is processing a request.

Example:

```text
Lenny Growth Assistant is thinking...
```

A typing indicator can be displayed.

For longer responses, streaming output can be used so that users see the answer progressively instead of waiting for the entire response.

---

# 10. Skill-Based User Experience

The application has different AI capabilities.

The user does not necessarily need to manually select a skill.

The agent can automatically determine the appropriate workflow.

```text
User Request
      │
      ▼
Agent Router
      │
      ├── Q&A
      │
      ├── Essay Generation
      │
      └── Artifact Generation
```

Examples:

### Q&A

```text
How do startups achieve product-market fit?
```

The system uses the Q&A skill and RAG retrieval.

### Essay

```text
Write a 1250-word essay about product-market fit.
```

The system uses the content generation skill.

### Artifact

```text
Create a landing page for a SaaS startup.
```

The system uses the artifact generation skill.

This reduces cognitive load for the user.

---

# 11. Artifact Viewer

The Artifact Viewer is a key differentiating feature.

It appears when the AI generates an artifact.

The viewer supports three modes:

```text
┌──────────┬──────────┬──────────┐
│ Preview  │  Code    │ Markdown │
└──────────┴──────────┴──────────┘
```

## Preview

Displays the actual rendered HTML/CSS artifact.

Example:

```text
┌───────────────────────────────┐
│        SaaS Product           │
│                               │
│  Build your product faster.   │
│                               │
│       [ Get Started ]         │
└───────────────────────────────┘
```

## Code

Displays the generated HTML/CSS source code with syntax highlighting.

## Markdown

Displays generated Markdown as a styled document.

---

# 12. Artifact Viewer Safety

Generated HTML should be rendered safely.

The application should use an isolated rendering environment such as a sandboxed iframe where appropriate.

The Artifact Viewer should prevent generated code from accessing sensitive application data.

The application should treat AI-generated HTML and JavaScript as untrusted content.

---

# 13. Ship30for30 Essay Experience

When an essay is generated, it should be optimized for readability.

The output should contain:

* A strong hook
* Short paragraphs
* Clear headings
* Bold key ideas
* Bullet points
* Practical examples
* A clear final takeaway

Example structure:

```text
# The Real Secret Behind Product-Market Fit

Strong opening hook...

## The Problem

...

## What Successful Startups Do Differently

- Point 1
- Point 2
- Point 3

## The Practical Framework

...

## The Takeaway

...
```

This makes long-form content easier to read and scan.

---

# 14. LLM Configuration UI

The application supports local and cloud LLM configurations.

The settings area can provide a simple configuration interface.

Example:

```text
LLM Provider

(●) Ollama
( ) Cloud LLM

Model

[ llama3.2          ▼ ]

             [ Save ]
```

The local Ollama configuration is the default option for the demo.

Cloud configuration can be enabled when valid credentials are available.

API keys should never be displayed in plain text or committed to the repository.

---

# 15. Visual Design

The visual language should be minimal and professional.

The application should use:

* Clean typography
* Rounded cards
* Subtle borders
* Clear spacing
* Consistent alignment
* Minimal visual noise
* Strong hierarchy

The design should prioritize content over decoration.

The interface should feel like a modern AI workspace.

---

# 16. Color and Typography

The application should use a neutral base palette.

Recommended approach:

* Neutral background
* High-contrast primary text
* Muted secondary text
* One accent color for primary actions
* Subtle borders for separation

Typography should prioritize readability.

Recommended hierarchy:

```text
Page Title
    ↓
Section Heading
    ↓
Subheading
    ↓
Body Text
    ↓
Supporting Text
```

The font should be modern and highly readable.

---

# 17. Responsive Design

The application should work across different screen sizes.

### Desktop

Use a three-column or two-panel layout:

```text
Sidebar | Chat | Artifact Viewer
```

### Tablet

Use:

```text
Sidebar | Chat
```

The Artifact Viewer can open as a panel.

### Mobile

Use a single-column layout:

```text
Chat
```

The sidebar and Artifact Viewer can open as overlays or drawers.

---

# 18. Empty State

When a new chat is opened, the user should see a helpful empty state.

Example:

```text
        Welcome to Lenny Growth Assistant

    Ask questions about product, growth, and startups.

    Try asking:

    "How do startups find product-market fit?"

    "What are effective growth strategies?"

    "Write an essay about user research."

    "Create a startup landing page."
```

The examples should be clickable where possible.

---

# 19. Error States

Errors should be communicated clearly without exposing technical stack traces.

### Ollama unavailable

```text
Unable to connect to the local AI model.

Please make sure Ollama is running and try again.
```

### Database unavailable

```text
We couldn't save your conversation.

Please check your connection and try again.
```

### No relevant transcript evidence

```text
I couldn't find sufficient evidence in the available
Lenny's Podcast transcripts to answer this question.
```

This is especially important for maintaining trust in the RAG-based Q&A experience.

---

# 20. Accessibility

The interface should follow basic accessibility principles.

The application should provide:

* Sufficient text contrast
* Keyboard navigation
* Visible focus states
* Descriptive button labels
* Accessible form inputs
* Proper heading hierarchy
* Responsive text sizing

Interactive elements should have clear visual states for:

* Hover
* Focus
* Active
* Disabled
* Loading

---

# 21. UX Flow

The primary user journey is:

```text
Open Application
       ↓
Create New Chat
       ↓
Ask Question
       ↓
Agent Identifies Request
       ↓
Select Appropriate Skill
       ↓
Retrieve Transcript Context
       ↓
Generate Response
       ↓
Display Response
       ↓
Save Conversation
```

For artifact generation:

```text
User Requests Artifact
       ↓
Agent Selects Artifact Skill
       ↓
Generate HTML/CSS/Markdown
       ↓
Return Artifact
       ↓
Open Artifact Viewer
       ↓
Render Preview
```

---

# 22. Design Goals

The final product should achieve the following:

1. **Easy to understand** within the first few seconds.
2. **Fast to interact with** through a simple chat interface.
3. **Reliable** through transcript-grounded responses.
4. **Powerful** through multiple AI skills.
5. **Visual** through the integrated Artifact Viewer.
6. **Professional** through consistent UI design.
7. **Accessible** to both technical and non-technical users.

The goal is to create an AI workspace where users can move naturally from:

> **Question → Research → Insight → Content → Artifact**

without leaving the application.
