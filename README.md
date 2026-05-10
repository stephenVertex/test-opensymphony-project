# Test OpenSymphony Project

A minimal Python project used to validate the OpenSymphony workflow integration with Linear.

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