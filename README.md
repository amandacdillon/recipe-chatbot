# Recipe Chatbot - AI Evaluations Course

This repository contains a complete AI evaluations course built around a Recipe Chatbot. Through 5 progressive homework assignments, you'll learn practical techniques for evaluating and improving AI systems.

## Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/ai-evals-course/recipe-chatbot.git
   cd recipe-chatbot
   uv sync
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env to add your model and API keys
   ```

3. **Run the Chatbot**
   ```bash
   uv run uvicorn backend.main:app --reload
   # Open http://127.0.0.1:8000
   ```

## Course Overview

### Homework Progression

1. **HW1: Basic Prompt Engineering** (`homeworks/hw1/`)
   - Write system prompts and expand test queries
   - Walkthrough: See HW2 walkthrough for HW1 content

2. **HW2: Error Analysis & Failure Taxonomy** (`homeworks/hw2/`)
   - Systematic error analysis and failure mode identification
   - **Interactive Walkthrough**:
      - Code: `homeworks/hw2/hw2_solution_walkthrough.ipynb`
      - [video 1](https://youtu.be/h9oAAAYnGx4?si=fWxN3NtpSbdD55cW): walkthrough of code
      - [video 2](https://youtu.be/AKg27L4E0M8) : open & axial coding walkthrough

3. **HW3: LLM-as-Judge Evaluation** (`homeworks/hw3/`)
   - Automated evaluation using the `judgy` library
   - **Interactive Walkthrough**:
      - Code: `homeworks/hw3/hw3_walkthrough.ipynb`
      - [video](https://youtu.be/1d5aNfslwHg): walkthrough of solution

4. **HW4: RAG/Retrieval Evaluation** (`homeworks/hw4/`)
   - BM25 retrieval system with synthetic query generation
   - **Interactive Walkthroughs**: 
     - `homeworks/hw4/hw4_walkthrough.py` (Marimo)
     - [video](https://youtu.be/GMShL5iC8aY): walkthrough of solution

5. **HW5: Agent Failure Analysis** (`homeworks/hw5/`)
   - Analyze conversation traces and failure patterns
   - **Interactive Walkthroughs**:
      - `homeworks/hw5/hw5_walkthrough.py` (Marimo)
      - [video](https://youtu.be/z1oISsDUKLA) 

### Key Features

- **Backend**: FastAPI with LiteLLM (multi-provider LLM support)
- **Frontend**: Simple chat interface with conversation history
- **Annotation Tool**: FastHTML-based interface for manual evaluation (`annotation/`)
- **Retrieval**: BM25-based recipe search (`backend/retrieval.py`)
- **Query Rewriting**: LLM-powered query optimization (`backend/query_rewrite_agent.py`)
- **Evaluation Tools**: Automated metrics, bias correction, and analysis scripts

## System Prompt Engineering (HW1 Implementation)

The recipe chatbot uses a carefully engineered system prompt (`backend/utils.py`) designed around three core principles for reliable AI behavior:

### 1. User Unhappiness Prevention
The prompt explicitly prevents common failure modes that would frustrate users:
- **Dietary Safety**: Never suggests ingredients that conflict with stated allergies or restrictions
- **Accessibility**: Uses common, obtainable ingredients unless exotic ones are specifically requested
- **Completeness**: Always provides complete recipes with clear instructions, cooking times, and temperatures
- **Safety**: Prohibits unsafe cooking methods or food handling practices

### 2. Clear Specifications

**Must Always Do:**
- Structure responses with consistent Markdown formatting
- Begin with recipe name as Level 2 heading (e.g., `## Creamy Mushroom Risotto`)
- Include brief, appetizing description (1-3 sentences)
- Provide `### Ingredients` section with precise measurements
- Provide `### Instructions` section with numbered steps
- Specify serving size (defaults to 2-4 servings)
- Respect ALL dietary restrictions and preferences

**Must Never Do:**
- Ignore stated allergies or dietary restrictions
- Suggest rare ingredients without alternatives
- Ask follow-up questions (provides complete recipe immediately)
- Use offensive language or make cooking skill assumptions

### 3. Defined Agency (Medium Level)
The bot has creative freedom within safe boundaries:
- **Adaptability**: Can suggest variations and ingredient substitutions
- **Problem-Solving**: Adapts traditional recipes for dietary needs (vegan, gluten-free, etc.)
- **Time Awareness**: Prioritizes recipes that fit stated time constraints
- **Enhancement**: May add helpful `### Tips` or `### Notes` sections
- **Contextual Choice**: Selects appropriate recipes for vague requests

### How It Works
Each rule is designed to be **checkable** for systematic evaluation:
- "Does the output contain an 'Ingredients' section?" ✓
- "If allergies were mentioned, are those ingredients avoided?" ✓  
- "Are cooking times provided for relevant steps?" ✓
- "Is the recipe feasible within stated time constraints?" ✓

This approach enables the progressive evaluation techniques taught throughout the course, from basic prompt testing (HW1) to sophisticated failure analysis (HW5).

## Project Structure

```
recipe-chatbot/
├── backend/               # FastAPI app & core logic
├── frontend/              # Chat UI (HTML/CSS/JS)
├── homeworks/             # 5 progressive assignments
│   ├── hw1/              # Prompt engineering
│   ├── hw2/              # Error analysis (with walkthrough)
│   ├── hw3/              # LLM-as-Judge (with walkthrough)
│   ├── hw4/              # Retrieval eval (with walkthroughs)
│   └── hw5/              # Agent analysis
├── annotation/            # Manual annotation tools
├── scripts/               # Utility scripts
├── data/                  # Datasets and queries
└── results/               # Evaluation outputs
```

## Running Homework Scripts

Each homework includes complete pipelines. For example:

**HW3 Pipeline:**
```bash
cd homeworks/hw3
uv run python scripts/generate_traces.py
uv run python scripts/label_data.py
uv run python scripts/develop_judge.py
uv run python scripts/evaluate_judge.py
```

**HW4 Pipeline:**
```bash
cd homeworks/hw4
uv run python scripts/process_recipes.py
uv run python scripts/generate_queries.py
uv run python scripts/evaluate_retrieval.py
# Optional: uv run python scripts/evaluate_retrieval_with_agent.py
```

## Additional Resources

- **Annotation Interface**: Run `uv run python annotation/annotation.py` for manual evaluation
- **Bulk Testing**: Use `uv run python scripts/bulk_test.py` to test multiple queries
- **Trace Analysis**: All conversations saved as JSON for analysis

## Environment Variables

Configure your `.env` file with:
- `MODEL_NAME`: LLM model (e.g., `openai/gpt-4`, `anthropic/claude-3-haiku-20240307`)
- API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for supported providers.

## Course Philosophy

This course emphasizes:
- **Practical experience** over theory
- **Systematic evaluation** over "vibes"
- **Progressive complexity** - each homework builds on previous work
- **Industry-standard techniques** for real-world AI evaluation
