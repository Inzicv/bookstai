# BookstAI

**BookstAI** is a local-first book analysis and content generation framework built around:

Next.js UI
↓
FastAPI API
↓
Python workflows

## Features

- 📖 **Memory System**: Read and parse Markdown-based memory files
- 🔄 **Reusable Components**: Build upon a foundation of well-tested components
- 🎯 **Type-Safe**: Full type hints and configuration management
- 🧪 **Well-Tested**: Comprehensive test suite for reliability

## Installation

### Development Installation

```bash
# Clone the repository
git clone https://github.com/Inzicv/bookstai.git
cd bookstai

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Production Installation

```bash
pip install bookstai
```

## Quick Start

### Reading Memory Files

```python
from pathlib import Path
from bookstai import MemoryReader

# Read a Markdown file
reader = MemoryReader(Path("memory/books/example.md"))

# Get all sections
sections = reader.parse()
print(sections)

# Get a specific section
intro = reader.get_section("Introduction")

# Check if section exists
if reader.section_exists("Characters"):
    print(reader.get_section("Characters"))
```

### Configuration

```python
from bookstai import BookstAISettings, load_settings

# Load settings from environment variables
settings = load_settings()

# Or create custom settings
settings = BookstAISettings(
    memory_root=Path("./memory"),
    output_root=Path("./output"),
    provider="openai",
    model="gpt-4",
    temperature=0.7
)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/bookstai

# Run specific test file
pytest tests/test_memory_reader.py
```

## Project Structure

```
bookstai/
├── src/bookstai/
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   ├── errors.py        # Custom exceptions
│   │   └── types.py         # Type definitions
│   ├── memory/
│   │   └── reader.py        # MemoryReader component
│   ├── agents/              # Agent implementations (future)
│   ├── workflows/           # Workflow definitions (future)
│   └── exports/             # Export utilities (future)
├── tests/                   # Test suite
└── pyproject.toml          # Project configuration
```

## Development

### Code Style

This project uses:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Format code before committing:

```bash
black src/ tests/
isort src/ tests/
```

### Type Checking

```bash
mypy src/bookstai/
```

## Sprint 1: Foundation

Sprint 1 establishes the core foundation of BookstAI:

- ✅ Project structure and configuration management
- ✅ Type definitions and custom exceptions
- ✅ MemoryReader component for parsing Markdown files
- ✅ Comprehensive test suite

See [Roadmap](docs/roadmap.md) for more details.

## Usage rapide

Voir :

- `docs/commands.md`
- `docs/daily-usage.md`

Commandes principales :

```text
bookstai review
bookstai song
bookstai hitl
bookstai learning
bookstai history
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **BookstAI Team**
