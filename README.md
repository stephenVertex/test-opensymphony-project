# Test OpenSymphony Project

A hello-world CLI that prints greetings in English and Hebrew, plus a command-line calculator for basic arithmetic. A minimal Python project used to validate the OpenSymphony workflow integration with Linear.

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

### Calculator

```bash
# Add two numbers
test-opsyn calculate add 2 3
# Output: 5

# Subtract
test-opsyn calculate subtract 10 4
# Output: 6

# Multiply
test-opsyn calculate multiply 3 7
# Output: 21

# Divide
test-opsyn calculate divide 10 2
# Output: 5.0

# Float operands are supported
test-opsyn calculate add 1.5 2.5
# Output: 4.0

# Negative operands are supported (use -- to prevent -N being read as a flag)
test-opsyn calculate add -- -3 7
# Output: 4

# Division by zero is caught
test-opsyn calculate divide 5 0
# Output (stderr): Cannot divide by zero

# Unknown operation shows error
test-opsyn calculate modulo 5 3
# Output: Unknown operation: modulo. Choose from: add, subtract, multiply, divide
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
│       ├── calculator.py     # Calculator logic (add, subtract, multiply, divide)
│       └── cli.py            # CLI entry point (typer)
├── tests/
│   ├── test_calculator.py    # Calculator unit and CLI integration tests
│   └── test_hello.py         # Unit tests
├── pyproject.toml            # Project metadata and dependencies
├── requirements.txt          # Development dependencies
├── config.yaml               # OpenSymphony configuration
├── AGENTS.md                 # Agent conventions
└── WORKFLOW.md               # Orchestration workflow
```

See [AGENTS.md](AGENTS.md) for project conventions and [WORKFLOW.md](WORKFLOW.md) for orchestration details.
