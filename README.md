# LLM Log Analyzer

A CLI tool that analyzes application logs using Large Language Models (LLMs), with
support for multiple backends, fallback, and lightweight retrieval-augmented generation (RAG).

---

## Features

- Analyze logs using LLMs
- Multiple LLM backends:
  - Ollama (local)
  - OpenAI
  - DeepSeek
  - Hugging Face
- Automatic LLM fallback (comma-separated priority)
- Lightweight RAG using a domain knowledge file
- Secure API key management via `.env`

---

## Installation

```bash
pip install -r requirements.txt

