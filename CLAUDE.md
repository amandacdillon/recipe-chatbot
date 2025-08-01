# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Recipe Chatbot built for an AI evaluations course. The system combines a FastAPI backend with LiteLLM for multi-provider LLM support, a simple HTML/CSS/JS frontend, and comprehensive evaluation tools for testing AI system performance.

## Common Commands

### Development Server
```bash
# Start the main chatbot server
uv run uvicorn backend.main:app --reload
# Access at http://127.0.0.1:8000

# Start annotation tool for manual evaluation
uv run python annotation/annotation.py
```

### Environment Setup
```bash
# Install dependencies
uv sync

# Configure environment
cp env.example .env
# Edit .env to add your MODEL_NAME and API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
```

### Testing and Evaluation
```bash
# Bulk testing
uv run python scripts/bulk_test.py

# Run homework evaluation pipelines
cd homeworks/hw3 && uv run python scripts/generate_traces.py
cd homeworks/hw4 && uv run python scripts/evaluate_retrieval.py
```

## Architecture

### Core Components
- **Backend (`backend/`)**: FastAPI application with LiteLLM integration
  - `main.py`: FastAPI routes and conversation trace logging
  - `utils.py`: System prompt and LLM wrapper using LiteLLM
  - `retrieval.py`: BM25-based recipe search functionality  
  - `query_rewrite_agent.py`: LLM-powered query optimization
  - `evaluation_utils.py`: Metrics and evaluation utilities

- **Frontend (`frontend/`)**: Simple chat interface (HTML/CSS/JS)
  - `index.html`: Single-page chat application

- **Annotation System (`annotation/`)**: FastHTML-based manual evaluation tool
  - `annotation.py`: Web interface for labeling conversation traces
  - `traces/`: Directory where conversation traces are automatically saved

### Key Design Patterns
- All conversations are automatically logged as JSON traces in `annotation/traces/`
- System uses LiteLLM for model-agnostic LLM calls - configure via `MODEL_NAME` env var
- FastAPI backend serves both API endpoints and static frontend files
- Evaluation scripts are organized in homework directories for progressive learning

### Environment Configuration
The system requires a `.env` file with:
- `MODEL_NAME`: LLM model identifier (e.g., `openai/gpt-4`, `anthropic/claude-3-haiku-20240307`)
- Provider API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

See [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for supported model formats.

### Evaluation Framework
The codebase includes 5 progressive homework assignments (`homeworks/hw1-hw5/`) that demonstrate:
- Prompt engineering and systematic error analysis
- LLM-as-Judge evaluation using the `judgy` library
- RAG/retrieval system evaluation with BM25
- Agent failure analysis and conversation trace analysis

Each homework contains complete evaluation pipelines with data processing, metric computation, and analysis scripts.