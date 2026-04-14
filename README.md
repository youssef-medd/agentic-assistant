# AION — Local AI Document Intelligence

**A fully local, privacy-first AI assistant. Zero data egress. Your files never leave your machine.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA%203.2-black?logo=ollama&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)
![License](https://img.shields.io/badge/License-MIT-22863a)

---

## What is AION?

AION is a local AI assistant that lets you chat with your documents — PDFs, text files, and images — using LLaMA 3.2 and LLaVA, all running on your own machine via Ollama. No API keys. No cloud. No data ever sent anywhere.

It uses a RAG (Retrieval-Augmented Generation) pipeline backed by ChromaDB to find the most relevant chunks of your documents before answering, so responses are grounded in your actual content rather than hallucinated.

---

## Features

- **Fully local** — powered by Ollama (LLaMA 3.2 for text, LLaVA for images), zero internet dependency
- **RAG pipeline** — ChromaDB vector store with semantic chunking and cosine similarity search
- **Multimodal** — upload images directly in chat; LLaVA analyzes them with vision understanding
- **Multi-format support** — PDF, TXT, PNG, JPG, JPEG, WEBP
- **Persistent memory** — ChromaDB stores document embeddings across sessions via `nomic-embed-text`
- **Admin dashboard** — built-in Streamlit admin panel to inspect all messages, uploaded files, and searches
- **SQLite activity log** — every message, file upload, and search is recorded locally in `database.db`
- **Debug mode** — toggle extraction details to see chunk counts, scores, and raw context

---

## Tech Stack

| Layer             | Technology                   |
| ----------------- | ---------------------------- |
| UI                | Streamlit                    |
| LLM (text)        | LLaMA 3.2 (3B) via Ollama    |
| LLM (vision)      | LLaVA via Ollama             |
| Embeddings        | nomic-embed-text via Ollama  |
| Vector Store      | ChromaDB (persistent, local) |
| PDF parsing       | pypdf                        |
| Image processing  | Pillow                       |
| Activity database | SQLite                       |
| Language          | Python 3.10+                 |

---

## Project Structure

```
agentic-assistant/
├── app.py                  ← Main Streamlit chat interface
├── admin.py                ← Admin dashboard (messages, files, searches)
├── database.db             ← Local SQLite activity log (auto-created)
├── chroma_db/              ← ChromaDB persistent vector store
├── requirements.txt
├── db/
│   ├── database.py         ← SQLite init, save_message, save_file, save_search
│   └── vector_store.py     ← ChromaDB ingest, query, list, clear
└── modules/
    ├── brain.py            ← Ollama chat wrapper
    ├── multimodal.py       ← Image encoding, LLaVA message builder
    └── parser.py           ← PDF and text extraction pipeline
```

---

## Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repo

```bash
git clone https://github.com/youssef-medd/agentic-assistant.git
cd agentic-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull the required Ollama models

```bash
ollama pull llama3.2
ollama pull llava
ollama pull nomic-embed-text
```

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

### 5. (Optional) Open the admin dashboard

```bash
streamlit run admin.py --server.port 8502
```

Open your browser at **http://localhost:8502**

---

## How It Works

```
User uploads document
        │
        ▼
parser.py extracts text (pypdf / plain text)
        │
        ▼
vector_store.py chunks text → embeds with nomic-embed-text → stores in ChromaDB
        │
        ▼
User sends a question
        │
        ▼
vector_store.py embeds question → cosine similarity search → top-k chunks retrieved
        │
        ▼
Chunks injected as context into LLaMA 3.2 prompt
        │
        ▼
Ollama returns grounded response
        │
        ▼
Response + activity saved to SQLite
```

For image inputs, the pipeline skips ChromaDB and routes directly to LLaVA with base64-encoded image data.

---

## RAG Pipeline Details

- **Chunking:** 400-word chunks with 60-word overlap
- **Embeddings:** `nomic-embed-text` via Ollama
- **Similarity:** cosine distance (HNSW index in ChromaDB)
- **Score threshold:** hits below 0.35 similarity are discarded
- **Top-k retrieval:** 5 chunks per query

---

## Admin Dashboard

The admin panel at `admin.py` shows:

- **Total messages / files / searches** — live metrics
- **Full chat history** — rendered as chat bubbles with timestamps
- **Uploaded files table** — split by images and documents
- **Search log** — all queries made during sessions

---

## Requirements

```
streamlit
ollama
chromadb
pypdf
pillow
pandas
```

---

## License

MIT
