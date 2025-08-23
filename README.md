# README.md
# 🔄 GhostReplay

**Turn production error logs into reproducible failing tests and get AI-powered fix suggestions.**

GhostReplay bridges the gap between observability (logs) and fixing (tests + patches) by automatically generating test cases from your production errors.

## 🎯 Features

- **📥 Log Ingestion**: Parse structured JSON error logs into standardized incident contexts
- **🧪 Test Generation**: Automatically generate pytest files that reproduce production errors  
- **🤖 AI Suggestions**: Get intelligent patch scaffolds and fix recommendations
- **⏰ Time Control**: Use `freezegun` to reproduce time-sensitive bugs
- **🎨 Rich CLI**: Beautiful command-line interface with syntax highlighting

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone https://github.com/yourusername/ghostreplay.git
cd ghostreplay
pip install -e .

# Or install from PyPI (when published)
pip install ghostreplay
```

### Basic Usage

```bash
# 1. Parse an error log
ghostreplay ingest error.json

# 2. Generate a test file
ghostreplay gen-test --log error.json --out tests/test_bug.py

# 3. Get AI fix suggestions  
ghostreplay suggest-fix tests/test_bug.py

# 4. Run the demo
ghostreplay demo
```

## 📋 Log Format

GhostReplay expects JSON logs with these fields:

```json
{
  "method": "POST",
  "endpoint": "/api/users/create", 
  "body": {"username": "john", "email": "john@example.com"},
  "stack": "Traceback (most recent call last):\n  File \"/app/users.py\"...",
  "timestamp": "2024-01-15T10:30:45Z",
  "status_code": 400,
  "error_message": "Email already exists",
  "user_id": "user_123"
}
```

## 🧪 Generated Tests

Example generated test:

```python
import pytest
from freezegun import freeze_time
from unittest.mock import Mock, patch

class TestApiUsersCreateError:
    @freeze_time("2024-01-15T10:30:45Z")
    def test_api_users_create_reproduces_error(self):
        request_body = {
            "username": "john",
            "email": "john@example.com"
        }
        
        # TODO: Setup your application/client here
        # client = YourAppClient()
        
        # TODO: Make the request that caused the error
        # response = client.post("/api/users/create", json=request_body)
        
        # TODO: Assert the error condition  
        # assert response.status_code == 400
        # assert "Email already exists" in response.json()["error"]
        
        with pytest.raises(Exception) as exc_info:
            raise Exception("Replace this with actual failing code")
```

## 🏗️ Project Structure

```
ghostreplay/
├── ghostreplay/
│   ├── __init__.py
│   ├── cli.py          # Typer CLI commands
│   ├── models.py       # Pydantic models
│   ├── parser.py       # Log parsing logic  
│   └── generators.py   # Test & suggestion generation
├── tests/
├── setup.py
├── pyproject.toml
└── README.md
```

## 🔧 Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run CLI locally
python -m ghostreplay.cli --help
```

## 🎭 Hackathon Demo

```bash
# Run the complete demo workflow
ghostreplay demo

# This creates a sample error log and shows all commands
```

## 🤖 AI Integration

For the hackathon MVP, AI suggestions are mocked. In production, you could integrate with:

- OpenAI GPT-4
- Claude
- Local models via Ollama
- Custom fine-tuned models

## 🛣️ Roadmap

- [ ] **Multiple Frameworks**: Support Jest, JUnit, etc.
- [ ] **Real AI Integration**: Connect to actual LLM APIs
- [ ] **Advanced Parsing**: Support more log formats
- [ ] **Web UI**: Browser-based interface
- [ ] **CI/CD Integration**: GitHub Actions, Jenkins plugins
- [ ] **Observability Integration**: Datadog, New Relic connectors

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Make your changes
4. Add tests
5. Submit a pull request

---