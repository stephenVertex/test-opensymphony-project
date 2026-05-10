# Test OpenSymphony Project

A hello-world CLI that prints greetings in English and Hebrew. A minimal Python project used to validate the OpenSymphony workflow integration with Linear.

## Prerequisites

- **Python 3.11+** — the project requires Python 3.11 or newer
- **[uv](https://docs.astral.sh/uv/)** (recommended) or **pip** for dependency management

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/stephenVertex/test-opensymphony-project.git
cd test-opensymphony-project
```

### 2. Install dependencies

Using **uv** (recommended):

```bash
# Create a virtual environment and install all dependencies
uv sync

# Or install in editable mode with dev dependencies
uv pip install -e ".[dev]"
uv pip install -r requirements.txt
```

Using **pip**:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the project in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Usage

### CLI

After installation, the `test-opsyn` command is available:

```bash
# Print hello-world in English and Hebrew
test-opsyn --hello-world

# Show help
test-opsyn --help
```

### Python library

```python
from src.hello import greet

print(greet("World"))
```

## Testing

```bash
# Run all tests
python3 -m pytest tests/

# Run with verbose output
python3 -m pytest tests/ -v
```

## Project Structure

```
├── src/
│   ├── hello.py              # Greeting library
│   └── test_opsyn/
│       └── cli.py            # CLI entry point (typer)
├── tests/
│   └── test_hello.py         # Unit tests
├── pyproject.toml            # Project metadata and dependencies
├── requirements.txt          # Development dependencies
├── config.yaml               # OpenSymphony configuration
├── AGENTS.md                 # Agent conventions
└── WORKFLOW.md               # Orchestration workflow
```

See [AGENTS.md](AGENTS.md) for project conventions and [WORKFLOW.md](WORKFLOW.md) for orchestration details.
