# Anu_Telegram_Bot
Telegram Bot with Simple_RAG and LLM

How to run locally:
python Telegram_bot_working.py

Which models and APIs are used:
GPT-4o-mini via OpenAI API
HuggingFace sentence embeddings
FAISS for document retrieval
LangChain Agent for orchestration

LangChain Telegram AI Assistant
  A Telegram AI Assistant powered by LangChain, OpenAI GPT-4o-mini, and FAISS for Retrieval-Augmented Generation (RAG).
  The bot can:
    Answer questions from your uploaded documents.
    Retrieve facts using local embeddings.
    Maintain conversational context.
    Run directly with Python.

Feature	Description:
/ask <query>	Ask any question — the bot answers using GPT-4o-mini and RAG.
/image	Upload an image — the bot describes it (placeholder).
/help	Show available commands and usage info.
Memory	Stores recent chat history per user.
Document RAG	Uses FAISS + HuggingFace embeddings for semantic search.
Extensible	Easily add new commands or tools (e.g., web search, summarization).

Tech Stack
Component	Technology
Language Model (LLM)	OpenAI GPT-4o-mini (via langchain_openai.ChatOpenAI)
Embeddings	HuggingFace sentence-transformers/all-MiniLM-L6-v2
Vector Store	FAISS (for document retrieval)
Bot Framework	python-telegram-bot
LangChain Components	RetrievalQA, LLMChain, AgentType.ZERO_SHOT_REACT_DESCRIPTION
Memory	ConversationBufferMemory

System Design Diagram:

                ┌──────────────────────┐
                │   Telegram User      │
                └──────────┬───────────┘
                           │
                           ▼
                 ┌──────────────────────┐
                 │ python-telegram-bot  │
                 └──────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │       LangChain Agent       │
              │ ── Tool 1: Simple QA        │
              │ ── Tool 2: RAG Search       │
              │ ── Tool 3: Web Search       │
              └──────────┬─────────────────┘
                           │
                           ▼
         ┌────────────────────────────────────────┐
         │    FAISS Vector DB (sample.txt docs)   │
         │  + HuggingFace Embeddings              │
         └────────────────────────────────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │   OpenAI GPT-4o-mini   │
               └────────────────────────┘


Here i attached the Screenshot of the output.

<img width="1920" height="1080" alt="Output" src="https://github.com/user-attachments/assets/e5940a53-e8c0-4503-bfa1-07b3159c8f9a" />

Optional Enhancements:
 Message history awareness — maintain last 3 interactions per user.
 “Source snippets” — show which doc was used in RAG response.

Above 2 optionals enhancements are implemented.
