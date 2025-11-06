# Installation

Get the RAG Patterns Guide set up on your machine in just a few minutes.

## Prerequisites

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- (Optional) **Virtual environment tool** - venv, conda, or virtualenv

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rag-patterns-guide.git
cd rag-patterns-guide
```

### 2. Create Virtual Environment (Recommended)

=== "venv (Built-in)"

    ```bash
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

=== "conda"

    ```bash
    conda create -n rag-patterns python=3.10
    conda activate rag-patterns
    ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! You're ready to run the examples.

## Verify Installation

Test that everything is working:

```bash
cd patterns/01-semantic-chunking
python example.py
```

You should see colored terminal output showing the semantic chunking demo.

## Dependencies

The project uses minimal dependencies:

- **rich** - Beautiful terminal output (required for all examples)
- **pytest** - Testing framework (optional, for running tests)

Optional dependencies for advanced patterns:

- **anthropic** - For Claude API integration
- **openai** - For OpenAI API integration
- **sentence-transformers** - For production-quality embeddings
- **chromadb** - For vector database examples

## Troubleshooting

### Terminal Colors Not Showing

**Windows users:** If you don't see colors:

1. Use Windows Terminal (recommended) instead of Command Prompt
2. Or install: `pip install colorama`

### Import Errors

If you see `ModuleNotFoundError`:

```bash
# Make sure you're in the correct directory
cd rag-patterns-guide

# Reinstall dependencies
pip install -r requirements.txt
```

### Python Version Issues

Check your Python version:

```bash
python --version
```

Must be 3.10 or higher. If not, install a newer version.

## Next Steps

Now that you're set up, continue to the [Quick Start Guide](quickstart.md) to run your first pattern!
