AST-aware repository RAG CLI for semantic code search, repository intelligence, and local codebase question answering.

RepoGraph indexes source code using AST chunking, generates embeddings locally with Ollama, stores vectors in Qdrant, and enables semantic retrieval + repository Q&A directly from your terminal.

---

# Features

- AST-aware code chunking
- Semantic code search
- Repository question answering
- Local embeddings with Ollama
- Local LLM-based repository chat
- Git intelligence support
- Qdrant vector storage
- CLI-first workflow
- Works on real-world repositories
- Fully local pipeline
- No cloud dependency required
:
---

# Architecture

```text
Repository
   ↓
Repository Loader
   ↓
AST Chunker
   ↓
Embedding Formatter
   ↓
Ollama Embeddings
   ↓
Qdrant Vector Store
   ↓
Semantic Retrieval
   ↓
LLM Prompt Builder
   ↓
Repository Answering
```

---

# Tech Stack

| Component | Technology |
|---|---|
| CLI | Typer |
| Terminal UI | Rich |
| AST Parsing | Tree-sitter |
| Embeddings | Ollama + nomic-embed-text |
| LLM | Qwen via Ollama |
| Vector DB | Qdrant |
| Validation | Pydantic |

---

# Supported Languages

Current support:

- Python

Planned:

- TypeScript
- JavaScript
- Go
- Rust

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/Amannnrt/repograph.git

cd repograph
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install RepoGraph

```bash
pip install -e .
```

This installs the `repograph` CLI command globally inside the virtual environment.

---

# Ollama Setup

RepoGraph uses Ollama for:
- embeddings
- local LLM inference

Install Ollama:

https://ollama.com

---

## Pull Embedding Model

```bash
ollama pull nomic-embed-text
```

---

## Pull LLM Model

```bash
ollama pull qwen2.5:1.5b
```

You may also use:
- llama3
- mistral
- deepseek
- qwen2.5
- codellama

by changing provider configuration.

---

# Basic Usage

---

# Index Repository

```bash
repograph index .
```

Example output:

```text
Indexing repository...
Loaded 142 source files
Extracted 891 chunks
Generating embeddings...
Stored embeddings in Qdrant
```

---

# Semantic Search

```bash
repograph search "authentication logic"
```

Example:

```bash
repograph search "request context"
```

RepoGraph retrieves semantically relevant code chunks instead of keyword matches.

---

# Repository Q&A

```bash
repograph ask "How are embeddings generated?"
```

Example:

```bash
repograph ask "How does Flask request context work?"
```

RepoGraph:
1. retrieves relevant chunks
2. builds repository context
3. queries local LLM
4. generates repository-aware answer

---

# Repository Status

```bash
repograph status
```

Example output:

```text
RepoGraph Status

Collection: code_chunks
Chunks Indexed: 842
Vector Size: 768
Distance: Cosine
Vector DB: .repograph/qdrant
```

---

# Version

```bash
repograph version
```

---

# Evaluation

RepoGraph includes a lightweight retrieval evaluation pipeline.

Run:

```bash
repograph eval
```

Evaluation dataset:

```text
repograph/evaluation/dataset/
```

---

# Git Intelligence

RepoGraph can attach git metadata to indexed chunks.

This enables future capabilities such as:
- commit-aware retrieval
- blame-aware context
- historical reasoning
- ownership analysis
- commit message retrieval

Current metadata includes:
- latest commit hash
- author
- commit message
- commit date

---

# Example Workflow

---

## Clone RepoGraph

```bash
git clone https://github.com/Amannnrt/repograph.git
cd repograph
pip install -e .
```

---

## Clone Another Repository

Example:

```bash
git clone https://github.com/pallets/flask.git
```

---

## Index Flask

```bash
cd flask

repograph index .
```

---

## Search Flask

```bash
repograph search "routing system"
```

---

## Ask Questions

```bash
repograph ask "How are routes registered?"
```

---

# Project Structure

```text
repograph/
├── cli/
├── core/
├── evaluation/
├── git/
├── indexing/
├── parsing/
├── providers/
├── retrieval/
├── storage/
└── utils/
```

---

# Core Components

---

## Repository Loader

Responsible for:
- recursive repository scanning
- extension filtering
- ignored directories
- structured file loading

File:

```text
repograph/indexing/loader.py
```

---

## AST Chunker

Extracts:
- functions
- classes
- async functions
- metadata
- imports
- docstrings

using Tree-sitter.

File:

```text
repograph/parsing/treesitter/python_parser.py
```

---

## Embedding Pipeline

Formats chunks for embedding and generates vectors using Ollama.

Files:

```text
repograph/indexing/embedding_formatter.py
repograph/providers/embeddings/
```

---

## Vector Storage

Stores embeddings inside local Qdrant database.

File:

```text
repograph/storage/vector_store.py
```

---

## Retrieval

Performs semantic retrieval using vector similarity.

File:

```text
repograph/retrieval/retriever.py
```

---

## Prompt Builder

Constructs repository-aware prompts for the LLM.

File:

```text
repograph/retrieval/prompt_builder.py
```

---

# Current Limitations

- Python-focused currently
- No reranking yet
- Large chunk splitting still basic
- No incremental indexing yet
- No hybrid BM25 retrieval yet
- No multi-repository indexing yet

---

# Planned Features

- Reranking
- Incremental indexing
- TypeScript support
- JavaScript support
- Graph-based retrieval
- Symbol relationship mapping
- Multi-repo indexing
- Hybrid search
- Chunk hierarchy
- Dependency graph analysis
- Remote repository indexing
- Web UI
- VSCode extension

---

# Why RepoGraph?

Most repository assistants are:
- cloud-based
- expensive
- opaque
- editor-locked

RepoGraph is:
- local-first
- hackable
- AST-aware
- CLI-native
- lightweight
- developer-friendly

---

# Inspiration

RepoGraph draws inspiration from:
- Sourcegraph Cody
- Cursor
- Continue.dev
- Graph-based code intelligence systems
- Modern RAG architectures

---

# Development

Install dev dependencies:

```bash
pip install -r requirements.txt
```

Run indexing:

```bash
repograph index .
```

Run search:

```bash
repograph search "vector store"
```

---

# Contributing

Contributions are welcome.

Potential areas:
- language parsers
- retrieval quality
- reranking
- chunking improvements
- evaluation benchmarks
- UI improvements
- performance optimization

---

# License

MIT License

---

# Author

Mohammad Aman.

---

# RepoGraph Vision

The long-term goal of RepoGraph is to become:

- a local-first repository intelligence engine
- a semantic developer search system
- an AST-aware repository reasoning framework
- a foundation for advanced code RAG systems

without requiring proprietary cloud infrastructure. , so how do we go on about making this into tab completion
