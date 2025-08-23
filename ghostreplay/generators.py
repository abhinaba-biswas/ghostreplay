# ghostreplay/generators.py
import json
from pathlib import Path
from typing import Optional
from .models import IncidentContext, TestGenerationConfig


class TestGenerator:
    """Generates test files from IncidentContext."""
    
    def __init__(self, config: TestGenerationConfig):
        self.config = config
    
    def generate_pytest_test(self, incident: IncidentContext) -> str:
        """Generate a pytest test file content."""
        test_content = self._generate_pytest_template(incident)
        return test_content
    
    def _generate_pytest_template(self, incident: IncidentContext) -> str:
        """Generate the actual pytest test template."""
        # Create safe test name from endpoint
        test_name = incident.endpoint.replace('/', '_').replace('-', '_').strip('_')
        if not test_name:
            test_name = "api_endpoint"
        
        # Format request body for test
        body_str = ""
        if incident.body:
            body_str = f"    request_body = {json.dumps(incident.body, indent=8)[4:]}"
        else:
            body_str = "    request_body = {}"
        
        # Generate test content
        template = f'''"""
Generated test from production error log
Incident timestamp: {incident.timestamp.isoformat()}
Endpoint: {incident.method} {incident.endpoint}
"""
import pytest
from freezegun import freeze_time
from unittest.mock import Mock, patch
import json


class Test{test_name.title().replace('_', '')}Error:
    """Test class for reproducing production error on {incident.endpoint}"""
    
    @freeze_time("{incident.timestamp.isoformat()}")
    def test_{test_name}_reproduces_error(self):
        """
        Reproduces the production error that occurred at {incident.timestamp}
        
        Original error: {incident.error_message or "Unknown error"}
        Stack trace: {incident.stack[:100]}...
        """
{body_str}
        
        # TODO: Setup your application/client here
        # client = YourAppClient()
        
        # TODO: Make the request that caused the error
        # response = client.{incident.method.lower()}("{incident.endpoint}", json=request_body)
        
        # TODO: Assert the error condition
        # assert response.status_code == {incident.status_code or 500}
        # assert "expected error message" in response.json()["error"]
        
        # Placeholder assertion - replace with actual test logic
        with pytest.raises(Exception) as exc_info:
            raise Exception("Replace this with actual failing code")
        
        assert "Replace this with actual error validation" in str(exc_info.value)
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock external dependencies that might affect the test."""
        with patch('your_module.external_service') as mock_service:
            mock_service.return_value = Mock()
            yield mock_service
    
    def test_{test_name}_with_valid_input_should_pass(self):
        """
        Test with valid input to ensure the fix works
        TODO: Implement after fixing the bug
        """
        pass
'''
        return template
    
    def write_test_file(self, incident: IncidentContext) -> Path:
        """Generate and write the test file to disk."""
        test_content = self.generate_pytest_test(incident)
        
        output_path = Path(self.config.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(test_content)
        
        return output_path


class AIFixSuggester:
    """Suggests AI-generated patch scaffolds."""
    
    @staticmethod
    def suggest_fix(test_file_path: str) -> str:
        """Generate a mock AI suggestion for fixing the code."""
        # For hackathon demo, return a realistic mock suggestion
        mock_suggestion = f"""
🤖 AI Fix Suggestion for {test_file_path}

Based on the failing test, here's a suggested patch scaffold:

## Potential Root Causes:
1. **Null/undefined value handling**: Check for missing input validation
2. **Race condition**: Consider adding proper synchronization
3. **External dependency failure**: Add retry logic or fallback

## Suggested Code Changes:

```python
# 1. Add input validation
def validate_request(data):
    if not data or 'required_field' not in data:
        raise ValidationError("Missing required field")
    return True

# 2. Add error handling wrapper
def safe_operation(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SpecificException as e:
            logger.error(f"Operation failed: {{e}}")
            return {{\"error\": str(e), \"status\": \"failed\"}}
    return wrapper

# 3. Add retry logic for external calls
@retry(max_attempts=3, backoff=ExponentialBackoff())
def call_external_service(payload):
    # Your external service call here
    pass
```

## Next Steps:
1. ✅ Implement the validation logic
2. ✅ Add proper error handling
3. ✅ Write additional edge case tests
4. ✅ Test the fix against the generated test

*This is a mock suggestion for hackathon demo. In production, this would be powered by a real AI model analyzing the stack trace and code context.*
"""
        return mock_suggestion
