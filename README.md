# Selamnew OKR Copilot – MVP

## 📌 Overview
Selamnew OKR Copilot is an **AI-powered OKR module** designed for internal use in our workspace platform.  
This MVP delivers **two key features** under one product umbrella:

1. **AI Suggestion for OKR Planning**  
   - Generates tailored Objectives & Key Results from historical data, OKR docs, and API inputs.
   - Uses Retrieval-Augmented Generation (RAG) and fine-tuned LLMs.
   
2. **Advanced OKR Chat Assistant**  
   - Acts as a **personal OKR coach, performance checker, and nudger**.
   - Provides context-aware recommendations based on progress metrics.

---

## 🧠 Architecture Summary
- **Data Sources:** Historical OKR datasets, API endpoints, planning docs & PDFs.
- **Pipeline:**  
  1. Ingest → Transform → Store (Data Lake + Data Warehouse)  
  2. Chunk & Embed (BERT) → Vector Search (FAISS/Pinecone)  
  3. Retrieve Context → Combine with Query → Send to LLM (GPT-4 fine-tuned model)
- **Key Components:**
  - **Cursor AI** – Development and prompt engineering
  - **Platform.OpenAI** – LLM testing, function calling, and cost tracking
  - **FAISS/Pinecone** – Vector similarity search
  - **Kafka** – Data ingestion and streaming

---

## ⚙️ Tech Stack
| Area | Technology |
|------|------------|
| Backend | Python (FastAPI), Node.js |
| LLM | OpenAI GPT-4 / GPT-3.5 + Fine-tuning |
| Embeddings | BERT, OpenAI text-embedding-ada-002 |
| Vector DB | FAISS (MVP) / Pinecone (scalable) |
| Data Layer | Kafka, S3 Data Lake, PostgreSQL Warehouse |
| Frontend | React + Next.js |
| Dev Tools | Cursor AI, Postman, GitHub Actions |

---


