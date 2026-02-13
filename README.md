# Superior Outreach – RAG Chatbot Widget (FastAPI + FAISS + OpenAI)

An embeddable **chatbot widget** powered by **RAG (Retrieval-Augmented Generation)**.  
It crawls content from **superior-outreach.com** using **crawl4ai**, indexes it with **OpenAI embeddings** into a **FAISS** vector store (via **LangChain**), and serves an **answer-only** chat experience embedded into a **WordPress** site via a simple JavaScript include.

**Repo:** `superior-outreach-llm`  
**Live demo:** [Demo available here](https://www.superioroutreach.ai/)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Run Locally](#run-locally)
  - [Build / Update the Vector Index](#build--update-the-vector-index)
- [WordPress Embed](#wordpress-embed)
- [API Endpoints (example)](#api-endpoints-example)
- [Deployment (Render)](#deployment-render)
- [Security Notes](#security-notes)
- [Roadmap](#roadmap)
- [Repo Structure (optional)](#repo-structure-optional)

---

## Overview

This project delivers a **website chatbot widget** designed to sit on a WordPress site and answer visitor questions about Superior Outreach’s services.

Unlike a generic chatbot, it uses **RAG** or Retrieval Augmented Generation:

1) Retrieve the most relevant snippets from a **FAISS** vector index  
2) Generate a response grounded in those snippets using **OpenAI (gpt-4o-mini)**

This repo is built to show UK industry-style engineering signals: **clean architecture**, **practical RAG**, **real embed integration**, and **deployable production shape** on **Render**.

---

## Key Features

### Embeddable Chat Widget (WordPress)
- Lightweight widget UI using **HTML / CSS / JavaScript**
- Embedded into WordPress via a script tag
- Widget assets are served from the FastAPI backend (hosted on Render)

### RAG with LangChain + FAISS
- Website content crawled from **superior-outreach.com** via **crawl4ai**
- Text chunking + embeddings stored in **FAISS**
- Similarity search retrieves top-K relevant chunks per query

### FastAPI Backend + OpenAI Integration
- FastAPI endpoint receives user message from the widget
- Retrieves context from FAISS index
- Calls **OpenAI gpt-4o-mini** to generate an answer
- Returns **answer-only** output (no citations)

### Basic Guards (open access)
- Public endpoint intended for widget usage
- Includes basic guardrails (e.g., input validation + prompt constraints)  
  *(If you add rate limiting / CORS allowlist, call that out here.)*

---

## Architecture

![System Architecture Diagram](https://github.com/raf945/superior-outreach-llm/raw/main/images/superior_outreach_cicd.png)

**Ingestion (build the index)**  
1. Crawl target pages using **crawl4ai**  
2. Extract + clean text and metadata (e.g., URL / title)  
3. Chunk content (with overlap)  
4. Generate **OpenAI embeddings** and build a **FAISS** index via LangChain  
5. Persist index artifacts to disk for runtime retrieval

**Runtime (visitor chat)**  
1. Visitor opens the widget in WordPress and asks a question  
2. Widget sends a request to the FastAPI backend (Render)  
3. Backend:
   - vector search in FAISS (top-K)
   - prompt = instructions + retrieved chunks + user question
   - OpenAI call (`gpt-4o-mini`)
4. Backend returns the generated answer to the widget UI

---

## Tech Stack

- **Backend:** Python, **FastAPI**
- **RAG / Vector Search:** **LangChain**, **FAISS**
- **Embeddings:** **OpenAI embeddings**
- **LLM:** OpenAI **gpt-4o-mini**
- **Crawler / Scraper:** **crawl4ai**
- **Frontend Widget:** Vanilla **HTML / CSS / JavaScript**
- **Hosting:** **Render** (backend + widget assets)
- **Embed Target:** WordPress

---

## Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key
- Git

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# App
APP_ENV=local

# Optional: paths (adjust to your codebase)
FAISS_INDEX_DIR=./data/faiss_index# Setup, Embed, Deployment & Next Steps

## Run Locally

```bash
git clone https://github.com/<your-username>/superior-outreach-llm.git
cd superior-outreach-llm

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

- App: http://localhost:8000  
- Docs: http://localhost:8000/docs   

---

## Deployment (Render)

Typical Render setup:

- Create a Web Service
- Connect your GitHub repo (`superior-outreach-llm`)
- Set environment variables in Render:
  - `OPENAI_API_KEY`
  - (Any index path vars you use)
- Ensure your service binds to Render’s port (commonly via `PORT` env var)

Common start command examples (choose the one that matches your app structure):

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Security Notes

Even for an open/public widget endpoint, these are good baseline practices:

- Never expose `OPENAI_API_KEY` in client-side code
- Validate inputs (length caps, basic sanitisation)
- Add prompt hardening (clear system rules, context delimiting)
- Consider CORS allowlisting to your WordPress domain(s)
- Consider rate limiting (per-IP / per-session) if traffic grows
- Avoid logging sensitive user content by default




