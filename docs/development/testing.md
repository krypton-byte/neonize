# Testing

Guide to testing Neonize.

## Overview

Neonize uses pytest for testing. This guide covers running tests, writing tests, and ensuring code quality.

## Running Tests

### Basic Test Run

```bash
pytest
```

### With Verbose Output

```bash
pytest -v
```

### Run Specific Tests

```bash
# Run a specific test file
pytest tests/test_client.py

# Run a specific test function
pytest tests/test_client.py::test_send_message

# Run tests matching a pattern
pytest -k "test_send"
```

### With Coverage

```bash
# Run with coverage report
pytest --cov=neonize

# Generate HTML coverage report
pytest --cov=neonize --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_client.py       # Client tests
├── test_events.py       # Event tests
├── test_utils.py        # Utility tests
└── integration/         # Integration tests
    └── test_real_connection.py
```

## Writing Tests

### Basic Test

```python
import pytest
from neonize.client import NewClient

def test_client_creation():
    """Test creating a new client."""
    client = NewClient("test_bot")
    assert client is not None
    assert client.name == "test_bot"
```

### Using Fixtures

```python
import pytest
from neonize.client import NewClient

@pytest.fixture
def client():
    """Create a test client."""
    return NewClient("test_bot", database=":memory:")

def test_send_message(client):
    """Test sending a message."""
    # Your test code here
    assert client.is_connected is False
```

### Mocking External Calls

```python
from unittest.mock import Mock, patch
from neonize.client import NewClient

def test_send_message_mock():
    """Test sending message with mocked network call."""
    with patch('neonize.client.NewClient.send_message') as mock_send:
        mock_send.return_value = Mock(ID="test123")
        
        client = NewClient("test")
        result = client.send_message(Mock(), "test")
        
        assert result.ID == "test123"
        mock_send.assert_called_once()
```

### Async Tests

```python
import pytest
from neonize.aioze.client import NewAClient

@pytest.mark.asyncio
async def test_async_client():
    """Test async client."""
    client = NewAClient("test_async")
    assert client is not None
```

## Test Categories

### Unit Tests

Test individual functions and methods:

```python
def test_build_jid():
    """Test JID building utility."""
    from neonize.utils import build_jid
    
    jid = build_jid("1234567890")
    assert jid.User == "1234567890"
    assert jid.Server == "s.whatsapp.net"
```

### Integration Tests

Test interactions between components:

```python
@pytest.mark.integration
def test_client_connection():
    """Test client connection flow."""
    # Integration test code
    pass
```

### End-to-End Tests

Test complete workflows:

```python
@pytest.mark.e2e
def test_send_and_receive():
    """Test sending and receiving messages."""
    # E2E test code
    pass
```

## Test Markers

### Skip Tests

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass
```

### Conditional Skip

```python
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass
```

### Expected Failure

```python
@pytest.mark.xfail
def test_known_bug():
    # This test is expected to fail
    assert False
```

## Parameterized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("test", "TEST"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Testing Best Practices

### 1. Use Descriptive Names

```python
# Good
def test_send_message_returns_message_id():
    pass

# Bad
def test_1():
    pass
```

### 2. Test One Thing

```python
# Good - tests one behavior
def test_client_connects_successfully():
    client = NewClient("test")
    assert client.is_connected is False

# Bad - tests multiple behaviors
def test_everything():
    client = NewClient("test")
    assert client.is_connected
    client.send_message(...)
    client.disconnect()
    # Too much in one test
```

### 3. Use Fixtures

```python
@pytest.fixture
def authenticated_client():
    """Provide an authenticated client for tests."""
    client = NewClient("test", database=":memory:")
    # Setup authentication
    yield client
    # Cleanup
    client.logout()
```

### 4. Clean Up Resources

```python
def test_with_cleanup():
    client = NewClient("test")
    try:
        # Test code
        assert client is not None
    finally:
        # Always cleanup
        client.disconnect()
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          pytest --cov=neonize --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Performance Testing

### Benchmark Tests

```python
import time
import pytest

def test_send_message_performance():
    """Test message sending performance."""
    client = NewClient("perf_test")
    
    start = time.time()
    # Perform operation
    client.send_message(Mock(), "test")
    duration = time.time() - start
    
    assert duration < 1.0  # Should complete in under 1 second
```

### Load Testing

```python
@pytest.mark.load
def test_concurrent_messages():
    """Test handling multiple concurrent messages."""
    from concurrent.futures import ThreadPoolExecutor
    
    client = NewClient("load_test")
    
    def send_message():
        return client.send_message(Mock(), "test")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_message) for _ in range(100)]
        results = [f.result() for f in futures]
    
    assert len(results) == 100
```

## Debugging Tests

### Print Debugging

```bash
pytest -s  # Don't capture output
```

### PDB Debugging

```bash
pytest --pdb  # Drop into debugger on failure
```

### Verbose Failure Output

```bash
pytest -vv  # Very verbose output
```

## Coverage Goals

Aim for:
- **80%+** overall code coverage
- **100%** for critical paths
- **90%+** for public APIs

Check coverage:

```bash
pytest --cov=neonize --cov-report=term-missing
```

## Next Steps

- [Contributing](contributing.md) - Contribute to Neonize
- [Building](building.md) - Build from source
- [Development Guide](index.md) - Development overview
