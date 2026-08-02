# 🧠 Lenny Growth Assistant

An AI-powered conversational assistant that provides insights and answers based on Lenny's Podcast transcripts using **Retrieval-Augmented Generation (RAG)**.

## 🚀 Features

* 💬 Ask questions about product management, startups, and growth
* 🔍 Retrieves relevant information from podcast transcripts
* 🤖 Generates context-aware answers using an LLM
* 📚 Uses RAG to ground responses in available source data
* 🌐 Simple web-based chat interface
* ⚡ FastAPI backend for API communication

## 🛠️ Technologies Used

* Python
* FastAPI
* RAG (Retrieval-Augmented Generation)
* Large Language Models (LLMs)
* NLP
* HTML, CSS, JavaScript
* SQLite

## 📁 Project Structure

```text
Lenny-Growth-Assistant/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── rag.py
│   ├── llm.py
│   ├── agent.py
│   └── prompts.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── transcripts/
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Lenny-Growth-Assistant.git
cd Lenny-Growth-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 5. Open the Frontend

Open the `frontend/index.html` file in your browser or use the **Live Server** extension in VS Code.

## 💡 Example Questions

* How do I start a business?
* How can I achieve product-market fit?
* What are the best growth strategies for startups?
* How should I build a successful product?
* How can I improve user retention?

## 🎯 Project Goal

The goal of this project is to demonstrate how **RAG and LLM technologies** can be used to build an AI-powered knowledge assistant that allows users to easily access and interact with insights from a large collection of podcast transcripts.

## 👩‍💻 Author

**Gopika P**
M.Sc Data Science
