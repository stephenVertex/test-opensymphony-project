# Test OpenSymphony Project

An OpenSymphony-managed project template. A minimal Python project used to validate the OpenSymphony workflow integration with Linear.

## Getting Started

Clone the repository and configure your environment:

```bash
# Clone the project
git clone https://github.com/stephenVertex/test-opensymphony-project.git
cd test-opensymphony-project
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.hello import greet

print(greet("World"))
```

## Testing

```bash
python3 -m pytest tests/
```

See [AGENTS.md](AGENTS.md) for project conventions and [WORKFLOW.md](WORKFLOW.md) for orchestration details.
